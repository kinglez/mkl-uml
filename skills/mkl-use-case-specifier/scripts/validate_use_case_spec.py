#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Validate textual use case specifications in Markdown.

Check mechanically verifiable properties: minimum fields, well-formed and unique
identifiers, resolving cross-references, and writing risks such as ambiguous
vocabulary, passive/impersonal voice, implementation details, and unresolved flows.

This does not judge the domain or replace analyst review: an ERROR is a verifiable
structural defect; a WARNING is a risk requiring judgment.

Both the lean summary form (with numbered basic-flow steps) and the full template
are supported. Sections absent from the lean form are not required. Structural fields support English,
legacy Spanish and Chinese. Writing-risk lexicons cover English/Spanish only;
Python names and statistics keys remain stable for compatibility.

Usage:
    python validate_use_case_spec.py specification.md

Exit codes: 0 = no errors, 1 = errors, 2 = usage/reading problem.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# --- Configuration --------------------------------------------------------

ID_PREFIXES = ("CU", "RF", "RN", "RE", "PRE", "FA", "FE", "CA", "OBJ", "CP", "DR", "DS")

# References with these prefixes must resolve within this document.
# RF/OBJ/CP/DR/DS may live in other artifacts, so local resolution is not required.
MUST_RESOLVE = ("RN", "FA", "FE", "PRE", "RE", "CA")

CAMPOS_MINIMOS = {
    "primary actor": r"primary\s+actor|actor\s+(primario|principal)|主(?:要)?参与者",
    "trigger": r"disparador|trigger|evento\s+inicial|initial\s+event|触发",
    "preconditions": r"precondici|preconditions?|前置条件",
    "basic flow": r"(flujo|curso)\s+(basico|principal)|escenario\s+soleado|(?:basic|main)\s+(?:flow|course)|sunny.day\s+scenario|基本流程|主流程",
    "postconditions": r"postcondici|postconditions?|后置条件",
    "acceptance criteria": r"criterios?\s+de\s+aceptacion|acceptance\s+criteri(?:a|on)|验收(?:标准|条件)",
}

LEXICO_AMBIGUO = (
    "los datos", "la informacion", "la pantalla", "el formulario",
    "los campos", "el mensaje", "las opciones",
    "the data", "the information", "the screen", "the form",
    "the fields", "the message", "the options",
)

IMPERSONAL = (
    r"\bse\s+(guarda|guardan|muestra|muestran|valida|validan|registra|registran|envia|envian|genera|generan|actualiza|actualizan|procesa|procesan|almacena|almacenan|calcula|calculan)\b"
    r"|\b(?:is|are)\s+(?:saved|displayed|validated|registered|sent|generated|updated|processed|stored|calculated)\b"
)

# A bare "endpoint" is intentionally excluded. The template permits a "visible
# endpoint" as an actor-observable interaction point. Technical REST/API endpoints
# do not belong in the specification. Use only unambiguously technical terms;
# legitimate domain concepts such as "rate table", "Institutional Repository",
# and "Traffic Controller" are excluded to avoid false positives of the kind
# previously encountered with the named "Request Form".
IMPLEMENTACION = (
    "sql", "base de datos", "tabla de la base de datos", "framework",
    "api rest", "endpoint rest", "dropdown", "combobox", "json", "xml",
    "servlet", "jsp", "clase java", "microservicio", "stored procedure",
    "database", "database table", "rest api", "rest endpoint", "java class", "microservice",
)

# Methodological guidance discusses these terms rather than using them in a flow.
META = r"\b(evitar|evita|no\s+usar|no\s+incluir|no\s+mezclar|prohibid|regla|deberia|no\s+debe|avoid|do\s+not\s+(?:use|include|mix)|forbidden|rule|should|must\s+not)\b"

MAX_PASOS_FLUJO = 15   # Documented trap: longer flows may contain several scenarios.


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


def norm(text: str) -> str:
    return strip_accents(text).lower()


# --- Supported Markdown evidence -----------------------------------------

_MARKER_RE = re.compile(r"(?<!\\)\[([^\]\n]+)\](?![ \t]*(?:\(|\[|:))")
_ID_PATTERN = "(?:" + "|".join(ID_PREFIXES) + ")-\\d+"
_ID_REFERENCE_RE = re.compile(r"\b(" + _ID_PATTERN + r")(?!\.\d)\b")
_ID_ITEM_RE = re.compile(r"^(" + _ID_PATTERN + r")(?P<substep>(?:\.\d+)*)(?!\w|\.\d)")


class _SpecificationEvidence:
    """One local interpretation of the supported specification forms.

    Fields, steps, IDs, flow bodies and writing-risk hints all consume these
    eligible lines. Fenced examples and HTML comments cannot become evidence.
    This is a small profile reader, not a Markdown renderer.
    """

    def __init__(self, source: str):
        self.lines = self._eligible_lines(source)
        self.text = "\n".join(self.lines)
        self.headings = {i: h for i, line in enumerate(self.lines)
                         if (h := self._heading(line)) is not None}
        self.ends: dict[int, int] = {}
        stack: list[int] = []
        for index, (level, _) in self.headings.items():
            while stack and self.headings[stack[-1]][0] >= level:
                self.ends[stack.pop()] = index
            stack.append(index)
        self.ends.update({index: len(self.lines) for index in stack})
        self.markers, self.template_warning = self._template_markers()
        self.placeholders = [match.group(0) for match in self._markers(self.text)]
        self.items = {i: item for i in range(len(self.lines))
                      if (item := self._identifier_item(i)) is not None}
        self.definitions = {prefix: {} for prefix in ID_PREFIXES}
        self.references = {prefix: set() for prefix in ID_PREFIXES}
        self.flows: dict[str, list[str]] = {}
        self._read_identifiers_and_flows()
        self.fields = {name: [] for name in CAMPOS_MINIMOS}
        self._read_fields()
        self.basic_steps = sum(self._step_count(value) for value in self.fields["basic flow"])

    @staticmethod
    def _eligible_lines(source: str) -> list[str]:
        lines, fence, in_comment = [], None, False
        for raw in source.splitlines():
            if fence:
                if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}[ \t]*", raw):
                    fence = None
                lines.append("")
                continue
            if not in_comment:
                opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", raw)
                if opening and not (opening[1][0] == "`" and "`" in opening[2]):
                    fence = (opening[1][0], len(opening[1]))
                    lines.append("")
                    continue
            # Comments are interpreted outside fences: '<!--' in a fenced
            # example must not hide real text following that example.
            visible, cursor = [], 0
            while cursor < len(raw):
                delimiter = "-->" if in_comment else "<!--"
                found = raw.find(delimiter, cursor)
                if found < 0:
                    visible.append(" " * (len(raw) - cursor) if in_comment else raw[cursor:])
                    break
                visible.append(" " * (found - cursor) if in_comment else raw[cursor:found])
                visible.append(" " * len(delimiter))
                cursor, in_comment = found + len(delimiter), not in_comment
            lines.append("".join(visible))
        return lines

    @staticmethod
    def _heading(line: str) -> tuple[int, str] | None:
        match = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line)
        if not match:
            return None
        return len(match[1]), re.sub(r"[ \t]+#+[ \t]*$", "", match[2]).strip()

    @staticmethod
    def _template_markers() -> tuple[set[str], str | None]:
        # The distributed template owns its vocabulary. New template fields do
        # not require a parallel handwritten list in this checker.
        path = Path(__file__).resolve().parents[1] / "references/use-case-specification-template.md"
        try:
            template = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return {"actor", "primary actor", "use case name"}, (
                "template vocabulary unavailable; placeholder checks are partial")
        return {norm(match[1]) for match in _MARKER_RE.finditer(template)}, None

    def _markers(self, text: str):
        return (match for match in _MARKER_RE.finditer(text) if self._is_placeholder(match[1]))

    def _is_placeholder(self, token: str) -> bool:
        normalized = norm(token)
        return (normalized in self.markers or normalized == "actor primario"
                or normalized.startswith("nombre del ")
                or bool(re.fullmatch(r"[A-Z]{2,4}-XX|[A-Za-z ]+ name", token, re.I)))

    def has_content(self, value: str) -> bool:
        lines = value.splitlines()
        for index, raw in enumerate(lines):
            if self._heading(raw) or re.fullmatch(r"[\s|:\-]+", raw):
                continue
            if index + 1 < len(lines) and "|" in raw and re.fullmatch(r"[\s|:\-]+", lines[index + 1]):
                continue
            raw = _MARKER_RE.sub(lambda m: " " if self._is_placeholder(m[1]) else m[0], raw)
            raw = re.sub(r"^\s*\d+[.)]\s*", "", raw)
            raw = re.sub(r"^(?:\|\s*)?(?:\*\*)?" + _ID_PATTERN + r"(?:\.\d+)*\b\s*[:|]?", "", raw.strip())
            content = re.sub(r"[*`|\[\]\s:：.\-]", "", raw).lower()
            if content and not content.isdigit() and content not in {"tbd", "todo", "xx", "待补充", "待填写"}:
                return True
        return False

    def _identifier_item(self, index: int) -> tuple[str, bool] | None:
        line = self.headings[index][1] if index in self.headings else self.lines[index].strip()
        if index in self.headings:
            line = re.sub(r"^\d+[.)]\s*", "", line)
        if line.startswith("|"):
            line = line.strip("|").split("|")[0].strip()
        line = re.sub(r"[*`]", "", line).strip()
        match = _ID_ITEM_RE.match(line)
        return (match[1], bool(match["substep"])) if match else None

    def _read_identifiers_and_flows(self):
        for ident in _ID_REFERENCE_RE.findall(self.text):
            self.references[ident.split("-", 1)[0]].add(ident)
        for index, (ident, substep) in self.items.items():
            prefix = ident.split("-", 1)[0]
            if not substep:
                counts = self.definitions[prefix]
                counts[ident] = counts.get(ident, 0) + 1
            if prefix not in ("FA", "FE"):
                continue
            context = self.flows.setdefault(ident, [])
            context.append(self.lines[index])
            if substep or self.lines[index].lstrip().startswith("|"):
                continue
            end = self.ends.get(index, len(self.lines))
            for following in range(index + 1, end):
                item = self.items.get(following)
                if item and not item[1] and item[0].startswith(("FA-", "FE-")):
                    break
                if index not in self.headings and following in self.headings:
                    break
                context.append(self.lines[following])

    def _read_fields(self):
        labels = {name: re.compile(r"^(?:\d+[.)]\s*)?(?:success\s+|failure\s+)?(?:" + pattern
                                  + r")\w*\s*(?::|：|/|$)") for name, pattern in CAMPOS_MINIMOS.items()}
        headers: dict[int, tuple[str, str | None]] = {}
        for index, raw in enumerate(self.lines):
            text = self.headings[index][1] if index in self.headings else raw.strip()
            text = re.sub(r"[*`]", "", text)
            table = text.startswith("|")
            cells = text.strip("|").split("|") if table else [text]
            for name, pattern in labels.items():
                if pattern.match(norm(cells[0].strip())):
                    if table:
                        value = " | ".join(cells[1:])
                    else:
                        parts = re.split(r"[:：]", text, maxsplit=1)
                        value = parts[1] if len(parts) == 2 and parts[1].strip() else None
                    headers[index] = name, value
                    break
        for index, (name, value) in headers.items():
            if value is None:
                end = self.ends.get(index, len(self.lines))
                for following in range(index + 1, end):
                    if following in headers or (index not in self.headings and following in self.headings):
                        end = following
                        break
                value = "\n".join(self.lines[index + 1:end])
            self.fields[name].append(value)

    def _step_count(self, value: str) -> int:
        count = 0
        for raw in value.splitlines():
            line = raw.strip()
            if self._heading(raw):
                continue
            if re.match(r"^\|\s*\d+\s*\|", line):
                bodies = [" | ".join(line.strip("|").split("|")[1:])]
            elif re.match(r"^\d+[.)][ \t]+", line):
                starts = list(re.finditer(r"(?:^|[ \t])\d+[.)][ \t]+", line))
                bodies = [line[m.end():starts[i + 1].start() if i + 1 < len(starts) else len(line)]
                          for i, m in enumerate(starts)]
            else:
                continue
            count += sum(self.has_content(body) and not any(self._markers(body)) for body in bodies)
        return count


# --- Validation -----------------------------------------------------------


def validate(text: str):
    evidence = _SpecificationEvidence(text)
    text = evidence.text
    errores: list[str] = []
    avisos: list[str] = []
    # -- Minimum fields
    for etiqueta in CAMPOS_MINIMOS:
        values = evidence.fields[etiqueta]
        if not values:
            if etiqueta == "acceptance criteria":
                avisos.append(
                    "no acceptance criteria found; without them the specification "
                    "is not verifiable and tests cannot be derived"
                )
            else:
                errores.append(f"missing minimum specification field: {etiqueta}")
        elif not any(evidence.has_content(value) for value in values):
            errores.append(f"empty minimum specification field: {etiqueta}")

    # -- Unfilled template markers, including legacy Spanish markers
    placeholders = evidence.placeholders
    if evidence.template_warning:
        avisos.append(evidence.template_warning)
    if placeholders:
        avisos.append(
            f"{len(placeholders)} unfilled template markers remain "
            f"(e.g., {placeholders[0]}); a partially completed template is not a specification"
        )

    # -- Identifier format, duplicates, and dangling references
    todos_definidos: dict[str, dict[str, int]] = {}
    for prefix in ID_PREFIXES:
        definidos, referenciados = evidence.definitions[prefix], evidence.references[prefix]
        todos_definidos[prefix] = definidos

        for ident, veces in definidos.items():
            if veces > 1:
                errores.append(
                    f"identifier {ident} is defined {veces} times; "
                    "each item needs a unique label for traceability"
                )

        if prefix in MUST_RESOLVE:
            colgantes = sorted(referenciados - set(definidos))
            for ident in colgantes:
                errores.append(
                    f"{ident} is referenced but not defined in the document; "
                    "every cross-reference must resolve"
                )

    # -- Malformed identifiers, e.g., RN1, FA_02, CU 03
    malformados = set(re.findall(r"\b(?:" + "|".join(ID_PREFIXES) + r")[\s_]?\d+\b", text))
    malformados = {m for m in malformados if not re.match(r"^[A-Z]{2,4}-\d+$", m)}
    for m in sorted(malformados):
        avisos.append(f"irregular identifier format: '{m}'; the package convention is PREFIX-NN")

    # -- Basic-flow length
    basic_values = evidence.fields["basic flow"]
    pasos = evidence.basic_steps
    if pasos == 0 and any(evidence.has_content(value) for value in basic_values):
        errores.append("basic flow must contain at least one numbered step with content")
    if pasos > MAX_PASOS_FLUJO:
        avisos.append(
            f"the basic flow has {pasos} steps (threshold {MAX_PASOS_FLUJO}); "
            "confirm that it describes one scenario rather than several use cases"
        )

    # -- Alternate flows without an outcome
    for prefix in ("FA", "FE"):
        definidos = evidence.definitions[prefix]
        for ident in sorted(definidos):
            contexto = "\n".join(evidence.flows.get(ident, []))
            if not re.search(r"\b(?:retorna|vuelve|finaliza|termina|continua|cancela|reanuda|returns?|ends?|terminates?|continues?|cancels?|resumes?)\b|返回|结束|终止|继续|取消|恢复", norm(contexto)):
                avisos.append(
                    f"flow {ident} has no declared outcome (return to step N, termination, or cancellation); "
                    "an alternate flow without an exit is incomplete"
                )

    # -- Writing risks, excluding methodological guidance lines
    ambiguos: set[str] = set()
    impersonales = 0
    implementacion: set[str] = set()

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        n = norm(line)
        if re.search(META, n):
            continue
        # Compare unaccented text while PRESERVING case so indices remain aligned
        # and a capitalized domain qualifier can disambiguate a generic term.
        plano_linea = strip_accents(line)
        bajo = plano_linea.lower()
        for frase in LEXICO_AMBIGUO:
            for m in re.finditer(rf"\b{re.escape(frase)}\b", bajo):
                cola = plano_linea[m.end() : m.end() + 30]
                # "the Form for Request" and "the Screen Main" are explicitly
                # qualified, like legacy Spanish "el Formulario de Solicitud".
                # Natural English names such as "the Request Form" are already
                # outside the generic-phrase match.
                if re.match(r"\s+(?:(?:de|of|for)\s+)?[A-Z]", cola):
                    continue
                ambiguos.add(frase)
        if re.search(IMPERSONAL, n):
            impersonales += 1
        for termino in IMPLEMENTACION:
            if re.search(rf"\b{re.escape(termino)}\b", n):
                implementacion.add(termino)

    if ambiguos:
        avisos.append(
            "ambiguous vocabulary: " + ", ".join(f"'{a}'" for a in sorted(ambiguos))
            + ". Name the domain concept rather than using a generic term"
        )
    if impersonales:
        avisos.append(
            f"{impersonales} step(s) use passive/impersonal voice ('is saved', 'is displayed'); "
            "state who does what: the actor acts and the system responds"
        )
    if implementacion:
        avisos.append(
            "implementation detail in the specification: "
            + ", ".join(f"'{t}'" for t in sorted(implementacion))
            + ". A use case describes observable behavior rather than how the system is built"
        )

    stats = {
        "ids_definidos": {p: len(d) for p, d in todos_definidos.items() if d},
        "pasos_flujo_basico": pasos,
    }
    return errores, avisos, stats


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Validate a textual use case specification.")
    ap.add_argument("path", help="path to the specification .md file")
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
    errores, avisos, stats = validate(text)

    print("Use case specification validation")
    print("=================================")
    if stats.get("ids_definidos"):
        resumen = ", ".join(f"{p}:{n}" for p, n in sorted(stats["ids_definidos"].items()))
        print(f"\nDefined identifiers: {resumen}")
    print(f"Basic-flow steps: {stats.get('pasos_flujo_basico', 0)}")
    print("Language coverage: fields/IDs/outcome keywords support English, Spanish and Chinese; "
          "writing-risk hints cover English/Spanish only.")

    print("\nERRORS:" if errores else "\nERRORS: none")
    for e in errores:
        print(f"- {e}")

    print("\nWARNINGS:" if avisos else "\nWARNINGS: none")
    for a in avisos:
        print(f"- {a}")

    print(
        "\nErrors are verifiable structural defects; "
        "warnings require analyst judgment."
    )
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
