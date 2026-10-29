#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Validate textual use case specifications in Markdown.

Check mechanically verifiable properties: minimum fields, well-formed and unique
identifiers, resolving cross-references, and writing risks such as ambiguous
vocabulary, passive/impersonal voice, implementation details, and unresolved flows.

This does not judge the domain or replace analyst review: an ERROR is a verifiable
structural defect; a WARNING is a risk requiring judgment.

Both the lean two-paragraph form and the full template are supported. Sections
absent from the lean form are not required. English and legacy Spanish input are
supported; Python names and statistics keys remain stable for compatibility.

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
    "primary actor": r"primary\s+actor|actor\s+(primario|principal)",
    "trigger": r"disparador|trigger|evento\s+inicial|initial\s+event",
    "preconditions": r"precondici|preconditions?",
    "basic flow": r"(flujo|curso)\s+(basico|principal)|escenario\s+soleado|(?:basic|main)\s+(?:flow|course)|sunny.day\s+scenario",
    "postconditions": r"postcondici|postconditions?",
    "acceptance criteria": r"criterios?\s+de\s+aceptacion|acceptance\s+criteri(?:a|on)",
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


# --- Identifier collection -----------------------------------------------


def collect_ids(text: str, prefix: str) -> tuple[dict[str, int], set[str]]:
    """Return ({identifier: definition_count}, {referenced_identifiers})."""
    definidos: dict[str, int] = {}
    referenciados: set[str] = set()
    # `(?!\.\d)` excludes template-prescribed substeps (`FA-01.1`, `FA-01.2`):
    # these detail a flow rather than defining `FA-01` again. Without this guard,
    # following the template exactly produced false duplicate-identifier errors.
    encontrar = re.compile(rf"\b({prefix}-\d+)(?!\.\d)\b")
    # A definition starts a line or table cell with the identifier.
    definir = re.compile(rf"^\|?\s*\**\s*({prefix}-\d+)(?!\.\d)\b")

    for raw in text.splitlines():
        line = raw.strip()
        m = definir.match(line)
        if m:
            definidos[m.group(1)] = definidos.get(m.group(1), 0) + 1
        for found in encontrar.findall(line):
            referenciados.add(found)
    return definidos, referenciados


def seccion(text: str, patron: str) -> str:
    """Extract the section from the heading matching `patron` to the next heading."""
    lineas = text.splitlines()
    inicio = None
    for i, raw in enumerate(lineas):
        if raw.lstrip().startswith("#") and re.search(patron, norm(raw)):
            inicio = i
            break
    if inicio is None:
        return ""
    for j in range(inicio + 1, len(lineas)):
        if lineas[j].lstrip().startswith("#"):
            return "\n".join(lineas[inicio:j])
    return "\n".join(lineas[inicio:])


def contar_pasos(bloque: str) -> int:
    """Count numbered steps in a table (| 3 | ...) or list (3. ...)."""
    n = 0
    for raw in bloque.splitlines():
        line = raw.strip()
        if re.match(r"^\|\s*\d+\s*\|", line) or re.match(r"^\d+[\.\)]\s+\S", line):
            n += 1
    return n


# --- Validation -----------------------------------------------------------


def validate(text: str):
    text = re.sub(r"<!--[\s\S]*?(?:-->|\Z)", "", text)
    errores: list[str] = []
    avisos: list[str] = []
    plano = norm(text)

    # -- Minimum fields
    for etiqueta, patron in CAMPOS_MINIMOS.items():
        if not re.search(patron, plano):
            if etiqueta == "acceptance criteria":
                avisos.append(
                    "no acceptance criteria found; without them the specification "
                    "is not verifiable and tests cannot be derived"
                )
            else:
                errores.append(f"missing minimum specification field: {etiqueta}")

    # -- Unfilled template markers, including legacy Spanish markers
    placeholders = re.findall(r"\[[A-Z]{2,4}-XX\]|\[Nombre del [^\]]+\]|\[Actor Primario\]|\[(?:[A-Za-z ]+ name|Use Case Name|Primary Actor)\]", text, re.IGNORECASE)
    if placeholders:
        avisos.append(
            f"{len(placeholders)} unfilled template markers remain "
            f"(e.g., {placeholders[0]}); a partially completed template is not a specification"
        )

    # -- Identifier format, duplicates, and dangling references
    todos_definidos: dict[str, dict[str, int]] = {}
    for prefix in ID_PREFIXES:
        definidos, referenciados = collect_ids(text, prefix)
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
    bloque_basico = seccion(text, CAMPOS_MINIMOS["basic flow"])
    pasos = contar_pasos(bloque_basico)
    if pasos > MAX_PASOS_FLUJO:
        avisos.append(
            f"the basic flow has {pasos} steps (threshold {MAX_PASOS_FLUJO}); "
            "confirm that it describes one scenario rather than several use cases"
        )

    # -- Alternate flows without an outcome
    for prefix in ("FA", "FE"):
        definidos, _ = collect_ids(text, prefix)
        for ident in sorted(definidos):
            contexto = "\n".join(
                l for l in text.splitlines() if ident in l
            )
            if not re.search(r"retorna|vuelve|finaliza|termina|continua|cancela|reanuda|returns?|ends?|terminates?|continues?|cancels?|resumes?", norm(contexto)):
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
