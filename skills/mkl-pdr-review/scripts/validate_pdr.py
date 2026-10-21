#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
# Modification notice: missing review evidence withholds provisional acceptance.
"""Validator of the Preliminary Design Review (PDR) of the MKL process.

Unlike sibling validators, which check ONE file, this one checks the
SET: domain model + use case diagram(s) + textual specification(s) + robustness diagram(s). Almost all the defects that the PDR looks for
occur BETWEEN artifacts, not inside one.

Each check is tied to one of the ten PDR guidelines. See
references/cross-artifact-checks.md for the complete mapping and limits of each
check.

Usage:
    python validate_pdr.py --robustez case_03_robustez.puml \
                           --spec case_03_specification.md \
                           --dominio domain_model.puml \
                           [--casos-uso use_cases.puml]

The --robustez and --spec flags support repetition to check an entire package.

Exit codes:
    0 no errors (warnings may occur)
    1 there are errors: the package does not pass
    2 usage error or file not found
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

TYPES = ("actor", "boundary", "control", "entity")

# Robustness analysis connection rules. Defined by
# /mkl-uml-robustness-diagram; here they are consumed and counted (guideline #5).
VALID_PAIRS = {
    frozenset({"actor", "boundary"}),
    frozenset({"boundary", "control"}),
    frozenset({"control"}),
    frozenset({"control", "entity"}),
}
INVALID_PAIRS = {
    frozenset({"actor", "control"}): "the actor only communicates with Boundary objects",
    frozenset({"actor", "entity"}): "the actor only communicates with Boundary objects",
    frozenset({"boundary", "entity"}): "must go through a Controller (missing verb)",
    frozenset({"entity"}): "must go through a Controller (missing verb)",
    frozenset({"boundary"}): "must go through a Controller (missing verb)",
    frozenset({"actor"}): "The diagram models the interaction with the system, not between actors.",
}

# Guideline #2 / step 5: design-pattern-itis. Only unambiguous terms of space
# of the solution. They are compared as a complete word, never as a single substring:
# The lesson already paid is that "Show payment form" is not a noun
# for containing "form".
PATTERN_TERMS = (
    "factory", "singleton", "strategy", "proxy", "observer", "adapter",
    "decorator", "facade", "builder", "visitor", "dao", "repository",
    "impl", "handler", "servlet", "controller bean", "dto", "orm",
)

# Guideline #2: Signs that the "robustness diagram" is actually one of
# sequence. See anti-patterns #10.
SEQUENCE_FRAGMENTS = re.compile(
    r"^\s*(alt|else|opt|loop|par|critical|break|group|activate|deactivate|"
    r"autonumber|participant|deactivate)\b",
    re.IGNORECASE | re.MULTILINE,
)
CALL_SIGNATURE = re.compile(r"\b[a-zA-Z_][\w]*\s*\([^)]*\)")
DIRECTED_ARROW = re.compile(r"(-+>|<-+|->>|<<-)")

# Guideline #3: screens without their own name.
GENERIC_BOUNDARY = (
    "pantalla", "pagina", "página", "formulario", "ventana", "vista",
    "interfaz", "screen", "page", "form", "window", "ui",
)

# Normalization of flow identifiers: FA-01, FA1, FA 1, fa_01 are the same.
FLUJO_RE = re.compile(r"\b(FA|FE)\s*[-_ ]?\s*0*(\d+)\b", re.IGNORECASE)

# PlantUML declarations in robustness diagrams.
DECL_RE = re.compile(
    r'^\s*(?P<type>actor|boundary|control|entity)\s+'
    r'(?:"(?P<label>[^"]+)"|(?P<bare>[\w]+))'
    r'(?:\s+as\s+(?P<alias>[\w]+))?'
    r'(?:\s+(?P<color>#[#\w]+))?\s*$',
    re.IGNORECASE | re.MULTILINE,
)
REL_RE = re.compile(
    r'^\s*(?P<left>"[^"]+"|[\w]+)\s*(?P<conn>[-.]{1,2}[->|]*)\s*'
    r'(?P<right>"[^"]+"|[\w]+)\s*(?::\s*(?P<label>.*))?$',
    re.MULTILINE,
)
CLASS_RE = re.compile(
    r'^\s*(?:abstract\s+)?class\s+(?:"(?P<q>[^"]+)"|(?P<n>[\w]+))', re.MULTILINE
)
# The type is OPTIONAL. /mkl-uml-domain-modeler prohibits type annotations in its
# strict academic mode ("no type annotations"), so a domain model
# correct according to the sister skill writes `placa`, not `placa : String`. Demand the
# type made ALL classes parse with zero attributes, silently, and
# fair for well-written models. Either way is accepted.
ATTR_RE = re.compile(
    r"^\s*[+#~-]?\s*(?P<name>[A-Za-zÁÉÍÓÚÑáéíóúñ_][\wÁÉÍÓÚÑáéíóúñ]*)"
    r"\s*(?::\s*[\w<>\[\], ]+)?\s*$",
    re.MULTILINE,
)

# Actors and use cases of the use case diagram.
UC_ACTOR_RE = re.compile(
    r'^\s*actor\s+(?:"(?P<label>[^"]+)"|(?P<bare>[\w]+))'
    r'(?:\s+as\s+(?P<alias>[\w]+))?', re.IGNORECASE | re.MULTILINE
)

STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "al",
    "y", "o", "en", "con", "por", "para", "que", "se", "su", "sus", "lo",
    "a", "the", "of", "to", "and", "or", "in", "on", "for", "is", "are",
    "sistema", "usuario", "datos", "informacion",
    "system", "user", "data", "information",
}

# Declared thresholds (see references/pdr-metrics.md).
#
# Two different thresholds, and the distinction matters:
# - COBERTURA_REINSPECCION: BELOW this the verdict is forced to
# Reinspection. It is a floor, not the acceptance criterion.
# - COBERTURA_ACEPTACION: for ACCEPTED, COMPLETE coverage is required, as
# It is documented by pdr-metrics.md.
# Before, only the 0.80 floor existed and the requirement for complete coverage was
# complied by side effect (any uncovered step generates a warning, and the
# warnings already push to the intermediate state). An invariant that depends on a
# foreign mechanism breaks at the first change of the foreign mechanism, so here
# is verified directly.
COBERTURA_REINSPECCION = 0.80
COBERTURA_ACEPTACION = 1.0
RITMO_PAGINAS_HORA = 3.5         # IEEE 1028 Sec 6.5.2, preliminary design: 3-4 pph
LINEAS_POR_PAGINA = 50           # declared equivalence to estimate volume
HORAS_SESION_RAZONABLE = 2.0     # Wiegers: the meeting should not exceed ~2 hours
SIMILITUD_DERIVA = 0.72          # threshold to propose a pair as vocabulary drift
RACHA_ACTOR_MAX = 3              # consecutive actor-subject steps before warning (guideline #6)


# --------------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------------

def strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def norm(text: str) -> str:
    return strip_accents(text or "").strip().lower()


def key(text: str) -> str:
    """Loose key to compare the same concept written in different ways.

    It is also used to INDEX (`out[key(name)] = (name, attrs)`), and there it leaves
    from being lax to becoming destructive: two names with the same key
    occupy the same entrance and the second step on the first, so that a
    entity disappears WITHOUT LEAVING A TRACE. The empty string is the key
    dangerous, because it collides with all the others. You reach it for two
    paths, and both are covered: the name is just stopwords (`El`, `Un`, and
    aliases `A`/`B` of the diagrams), or the character filter—which only
    preserve [a-z0-9]— entirely erases a name written in another alphabet.
    """
    t = norm(text)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    piezas = [w for w in t.split() if w]
    sin_stop = [w for w in piezas if w not in STOPWORDS]
    return "".join(sin_stop or piezas) or re.sub(r"\s+", "", norm(text))


def palabras(text: str) -> set[str]:
    t = re.sub(r"[^a-z0-9 ]+", " ", norm(text))
    return {w for w in t.split() if len(w) > 2 and w not in STOPWORDS}


def similitud(a: str, b: str) -> float:
    """Similarity by bigrams of characters. Without external dependencies."""
    a, b = key(a), key(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    ga = {a[i:i + 2] for i in range(len(a) - 1)}
    gb = {b[i:i + 2] for i in range(len(b) - 1)}
    if not ga or not gb:
        return 0.0
    return 2 * len(ga & gb) / (len(ga) + len(gb))


def flujos_declarados(text: str) -> set[str]:
    """Extracts flow identifiers normalized to the form FA-01 / FE-03."""
    return {
        f"{m.group(1).upper()}-{int(m.group(2)):02d}"
        for m in FLUJO_RE.finditer(text or "")
    }


def camel_split(text: str) -> str:
    """Separate CamelCase into words: 'DAOFactory Registry' -> 'DAO Factory Registry'.

    Essential before searching by full word. Without this, the check of
    design-pattern-itis remains MUTE in the pasted names, which are precisely
    those who need it most.
    """
    t = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text or "")
    t = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", t)
    return re.sub(r"[_\-.]+", " ", t)


def contiene_termino(nombre: str, terminos) -> str | None:
    """Returns the term found as a COMPLETE WORD, or None.

    By word and not by substring, because a check that marks 'Show form
    of payment' for containing 'form' is worse than not having it. But about him
    name with the CamelCase already separated, because otherwise the check never fires
    in 'DAOFactory Registry'. The two errors are symmetrical and both have been
    task: this helper exists so as not to repeat any.
    """
    n = norm(camel_split(nombre))
    for t in terminos:
        if re.search(rf"\b{re.escape(norm(t))}\b", n):
            return t
    return None


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class Element:
    alias: str
    label: str
    etype: str
    line: int

    @property
    def display(self) -> str:
        return self.label or self.alias


@dataclass
class Robustez:
    path: str
    text: str
    elements: dict = field(default_factory=dict)
    relations: list = field(default_factory=list)
    note_text: str = ""


@dataclass
class Spec:
    path: str
    text: str
    pasos: list = field(default_factory=list)      # (number, text, section)
    flujos: dict = field(default_factory=dict)     # FA-01 -> text block
    cu_id: str = ""


# --------------------------------------------------------------------------
# Parsers
# --------------------------------------------------------------------------

def parse_robustez(path: str, text: str) -> Robustez:
    r = Robustez(path=path, text=text)
    lines = text.split("\n")

    # Isolate note/legend blocks: their contents are not relations, but their text
    # It serves to cover flows.
    in_note = False
    cuerpo, notas = [], []
    for ln in lines:
        s = ln.strip().lower()
        if re.match(r"^(note|legend)\b", s) and not s.startswith("note over") is None:
            pass
        if re.match(r"^(note|legend)\b", s):
            in_note = True
            notas.append(ln)
            continue
        if in_note:
            notas.append(ln)
            if re.match(r"^end\s*(note|legend)\b", s) or s == "endnote" or s == "endlegend":
                in_note = False
            continue
        cuerpo.append(ln)
    r.note_text = "\n".join(notas)
    cuerpo_txt = "\n".join(cuerpo)

    for m in DECL_RE.finditer(cuerpo_txt):
        label = m.group("label") or m.group("bare") or ""
        alias = m.group("alias") or m.group("bare") or label
        line = cuerpo_txt[: m.start()].count("\n") + 1
        r.elements[alias] = Element(alias, label, m.group("type").lower(), line)

    for m in REL_RE.finditer(cuerpo_txt):
        left = m.group("left").strip('"')
        right = m.group("right").strip('"')
        if left.lower() in ("startuml", "enduml"):
            continue
        line = cuerpo_txt[: m.start()].count("\n") + 1
        r.relations.append(
            (left, right, (m.group("label") or "").strip(), line, m.group("conn"))
        )
    return r


def parse_dominio(text: str) -> dict:
    """Returns {clave: (nombre_original, {atributos})}."""
    out = {}
    for m in CLASS_RE.finditer(text):
        name = m.group("q") or m.group("n")
        # Class body, if any
        rest = text[m.end():]
        attrs = set()
        if rest.lstrip().startswith("{"):
            depth, buf, started = 0, [], False
            for ch in rest:
                if ch == "{":
                    depth += 1
                    started = True
                    continue
                if ch == "}":
                    depth -= 1
                    if depth == 0:
                        break
                    continue
                if started:
                    buf.append(ch)
            body = "".join(buf)
            attrs = {norm(a.group("name")) for a in ATTR_RE.finditer(body)}
        out[key(name)] = (name, attrs)
    return out


def parse_casos_uso(text: str) -> set[str]:
    actores = set()
    for m in UC_ACTOR_RE.finditer(text):
        label = m.group("label") or m.group("bare") or ""
        if label:
            actores.add(key(label))
        if m.group("alias"):
            actores.add(key(m.group("alias")))
    return actores


def parse_spec(path: str, text: str) -> Spec:
    s = Spec(path=path, text=text)
    mid = re.search(r"\bCU-(\d+)\b", text)
    if mid:
        s.cu_id = f"CU-{int(mid.group(1)):02d}"

    # Numbered steps (markdown list or table).
    for m in re.finditer(r"^\s*(?:\|\s*)?(\d+)[.)]?\s*\|?\s*(.+?)\s*\|?\s*$",
                         text, re.MULTILINE):
        cuerpo = m.group(2).strip()
        if len(cuerpo) > 8 and not cuerpo.startswith("-"):
            s.pasos.append((int(m.group(1)), cuerpo))

    # Alternative / exception flow blocks: from their identifier to the
    # next identifier or header.
    marcas = [(m.start(), f"{m.group(1).upper()}-{int(m.group(2)):02d}")
              for m in FLUJO_RE.finditer(text)]
    for i, (pos, fid) in enumerate(marcas):
        fin = marcas[i + 1][0] if i + 1 < len(marcas) else len(text)
        bloque = text[pos:fin]
        # It keeps the longest block seen for that id (the definition, not
        # mere references).
        if len(bloque) > len(s.flujos.get(fid, "")):
            s.flujos[fid] = bloque
    return s


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_sintaxis_robustez(rob: Robustez, errores: list, avisos: list) -> int:
    """Guideline #5. Returns the number of syntax violations."""
    viol = 0
    tag = f"[{rob.path}]"

    for left, right, label, line, conn in rob.relations:
        le = rob.elements.get(left)
        re_ = rob.elements.get(right)
        if not le or not re_:
            continue
        par = frozenset({le.etype, re_.etype})
        if par in INVALID_PAIRS:
            viol += 1
            errores.append(
                f"{tag} L{line}: guideline #5 - banned link "
                f"{le.etype}<->{re_.etype} between '{le.display}' and '{re_.display}': "
                f"{INVALID_PAIRS[par]}"
            )
        elif par not in VALID_PAIRS:
            viol += 1
            errores.append(
                f"{tag} L{line}: guideline #5 - unrecognized pair "
                f"{le.etype}<->{re_.etype} between '{le.display}' and '{re_.display}'"
            )

    controles = [e for e in rob.elements.values() if e.etype == "control"]
    if rob.elements and not controles:
        viol += 1
        errores.append(
            f"{tag} guideline #5 - the diagram has no Controllers: without them no "
            f"there is system behavior represented"
        )
    return viol


def check_robustez_como_secuencia(rob: Robustez, errores: list) -> None:
    """Guideline #2 / anti-pattern 10."""
    tag = f"[{rob.path}]"
    senales = []

    frags = {m.group(1).lower() for m in SEQUENCE_FRAGMENTS.finditer(rob.text)}
    if frags:
        senales.append(f"sequence fragments ({', '.join(sorted(frags))})")

    firmas = [
        (l, r, lb, ln) for (l, r, lb, ln, _c) in rob.relations
        if lb and CALL_SIGNATURE.search(lb)
    ]
    if firmas:
        ejemplo = firmas[0][2][:48]
        senales.append(f"{len(firmas)} message(s) with method signature (e.g. '{ejemplo}')")

    if senales:
        errores.append(
            f"{tag} guideline #2 - this diagram looks like a SEQUENCE diagram, not a "
            f"robustness: {'; '.join(senales)}. The assignment of behavior between "
            f"classes belongs to the next stage."
        )


def check_pattern_itis(rob: Robustez, avisos: list) -> None:
    """Guideline #2 / step 5."""
    tag = f"[{rob.path}]"
    for e in rob.elements.values():
        if e.etype != "control":
            continue
        hit = contiene_termino(e.display, PATTERN_TERMS)
        if hit:
            avisos.append(
                f"{tag} L{e.line}: guideline #2 - Driver '{e.display}' uses "
                f"implementation vocabulary ('{hit}'). Use a semantic name "
                f"that a non-technical participant understands."
            )


def check_boundaries_genericos(rob: Robustez, avisos: list) -> None:
    """Guideline #3: screens have their own name."""
    tag = f"[{rob.path}]"
    for e in rob.elements.values():
        if e.etype != "boundary":
            continue
        n = norm(e.display)
        # Only if the name IS generic, not if it contains it: "Reservation Page"
        # It is a proper name; "page" simply, no.
        if n in [norm(g) for g in GENERIC_BOUNDARY]:
            avisos.append(
                f"{tag} L{e.line}: guideline #3 - Boundary object '{e.display}' does not "
                f"It has its own name. Find out what that screen is called."
            )


def check_entidades(robs: list, dominio: dict, errores: list, infos: list) -> tuple:
    """Guideline #9. Returns (n_no_domain, derived_candidate_list)."""
    usadas = {}
    for rob in robs:
        for e in rob.elements.values():
            if e.etype == "entity":
                usadas.setdefault(key(e.display), (e.display, rob.path, e.line))

    faltantes = []
    for k, (nombre, path, line) in sorted(usadas.items()):
        if k not in dominio:
            faltantes.append((k, nombre, path, line))
            errores.append(
                f"[{path}] L{line}: guideline #9 - entity '{nombre}' does not exist in the "
                f"domain model. The robustness analysis discovered it and no one found it. "
                f"returned to the model."
            )

    no_usadas = [orig for k, (orig, _a) in dominio.items() if k not in usadas]
    if no_usadas:
        infos.append(
            "Domain classes that this package does not use (information, not default): "
            + ", ".join(sorted(no_usadas))
        )

    # Vocabulary drift: a missing entity that closely resembles a class
    # existing is probably the same under another name.
    candidatas = []
    for k, nombre, path, line in faltantes:
        for dk, (dnombre, _at) in dominio.items():
            sim = similitud(k, dk)
            if sim >= SIMILITUD_DERIVA:
                candidatas.append((nombre, dnombre, sim, path, line))
    return len(faltantes), candidatas


def check_cobertura_flujos(rob: Robustez, spec: Spec, errores: list) -> int:
    """Guideline #7, first half: each FA/FE of the specification has a branch."""
    declarados = set(spec.flujos.keys())
    if not declarados:
        return 0
    etiquetas = " ".join(lb for (_l, _r, lb, _ln, _c) in rob.relations if lb)
    dibujados = flujos_declarados(etiquetas) | flujos_declarados(rob.note_text)
    sin_rama = sorted(declarados - dibujados)
    for fid in sin_rama:
        errores.append(
            f"[{rob.path}] guideline #7 - the flow {fid} is declared in "
            f"{spec.path} but has no branch in the diagram."
        )
    return len(sin_rama)


def check_alternos_sin_comportamiento(spec: Spec, errores: list) -> int:
    """Guideline #7, second half: listing is not specifying."""
    n = 0
    for fid, bloque in sorted(spec.flujos.items()):
        # Behavior = at least one step where the system does something.
        tiene_sistema = re.search(r"\b(?:el\s+sistema|the\s+system)\b|\b(?:sistema|system)\s+\w+", norm(bloque))
        tiene_pasos = len(re.findall(r"^\s*(?:\|\s*)?\d+[.)]", bloque, re.MULTILINE)) >= 1
        if not (tiene_sistema and tiene_pasos):
            n += 1
            errores.append(
                f"[{spec.path}] guideline #7 - flow {fid} is listed but does not "
                f"specify system behavior. Identifying that it can "
                f"occur is necessary, not sufficient."
            )
    return n


def check_dialogo(spec: Spec, errores: list, avisos: list) -> None:
    """Guideline #6: both sides of the user/system dialogue.

    The TOTAL absence of a system response is deterministic and is an error. one
    long streak is a heuristic clue and is a warning: distinction matters
    because the verdict is derived from the errors.
    """
    if not spec.pasos:
        return
    # Only the basic flow is judged here; alternate courses are checked separately (guideline #7).
    fin_basico = min((p for p in (spec.text.find("## Flujos"),
                                  spec.text.find("## Alternative flows"),
                                  spec.text.find("## Exception flows"),
                                  spec.text.find("### FA-"),
                                  spec.text.find("### FE-")) if p > 0), default=len(spec.text))
    basico = [(n, t) for n, t in spec.pasos if spec.text.find(t) < fin_basico]
    if not basico:
        basico = spec.pasos

    racha, peor, inicio = 0, 0, None
    hay_sistema = False
    for num, texto in basico:
        if re.search(r"\b(?:sistema|system)\b", norm(texto)):
            hay_sistema = True
            racha = 0
        else:
            racha += 1
            if racha > peor:
                peor, inicio = racha, num - racha + 1

    if not hay_sistema:
        errores.append(
            f"[{spec.path}] guideline #6 - no steps in the basic flow describe the "
            f"system response. A use case is a dialogue; if the system does not "
            f"respond in the text, its behavior is not specified anywhere "
            f"and will not reach the code."
        )
    elif peor > RACHA_ACTOR_MAX:
        avisos.append(
            f"[{spec.path}] guideline #6 - {peor} consecutive steps without a system response "
            f"(from step {inicio}). Check if it is necessary to say what the system does."
        )


def check_actores(robs: list, actores_cu: set, avisos: list) -> None:
    """Guidelines #5 and #3: the actors come from the use case diagram."""
    if not actores_cu:
        return
    for rob in robs:
        for e in rob.elements.values():
            if e.etype != "actor":
                continue
            if key(e.display) not in actores_cu:
                avisos.append(
                    f"[{rob.path}] L{e.line}: Actor '{e.display}' does not appear in the "
                    f"use case diagram. Either he's missing there, or he's not an actor."
                )


def check_cobertura_marcador(rob: Robustez, spec: Spec) -> tuple:
    """Guideline #10, approximate. Returns (covered, total, uncovered_steps)."""
    if not spec.pasos:
        return (0, 0, [])
    vocab = set()
    for e in rob.elements.values():
        vocab |= palabras(e.display)
    for (_l, _r, lb, _ln, _c) in rob.relations:
        vocab |= palabras(lb)

    cubiertos, sin_cubrir = 0, []
    for num, texto in spec.pasos:
        p = palabras(texto)
        if not p:
            continue
        if p & vocab:
            cubiertos += 1
        else:
            sin_cubrir.append((num, texto[:60]))
    return (cubiertos, len([1 for _n, t in spec.pasos if palabras(t)]), sin_cubrir)


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def leer(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        print(f"File does not exist: {path}", file=sys.stderr)
        raise SystemExit(2)


def emparejar(robs: list, specs: list) -> list:
    """Match each robustness diagram with its specification by CU-XX, and if
    There is no clue, by position."""
    pares = []
    usadas = set()
    for rob in robs:
        elegida = None
        ids_rob = set(re.findall(r"\bCU-(\d+)\b", rob.text))
        for sp in specs:
            if sp.cu_id and sp.cu_id in {f"CU-{int(i):02d}" for i in ids_rob}:
                elegida = sp
                break
        if elegida is None:
            for sp in specs:
                if id(sp) not in usadas:
                    elegida = sp
                    break
        if elegida is not None:
            usadas.add(id(elegida))
        pares.append((rob, elegida))
    return pares


def validar(robs, specs, dominio, actores_cu, hay_dominio, hay_spec, hay_cu):
    errores, avisos, infos = [], [], []
    metricas = {
        "cobertura_marcador": None,
        "entidades_sin_dominio": None,
        "alternos_sin_comportamiento": None,
        "violaciones_sintaxis": 0,
    }
    capas = {}

    # --- Guideline #5 and #2: by diagram ---
    viol = 0
    for rob in robs:
        viol += check_sintaxis_robustez(rob, errores, avisos)
        check_robustez_como_secuencia(rob, errores)
        check_pattern_itis(rob, avisos)
        check_boundaries_genericos(rob, avisos)
    metricas["violaciones_sintaxis"] = viol
    capas["#5 robustness syntax"] = "executed"
    capas["#2 do not refer to detailed design"] = "executed"

    # --- Guideline #9: entities in the domain ---
    if hay_dominio:
        n_falt, candidatas = check_entidades(robs, dominio, errores, infos)
        metricas["entidades_sin_dominio"] = n_falt
        capas["#9 entities in the domain"] = "executed"
        for nombre, dnombre, sim, path, line in candidatas:
            avisos.append(
                f"[{path}] L{line}: guideline #3 - possible vocabulary drift: "
                f"'{nombre}' looks like the '{dnombre}' class of the domain "
                f"(similarity {sim:.2f}). Please confirm if they are the same concept before "
                f"create a new class."
            )
        # Guideline #8: automatable half. Without a wireframe you cannot verify that a
        # screen field exists, but IF you can check the other end of
        # the chain: that the entities where the data should land have
        # declared attributes. An entity without any attributes cannot receive
        # nothing that is typed on the screen.
        sin_atributos = []
        for rob in robs:
            for e in rob.elements.values():
                if e.etype != "entity":
                    continue
                entrada = dominio.get(key(e.display))
                if entrada and not entrada[1]:
                    sin_atributos.append(entrada[0])
        if sin_atributos:
            for nombre in sorted(set(sin_atributos)):
                avisos.append(
                    f"guideline #8 - class '{nombre}' is used as an entity but not declared "
                    f"no attributes in the domain model: the data that the user "
                    f"type they have nowhere to land. The guide asks to populate the model with "
                    f"missing attributes while plotting the flow."
                )
            capas["#8 data flow"] = (
                f"partial - attributes checked ({len(set(sin_atributos))} entity(ies) "
                f"no attributes); without wireframe the screen field is not verified"
            )
        else:
            capas["#8 data flow"] = (
                "partial - entities with attributes; without wireframe the verification is not possible "
                "screen field"
            )
    else:
        capas["#9 entities in the domain"] = "NOT EXECUTED - domain model missing"
        capas["#8 data flow"] = "NOT EXECUTED - domain model missing"

    # --- Guidelines #7, #6, #10: require specification ---
    if hay_spec:
        total_sin_rama, total_sin_comp = 0, 0
        cub_tot, pas_tot = 0, 0
        for rob, spec in emparejar(robs, specs):
            if spec is None:
                avisos.append(
                    f"[{rob.path}] could not be matched to any specifications; "
                    f"guidelines #10, #7 and #6 were not tested for this diagram."
                )
                continue
            total_sin_rama += check_cobertura_flujos(rob, spec, errores)
            c, t, sin_cubrir = check_cobertura_marcador(rob, spec)
            cub_tot += c
            pas_tot += t
            for num, frag in sin_cubrir[:6]:
                avisos.append(
                    f"[{spec.path}] guideline #10 - step {num} has no counterpart "
                    f"lexica in {rob.path}: \"{frag}...\""
                )
        for spec in specs:
            total_sin_comp += check_alternos_sin_comportamiento(spec, errores)
            check_dialogo(spec, errores, avisos)
        metricas["alternos_sin_comportamiento"] = total_sin_rama + total_sin_comp
        metricas["cobertura_marcador"] = (cub_tot / pas_tot) if pas_tot else None
        capas["#10 highlighter test"] = "executed (approximate)"
        capas["#7 alternate courses"] = "executed"
        capas["#6 user/system dialog"] = "executed"
    else:
        for g in ("#10 highlighter test", "#7 alternate courses",
                  "#6 user/system dialog"):
            capas[g] = "NOT EXECUTED - textual specification missing"

    # --- Guideline #3: actors ---
    if hay_cu:
        check_actores(robs, actores_cu, avisos)
        capas["#3 object context and GUI"] = "partial - verified actors"
    else:
        capas["#3 object context and GUI"] = (
            "partial - no use case diagram, actors are not verified"
        )

    capas["#4 technical and non-technical"] = "NOT AUTOMATABLE - verified in the minutes"
    capas["#1 the six steps"] = "compound - add #10, #5, #7 and #2"

    # Layers degraded by an ABSENT input that could have been provided. It is what
    # only one who must push the verdict to the intermediate state; the layers
    # partials by nature do not count (see verdict()).
    degradadas = []
    if not hay_dominio:
        degradadas += ["#9 entities in the domain", "#8 data flow"]
    if not hay_spec:
        degradadas += ["#10 highlighter test", "#7 alternate courses",
                       "#6 user/system dialog"]
    if not hay_cu:
        degradadas.append("#3 object and GUI context (unverified actors)")

    return errores, avisos, infos, metricas, capas, degradadas


def veredicto(errores, avisos, metricas, capas=None) -> tuple:
    """Exit decision model of IEEE 1028 Sec 6.5.6.5, in three states.

    The order of evaluation is deliberate: the rejection condition is checked
    first so that no result is degraded upwards by accumulation of
    favorable cases.
    """
    duras = [
        ("entities without domain", metricas["entidades_sin_dominio"]),
        ("alternates without behavior", metricas["alternos_sin_comportamiento"]),
        ("syntax violations", metricas["violaciones_sintaxis"]),
    ]

    # 1) Reinspection: non-zero hard metrics, below-ground coverage
    # or conformity errors.
    motivos = [f"{n} = {v}" for n, v in duras if v]
    cob = metricas["cobertura_marcador"]
    if cob is not None and cob < COBERTURA_REINSPECCION:
        motivos.append(
            f"highlighter coverage {cob:.0%} < {COBERTURA_REINSPECCION:.0%}"
        )
    if errores:
        motivos.append(f"{len(errores)} compliance error(s)")
    if motivos:
        return ("REINSPECTION REQUIRED", "; ".join(motivos))

    # Coverage is separate from disposition. Missing evidence cannot be
    # accepted as rework; existing blocking findings retain precedence above.
    sin_ejecutar = list(capas or [])
    if sin_ejecutar:
        return ("NOT FULLY VERIFIED",
                f"{len(sin_ejecutar)} layer(s) not executed or partial due to missing "
                f"inputs ({', '.join(sin_ejecutar)}): package cannot be declared "
                f"fully verified")
    if any(v is None for _n, v in duras) or cob is None:
        return ("NOT FULLY VERIFIED",
                "applicable layers lack evidence; the package cannot be declared fully verified")

    # Nonblocking findings can support only a provisional rework disposition.
    intermedio = []
    # Direct verification of the documented criteria: ACCEPTED requires coverage
    # complete, not just be above the reinspection floor.
    if cob is not None and cob < COBERTURA_ACEPTACION:
        intermedio.append(
            f"{cob:.0%} highlighter coverage: above ground level "
            f"reinspection but below the complete coverage required "
            f"ACCEPTED; text remains without counterpart in the diagram"
        )
    if avisos:
        intermedio.append(
            f"{len(avisos)} finding(s) that require your judgment; if confirmed, "
            f"each one needs correction, responsible person and date before closing"
        )
    if intermedio:
        return ("ACCEPTED WITH REWORK VERIFICATION", "; ".join(intermedio))

    # 3) Accepted.
    return (
        "ACCEPTED",
        "hard metrics at zero, coverage over threshold, no errors or "
        "pending warnings",
    )


def presupuesto(robs, specs) -> str:
    lineas = sum(r.text.count("\n") for r in robs) + sum(s.text.count("\n") for s in specs)
    paginas = max(1.0, lineas / LINEAS_POR_PAGINA)
    horas = paginas / RITMO_PAGINAS_HORA
    aviso = ""
    if horas > HORAS_SESION_RAZONABLE:
        aviso = (
            f"  -> exceeds {HORAS_SESION_RAZONABLE:.0f} sustainable meeting hours: "
            f"Consider breaking the package into several sessions."
        )
    return (
        f"Estimated volume: {paginas:.1f} equivalent pages. "
        f"A {RITMO_PAGINAS_HORA:.1f} p/h (IEEE 1028 6.5.2, preliminary design): "
        f"~{horas:.1f} review time.{aviso}"
    )


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass  # old consoles: better to continue than abort

    p = argparse.ArgumentParser(
        description="Validates the consistency of the artifact set for a PDR."
    )
    p.add_argument("--robustez", action="append", required=True,
                   help="robustness diagram (.puml). Repeatable.")
    p.add_argument("--spec", action="append", default=[],
                   help="textual specification of the use case (.md). Repeatable.")
    p.add_argument("--dominio", help="domain model (.puml)")
    p.add_argument("--casos-uso", dest="casos_uso", help="use case diagram (.puml)")
    args = p.parse_args(argv)

    robs = [parse_robustez(path, leer(path)) for path in args.robustez]
    specs = [parse_spec(path, leer(path)) for path in args.spec]
    dominio = parse_dominio(leer(args.dominio)) if args.dominio else {}
    actores_cu = parse_casos_uso(leer(args.casos_uso)) if args.casos_uso else set()

    errores, avisos, infos, metricas, capas, degradadas = validar(
        robs, specs, dominio, actores_cu,
        hay_dominio=bool(args.dominio), hay_spec=bool(specs), hay_cu=bool(args.casos_uso),
    )

    print("Preliminary Design Review (PDR) Validation")
    print("=" * 52)
    print(f"Robustness diagrams: {len(robs)} | Specifications: {len(specs)} | "
          f"Domain classes: {len(dominio)}")
    print(presupuesto(robs, specs))
    print()

    print("METRICS")
    cob = metricas["cobertura_marcador"]
    print(f"  highlighter coverage......... "
          f"{'n/a' if cob is None else f'{cob:.0%}'} (goal: complete; APPROXIMATE)")
    for clave, etiqueta in (
        ("entidades_sin_dominio", "non-domain entities ..........."),
        ("alternos_sin_comportamiento", "alternates without behavior....."),
        ("violaciones_sintaxis", "syntax violations........."),
    ):
        v = metricas[clave]
        print(f"  {etiqueta} {'n/a' if v is None else v} (target: 0)")
    print("  necessary revisions ........... not calculable from the artifacts "
          "(goal: <= 3)")
    print()

    print("COVERAGE OF THE TEN GUIDES")
    for g in sorted(capas):
        print(f"  {g}: {capas[g]}")
    print()

    if errores:
        print(f"ERRORS: {len(errores)}")
        for e in errores:
            print(f"  - {e}")
    else:
        print("ERRORS: none")
    print()

    if avisos:
        print(f"WARNINGS: {len(avisos)}")
        for a in avisos:
            print(f"  - {a}")
    else:
        print("WARNINGS: none")
    print()

    if infos:
        print("INFORMATION")
        for i in infos:
            print(f"  - {i}")
        print()

    estado, motivo = veredicto(errores, avisos, metricas, degradadas)
    print("PROPOSED VERDICT (MKL profile; scale adapted from IEEE 1028 inspection)")
    print(f"  {estado}")
    print(f"  Reason: {motivo}")
    print()
    print("Remember: errors are deterministic failures to comply with the guidelines of the "
          "PDR; warnings require your judgment. Marker coverage is "
          "a lexical approach: you do the real test, phrase by phrase.")

    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
