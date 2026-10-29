#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Validate MKL robustness diagrams (boundary/control/entity) in PlantUML.

Implements audit layer 1: output syntax and deterministic connection rules.
Errors identify rule violations; warnings require analyst judgment because the
validator does not understand the domain. Boundaries/entities are nouns and
controls are verbs: a noun-to-noun connection identifies a missing function.

Usage:
    python3 validate_robustness_puml.py diagram.puml
    python3 validate_robustness_puml.py diagram.puml --domain domain_model.puml

With --domain, unmatched entities are reported as object-discovery candidates.
Exit codes: 0 = no errors; 1 = validation errors; 2 = usage or input error.
Legacy machine-readable keys and function names remain compatible.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# Types and rules.

TYPES = ("actor", "boundary", "control", "entity")

# Unordered permitted pairs; every other known pair is prohibited.
VALID_PAIRS = {
    frozenset({"actor", "boundary"}),
    frozenset({"boundary", "control"}),
    frozenset({"control"}),               # control-control
    frozenset({"control", "entity"}),
}

INVALID_PAIRS = {
    frozenset({"actor", "control"}): "an actor cannot communicate directly with a control; use a boundary object",
    frozenset({"actor", "entity"}): "an actor cannot communicate directly with an entity; use a boundary object",
    frozenset({"boundary", "entity"}): "a boundary cannot communicate directly with an entity; a control is missing",
    frozenset({"boundary"}): "boundaries cannot communicate directly; a control is missing",
    frozenset({"entity"}): "entities cannot communicate directly; a control is missing",
    # The course matrix explicitly disallows actor-to-actor communication.
    frozenset({"actor"}): "actors cannot communicate directly; robustness diagrams model interaction with the system",
}

ALIAS_PREFIX = {"actor": "ACT_", "boundary": "B_", "control": "C_", "entity": "E_"}

REQUIRED_DIRECTIVES = (
    "left to right direction",
    "skinparam linetype ortho",
    "skinparam shadowing false",
)

# Heuristics, retaining Spanish and English input vocabulary.

GENERIC_BOUNDARY = (
    "pagina web", "pagina", "pantalla", "web page", "page", "screen",
    "formulario", "form", "ventana", "window", "interfaz", "interface", "vista", "view",
)

TECH_TERMS = (
    "jsp", "asp", "aspx", "servlet", "html", "php", "react", "angular", "vue",
    "api", "endpoint", "rest", "json", "xml", "sql", "jquery", "bootstrap", "dao",
)

# Only widgets clearly below screen level. A plain main menu may be a valid screen.
WIDGET_TERMS = (
    "boton", "button", "campo de texto", "checkbox", "radio button", "dropdown",
    "combo", "combobox", "menu desplegable", "menu contextual", "casilla",
    "barra de desplazamiento", "icono", "text field", "context menu", "scrollbar", "icon",
)

GENERIC_CONTROLLER = (
    "mostrar", "display", "gestionar", "procesar", "manejar", "ejecutar",
    "hacer", "realizar", "controlar", "manage", "process", "handle", "show", "execute", "do", "perform", "control",
)

# A control name beginning with a noun may indicate a misclassified boundary/entity.
# Check only the start: "Show payment form" is an appropriate action name.
NOUNY_CONTROLLER = (
    "pagina", "pantalla", "formulario", "ventana", "page", "screen", "form",
    "lista", "listado", "reporte", "informe", "mensaje", "window", "list", "listing", "report", "message",
)

MAX_ELEMENTS_HINT = 25
GOD_CONTROLLER_DEGREE = 6   # Review controls exceeding this degree.
CONTROL_CHAIN_HINT = 3      # Control clusters may indicate undistributed logic.

# Utilities.


def strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def norm(text: str) -> str:
    return strip_accents(text).lower().strip()


# Ignore linking words when comparing natural names with compact domain identifiers.
STOPWORDS = {"de", "del", "la", "el", "los", "las", "un", "una", "y", "of", "the", "a", "and"}


def key(text: str) -> str:
    """Normalize a comparison key: lowercase, without accents, separators, or stopwords."""
    words = [w for w in re.split(r"[\s_\-]+", norm(text)) if w]
    meaningful = [w for w in words if w not in STOPWORDS]
    return "".join(meaningful or words)


# Normalize flow ID variants (FA-01, FA1, FA 1, FE-3) to stable comparison keys.
FLUJO_RE = re.compile(r"\b(FA|FE)\s*[-_ ]?\s*0*(\d+)\b", re.IGNORECASE)


def flujos_declarados(text: str) -> set[str]:
    """Extract normalized alternative/exception flow IDs (FA1, FE3, ...)."""
    return {f"{m.group(1).upper()}{int(m.group(2))}" for m in FLUJO_RE.finditer(text or "")}


# Parsing.

DECL_RE = re.compile(
    r'^\s*(?P<type>actor|boundary|control|entity)\s+'
    r'(?:"(?P<label>[^"]+)"\s+as\s+(?P<alias1>\w+)|(?P<alias2>\w+)(?:\s+as\s+(?P<alias3>\w+))?)'
    # Optional fill color marks objects exclusive to alternative courses.
    r'(?:\s+(?P<color>#[#\w]+))?\s*$',
    re.IGNORECASE,
)

# Flexible PlantUML relationship connector and optional label.
REL_RE = re.compile(
    r'^\s*(?P<left>\w+)\s*'
    r'(?P<conn><?[-.]{1,3}(?:\[[^\]]*\])?[-.]{0,3}>?)\s*'
    r'(?P<right>\w+)\s*'
    r'(?::\s*(?P<label>.*?))?\s*$'
)

CLASS_RE = re.compile(
    r'^\s*(?:abstract\s+)?(?:class|entity|enum)\s+'
    r'(?:"(?P<q>[^"]+)"|(?P<p>[\wÀ-ſ]+))',
    re.IGNORECASE,
)


class Element:
    __slots__ = ("alias", "label", "etype", "line", "color")

    def __init__(self, alias: str, label: str, etype: str, line: int, color: str = ""):
        self.alias = alias
        self.label = label
        self.etype = etype.lower()
        self.line = line
        self.color = color or ""

    @property
    def display(self) -> str:
        return self.label or self.alias


def model_code(text: str, keep_notes: bool = False) -> str:
    """Keep note flow labels when requested, but exclude commented models."""
    text = re.sub(r"^[ \t]*/'[\s\S]*?(?:'/|\Z)",
                  lambda m: "\n" * m.group().count("\n"), text, flags=re.M)
    if keep_notes:
        return text
    lines, annotation = [], False
    for raw in text.split("\n"):
        line = raw.strip()
        if annotation:
            lines.append("")
            if re.match(r"^end\s*(?:[hr]?note|legend)\b", line, re.I):
                annotation = False
        elif re.match(r"^(?:[hr]?note|legend)\b", line, re.I):
            lines.append("")
            header = re.sub(r'"(?:\\.|[^"\\])*"', "", line)
            annotation = not (":" in header or re.match(r'^[hr]?note\s+"', line, re.I))
        else:
            lines.append("" if line.startswith("'") else raw)
    return "\n".join(lines)


def parse_diagram(text: str):
    text = model_code(text, keep_notes=True)
    elements: dict[str, Element] = {}
    relations: list[tuple[str, str, str, int, str]] = []  # left, right, label, line, connector
    unparsed: list[tuple[int, str]] = []
    note_lines: list[str] = []  # attached use case text for coverage checks

    in_block = False  # inside a multiline note/legend

    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()

        # Skip note/legend blocks when parsing relationships, but retain their text
        # for declared-flow coverage checks.
        if in_block:
            if re.match(r"^end\s*([hr]?note|legend)\b", line, re.IGNORECASE):
                in_block = False
            else:
                note_lines.append(line)
            continue

        if not line or line.startswith("'") or line.startswith("@"):
            continue

        if re.match(r"^([hr]?note|legend)\b", line, re.IGNORECASE):
            # One-line note forms have inline text or a quoted alias declaration.
            single_line = re.search(r":\s*\S", re.sub(r'"(?:\\.|[^"\\])*"', "", line)) or re.search(
                r'^\s*[hr]?note\s+"[^"]*"\s+as\s+\w+', line, re.IGNORECASE
            )
            if single_line:
                note_lines.append(line)
            else:
                in_block = True
            continue

        if line.lower().startswith(("skinparam", "title", "hide", "left to", "top to", "!")):
            continue

        decl = DECL_RE.match(line)
        if decl:
            etype = decl.group("type").lower()
            alias = decl.group("alias1") or decl.group("alias3") or decl.group("alias2")
            label = decl.group("label") or (decl.group("alias2") if decl.group("alias3") else "") or ""
            elements[alias] = Element(alias, label, etype, n, decl.group("color") or "")
            continue

        rel = REL_RE.match(line)
        if rel and rel.group("conn"):
            relations.append(
                (
                    rel.group("left"),
                    rel.group("right"),
                    rel.group("label") or "",
                    n,
                    rel.group("conn"),
                )
            )
            continue

        # Report relationship-like lines that were not parsed.
        if re.search(r"[-.]{2}", line):
            unparsed.append((n, line))

    return elements, relations, unparsed, "\n".join(note_lines)


def parse_domain_classes(text: str) -> dict[str, str]:
    """Return domain classes as {normalized_key: original_name}."""
    text = model_code(text)
    names: dict[str, str] = {}
    for line in text.splitlines():
        m = CLASS_RE.match(line.strip())
        if m:
            original = m.group("q") or m.group("p")
            names[key(original)] = original
    return names


# Validation.


def validate(text: str, domain_text: str | None = None):
    errors: list[str] = []
    warnings: list[str] = []

    stripped = text.strip()
    if not stripped.startswith("@startuml"):
        errors.append("source must start with @startuml")
    if not stripped.endswith("@enduml"):
        errors.append("source must end with @enduml")

    for directive in REQUIRED_DIRECTIVES:
        if directive not in text:
            warnings.append(f"missing recommended output directive: {directive}")

    elements, relations, unparsed, note_text = parse_diagram(text)

    if not elements:
        errors.append(
            "no actor/boundary/control/entity elements declared; "
            "a robustness diagram requires typed elements"
        )
        return errors, warnings, {}

    for n, line in unparsed:
        warnings.append(f"line {n}: relationship-like syntax could not be parsed: {line}")

    by_type: dict[str, list[Element]] = {t: [] for t in TYPES}
    for el in elements.values():
        by_type[el.etype].append(el)

    # Minimum structure.
    if not by_type["control"]:
        errors.append(
            "diagram has no controls; controls represent "
            "system behavior, so omitting them removes the behavioral content"
        )
    if not by_type["boundary"]:
        warnings.append("diagram has no boundaries; check how the actor interacts with the system")
    if not by_type["actor"]:
        warnings.append("diagram declares no actors")
    if not by_type["entity"]:
        warnings.append(
            "diagram has no entities; add them if the use case manipulates domain concepts"
        )

    # Alias contract.
    for el in elements.values():
        expected = ALIAS_PREFIX[el.etype]
        if not el.alias.startswith(expected):
            warnings.append(
                f"line {el.line}: alias '{el.alias}' for {el.etype} should start with '{expected}' "
                "(the prefix makes traceability unambiguous)"
            )
        for other_type, prefix in ALIAS_PREFIX.items():
            if other_type != el.etype and el.alias.startswith(prefix):
                errors.append(
                    f"line {el.line}: '{el.alias}' is declared as {el.etype}, but its alias "
                    f"indicates {other_type}; correct the declaration or alias"
                )

    # Hard connection rules.
    seen_pairs: set[tuple[str, str, str]] = set()
    control_control_edges = 0
    directed_lines: list[int] = []
    for left, right, label, n, conn in relations:
        if ">" in conn or "<" in conn:
            directed_lines.append(n)
        el_l, el_r = elements.get(left), elements.get(right)
        if el_l is None or el_r is None:
            missing = left if el_l is None else right
            warnings.append(f"line {n}: relationship references undeclared alias '{missing}'")
            continue

        pair = frozenset({el_l.etype, el_r.etype})
        if pair in INVALID_PAIRS:
            errors.append(
                f"line {n}: {el_l.etype} '{el_l.display}' -- {el_r.etype} '{el_r.display}': "
                f"{INVALID_PAIRS[pair]}"
            )
        elif pair not in VALID_PAIRS:
            warnings.append(f"line {n}: unrecognized relationship between {el_l.etype} and {el_r.etype}")

        # Distinct labels permit multiple edges between the same objects.
        ordered = tuple(sorted((left, right))) + (norm(label),)
        if ordered in seen_pairs:
            warnings.append(
                f"line {n}: duplicate relationship between '{el_l.display}' and '{el_r.display}'"
                + (f" with the same label '{label}'" if label else " without a label")
            )
        seen_pairs.add(ordered)

        if pair == frozenset({"control"}):
            control_control_edges += 1

    # Direction is semantically immaterial; warn only for notation consistency.
    if directed_lines:
        muestra = ", ".join(str(x) for x in directed_lines[:5])
        resto = "..." if len(directed_lines) > 5 else ""
        warnings.append(
            f"lines {muestra}{resto}: directed arrows used. Robustness edges "
            "are communication associations without directional semantics "
            "(sequence diagrams establish temporal order); use '--' consistently"
        )

    # God control: excessive concentration of behavior.
    degree: dict[str, int] = {}
    for l, r, _, _, _ in relations:
        degree[l] = degree.get(l, 0) + 1
        degree[r] = degree.get(r, 0) + 1

    for c in by_type["control"]:
        grado = degree.get(c.alias, 0)
        if grado > GOD_CONTROLLER_DEGREE:
            warnings.append(
                f"line {c.line}: control '{c.display}' has {grado} connections; "
                "check whether it absorbs responsibilities belonging to other controls"
            )

    # Control clusters are legal but warrant a distribution review.
    if control_control_edges >= CONTROL_CHAIN_HINT:
        warnings.append(
            f"there are {control_control_edges} control-to-control connections; these are valid, "
            "but a cluster may indicate undistributed logic or a candidate manager class"
        )

    # Every alternative/exception declared in attached text must be represented.
    declarados = flujos_declarados(note_text)
    if declarados:
        blob = " ".join(
            [lab for _, _, lab, _, _ in relations] + [e.display for e in elements.values()]
        )
        dibujados = flujos_declarados(blob)
        for flujo in sorted(declarados - dibujados):
            warnings.append(
                f"flow coverage: use case text declares {flujo}, but it is absent "
                "from the diagram; include alternatives with the basic course"
            )

    # Color alternative-only objects as a readability recommendation.
    etiquetas_por_alias: dict[str, list[str]] = {}
    for l, r, lab, _, _ in relations:
        for alias in (l, r):
            if alias in elements:
                etiquetas_por_alias.setdefault(alias, []).append(lab)

    marca_flujo = FLUJO_RE
    for alias, labs in etiquetas_por_alias.items():
        el = elements[alias]
        if el.etype == "actor" or el.color:
            continue
        # Shared basic/alternative objects remain uncolored.
        if labs and all(marca_flujo.search(lab or "") for lab in labs):
            warnings.append(
                f"line {el.line}: '{el.display}' participates only in alternatives but is "
                "uncolored; use a distinct fill (e.g. #LightCoral) to show the "
                "difference between basic and alternative flows"
            )

    # Connectivity.
    connected = {a for left, right, _, _, _ in relations for a in (left, right)}
    for el in elements.values():
        if el.alias not in connected:
            warnings.append(
                f"line {el.line}: '{el.display}' ({el.etype}) has no relationships; "
                "connect or remove it"
            )

    for actor in by_type["actor"]:
        targets = [
            elements[r if l == actor.alias else l].etype
            for l, r, _, _, _ in relations
            if actor.alias in (l, r) and elements.get(l) and elements.get(r)
        ]
        if targets and "boundary" not in targets:
            warnings.append(
                f"actor '{actor.display}' has no boundary connection; "
                "actors interact with the system through an interface"
            )

    # Naming heuristics.
    for b in by_type["boundary"]:
        name = norm(b.display)
        if name in GENERIC_BOUNDARY or name.rstrip("s") in GENERIC_BOUNDARY:
            warnings.append(
                f"line {b.line}: boundary '{b.display}' has a generic name; "
                "use the actual screen name"
            )
        for t in TECH_TERMS:
            if re.search(rf"\b{re.escape(t)}\b", name):
                warnings.append(
                    f"line {b.line}: boundary '{b.display}' names a technology ('{t}'); "
                    "keep this at conceptual design level"
                )
                break
        for w in WIDGET_TERMS:
            if re.search(rf"\b{re.escape(w)}\b", name):
                warnings.append(
                    f"line {b.line}: boundary '{b.display}' appears to be a widget ('{w}'); "
                    "boundaries represent whole screens or pages"
                )
                break

    for c in by_type["control"]:
        name = norm(c.display)
        if name in GENERIC_CONTROLLER:
            warnings.append(
                f"line {c.line}: control '{c.display}' is too generic; "
                "name the specific function it represents"
            )
        for nn in NOUNY_CONTROLLER:
            # A leading noun is suspicious; an action followed by that noun is valid.
            if re.match(rf"^{re.escape(nn)}\b", name):
                warnings.append(
                    f"line {c.line}: control '{c.display}' begins with a noun ('{nn}'); "
                    "a control represents a verb; put the action first "
                    "(e.g. 'Show {nn}...')".replace("{nn}", nn)
                )
                break

    for e in by_type["entity"]:
        for t in TECH_TERMS:
            if re.search(rf"\b{re.escape(t)}\b", norm(e.display)):
                warnings.append(
                    f"line {e.line}: entity '{e.display}' names a technology ('{t}'); "
                    "entities represent domain concepts"
                )
                break

    # Size.
    if len(elements) > MAX_ELEMENTS_HINT:
        warnings.append(
            f"diagram has {len(elements)} elements; if alternatives have "
            "subordinate alternatives, consider splitting the use case"
        )

    # Object discovery against the domain model.
    discovery: dict[str, list[str]] = {}
    if domain_text is not None:
        domain = parse_domain_classes(domain_text)
        if not domain:
            warnings.append("no classes recognized in the supplied domain model")
        else:
            missing = [e.display for e in by_type["entity"] if key(e.display) not in domain]
            if missing:
                discovery["nuevas"] = missing
                for name in missing:
                    warnings.append(
                        f"object discovery: entity '{name}' is absent from the domain model; "
                        "include it in the discovery delta"
                    )
            used = {key(e.display) for e in by_type["entity"]}
            discovery["no_usadas"] = sorted(orig for k, orig in domain.items() if k not in used)

    stats = {
        "elementos": len(elements),
        "actores": len(by_type["actor"]),
        "boundary": len(by_type["boundary"]),
        "control": len(by_type["control"]),
        "entity": len(by_type["entity"]),
        "relaciones": len(relations),
        "object_discovery": discovery,
    }
    return errors, warnings, stats


def main(argv: list[str]) -> int:
    # UTF-8 output keeps accented domain names readable on Windows consoles.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Validate an MKL robustness diagram in PlantUML.")
    ap.add_argument("path", help="path to the robustness .puml file")
    ap.add_argument("--domain", help="path to the domain model .puml file (enables object-discovery checks)")
    args = ap.parse_args(argv[1:])

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot read UTF-8 input {path}: {exc}")
        return 2

    domain_text = None
    if args.domain:
        dpath = Path(args.domain)
        if not dpath.exists():
            print(f"ERROR: domain model not found: {dpath}")
            return 2
        try:
            domain_text = dpath.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: cannot read UTF-8 domain input {dpath}: {exc}")
            return 2

    errors, warnings, stats = validate(text, domain_text)

    print("Robustness diagram validation")
    print("==================================")
    if stats:
        print(
            f"\nElements: {stats['elementos']} "
            f"(actors {stats['actores']}, boundary {stats['boundary']}, "
            f"control {stats['control']}, entity {stats['entity']}) | "
            f"relationships: {stats['relaciones']}"
        )

    print("\nERRORS:" if errors else "\nERRORS: none")
    for e in errors:
        print(f"- {e}")

    print("\nWARNINGS:" if warnings else "\nWARNINGS: none")
    for w in warnings:
        print(f"- {w}")

    disc = stats.get("object_discovery") if stats else None
    if disc:
        if disc.get("nuevas"):
            print("\nOBJECT DISCOVERY - entities absent from the domain model:")
            for name in disc["nuevas"]:
                print(f"- {name}")
        if disc.get("no_usadas"):
            print("\nDomain classes unused by this use case (informational):")
            print("- " + ", ".join(disc["no_usadas"]))

    print(
        "\nErrors identify deterministic robustness-rule violations; "
        "warnings require analyst judgment."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
