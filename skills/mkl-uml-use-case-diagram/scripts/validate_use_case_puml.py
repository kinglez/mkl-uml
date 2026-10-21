#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Validator for UML use case diagrams in PlantUML.

The script flags common mechanical and semantic-risk issues. It does not
replace conceptual review by an analyst, but it supports standards-informed
quality gates inspired by UML, requirements traceability, viewpoint separation,
and regression-style checking.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ERRORS: list[str] = []
WARNINGS: list[str] = []
_SEEN_ERRORS: set[str] = set()
_SEEN_WARNINGS: set[str] = set()


def add_error(msg: str) -> None:
    if msg not in _SEEN_ERRORS:
        ERRORS.append(msg)
        _SEEN_ERRORS.add(msg)


def add_warning(msg: str) -> None:
    if msg not in _SEEN_WARNINGS:
        WARNINGS.append(msg)
        _SEEN_WARNINGS.add(msg)


def strip_accents_basic(text: str) -> str:
    table = str.maketrans(
        "áéíóúÁÉÍÓÚñÑüÜ",
        "aeiouAEIOUnNuU",
    )
    return text.translate(table)


def normalize(text: str) -> str:
    return strip_accents_basic(text.lower())


def extract_system_body(text: str) -> str:
    match = re.search(r'\brectangle\s+"[^"]+"\s*\{', text)
    if not match:
        return ""
    start = match.end()
    depth = 1
    i = start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i]
        i += 1
    return ""


def main(path: str, dominant_hint: str | None = None) -> int:
    # Actor and use case names are domain vocabulary, so they carry accents in
    # most languages. Without this, a Windows console using cp1252 turns
    # an accented name into question marks in every message, which makes
    # the findings hard to act on.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass  # older consoles: better to continue than to abort

    p = Path(path)
    if not p.exists():
        print(f"ERROR: file not found: {p}")
        return 2

    text = p.read_text(encoding="utf-8")
    stripped = text.strip()

    if not stripped.startswith("@startuml"):
        add_error("script must start with @startuml")
    if not stripped.endswith("@enduml"):
        add_error("script must end with @enduml")

    for required in [
        "left to right direction",
        "skinparam linetype ortho",
        "skinparam packageStyle rectangle",
        "skinparam shadowing false",
    ]:
        if required not in text:
            add_warning(f"missing recommended directive: {required}")

    if not re.search(r'\brectangle\s+"[^"]+"\s*\{', text):
        add_error('missing system boundary: rectangle "System Name" { ... }')

    if re.search(r'^\s*class\s+', text, re.MULTILINE):
        add_error("use case diagram must not declare classes")

    if re.search(r'^\s*(component|database|interface)\b', text, re.IGNORECASE | re.MULTILINE):
        add_warning("technical diagram elements detected; verify they are not implementation details")

    if re.search(r'\b\w+\s+"(?:1|0\.\.1|1\.\.\*|0\.\.\*|\*)"\s*[-.]', text):
        add_error("multiplicity detected; use case diagrams should not include multiplicities")

    usecases = re.findall(r'^\s*usecase\s+"([^"]+)"\s+as\s+(\w+)', text, re.MULTILINE)
    quoted_actors = re.findall(r'^\s*actor\s+"([^"]+)"\s+as\s+(\w+)', text, re.MULTILINE)
    unquoted_actors = re.findall(r'^\s*actor\s+(\w+)\s*(?:$|\n)', text, re.MULTILINE)
    actors = quoted_actors + [(name, name) for name in unquoted_actors]

    if not usecases:
        add_error("no use cases declared")
    if not actors:
        add_warning("no actors declared")

    alias_to_usecase = {alias: visible for visible, alias in usecases}
    actor_aliases = {alias for _, alias in actors}
    usecase_aliases = set(alias_to_usecase)

    # Check rough placement: actors should not be inside the system boundary and use cases should not be outside it.
    system_body = extract_system_body(text)
    if system_body:
        if re.search(r'^\s*actor\s+', system_body, re.MULTILINE):
            add_error("actor declaration detected inside system boundary")
        outside_text = text.replace(system_body, "")
        if re.search(r'^\s*usecase\s+', outside_text, re.MULTILINE):
            add_error("use case declaration detected outside system boundary")

    technical_terms = [
        "boton", "botón", "pantalla", "formulario", "base de datos", "sql", "api",
        "json", "http request", "http response", "endpoint", "repositorio", "controlador",
        "renderizar", "instanciar", "persistir", "variable interna", "metodo", "método",
        "servicio interno", "microservicio", "tabla", "columna", "query",
        # English terms supplement the legacy Spanish input vocabulary.
        "button", "screen", "form", "database", "repository", "controller",
        "render", "instantiate", "persist", "internal variable", "internal method",
        "internal service", "microservice", "table", "column",
    ]
    internal_step_patterns = [
        "validar", "calcular", "actualizar", "guardar", "persistir", "generar identificador",
        "generar id", "registrar internamente", "asignar identificador", "verificar campo",
        "procesar json", "ejecutar algoritmo", "sincronizar base", "escribir log",
        "validate", "calculate", "update", "save", "persist", "generate identifier",
        "generate unique identifier", "generate id", "record internally", "assign identifier",
        "check field", "process json", "execute algorithm", "synchronize database", "write log",
    ]
    access_terms = [
        "acceder al sistema", "ingresar al sistema", "entrar al sistema", "iniciar sesion", "iniciar sesión",
        "access system", "enter system", "log in", "login"
    ]
    output_terms = [
        "notificar", "enviar notificacion", "enviar notificación", "generar confirmacion",
        "generar confirmación", "emitir comprobante", "generar comprobante", "emitir certificado",
        "notify", "send notification", "generate confirmation", "issue receipt",
        "generate receipt", "issue certificate", "report reservation",
        "issue enrollment", "report enrollment"
    ]
    suspicious_nouns = [
        "disponibilidad real", "vigencia de tarifa", "vigencia de tarifas", "restriccion", "restricción",
        "identificador unico", "identificador único", "estado interno",
        "actual availability", "rate validity", "restriction", "unique identifier", "internal state"
    ]

    for visible, alias in usecases:
        lower = normalize(visible)
        for term in technical_terms:
            if normalize(term) in lower:
                add_warning(f"technical or UI-like term in use case '{visible}'; review viewpoint separation")
        for pattern in internal_step_patterns:
            if normalize(pattern) in lower:
                add_warning(
                    f"possible internal-step use case '{visible}'; keep it only if it is an external actor goal or external-service interaction"
                )
        for noun in suspicious_nouns:
            if normalize(noun) in lower:
                add_warning(f"granularity risk in use case '{visible}'; verify it is not a business rule or postcondition")
        if any(normalize(term) in lower for term in access_terms):
            add_warning(
                f"access/auth use case '{visible}' detected; keep it only if authentication, credentials, identity, roles, or session handling are explicit"
            )
        if any(normalize(term) in lower for term in output_terms):
            add_warning(
                f"system-output use case '{visible}' detected; verify the actor requests it or model it as postcondition/include/extend"
            )
        if not alias.startswith("CU_"):
            add_warning(f"use case alias '{alias}' should preferably start with CU_")
        if len(visible.split()) < 2:
            add_warning(f"use case '{visible}' may be too vague; prefer infinitive verb + domain complement")

    # Actors that look like internal components.
    internal_actor_terms = [
        "base de datos", "database", "controlador", "controller", "repositorio", "repository",
        "servicio interno", "microservicio", "modulo", "módulo", "pantalla", "formulario",
        "internal service", "microservice", "module", "screen", "form"
    ]
    for visible, _alias in actors:
        lower = normalize(visible)
        for term in internal_actor_terms:
            if normalize(term) in lower:
                add_warning(f"actor '{visible}' looks like an internal component; actors should be external roles/systems/devices")

    include_edges = re.findall(r'^\s*(\w+)\s*\.>\s*(\w+)\s*:\s*<<\s*include\s*>>', text, re.MULTILINE | re.IGNORECASE)
    extend_edges = re.findall(r'^\s*(\w+)\s*\.>\s*(\w+)\s*:\s*<<\s*extend\s*>>', text, re.MULTILINE | re.IGNORECASE)
    include_count = len(include_edges)
    extend_count = len(extend_edges)

    if include_count + extend_count > max(8, len(usecases)):
        add_warning("many include/extend relations detected; verify the diagram is not a workflow decomposition")
    if include_count > 8:
        add_warning("high include count; verify include is not being used to represent temporal sequence")
    if extend_count > 4:
        add_warning("high extend count; verify extend is not being used for every alternate/error flow")

    for source, target in include_edges:
        target_name = alias_to_usecase.get(target, target)
        target_lower = normalize(target_name)
        if any(normalize(pattern) in target_lower for pattern in internal_step_patterns):
            add_warning(f"included use case '{target_name}' looks like an internal step; include should not model workflow internals")

    for source, target in extend_edges:
        source_name = alias_to_usecase.get(source, source)
        source_lower = normalize(source_name)
        if any(normalize(pattern) in source_lower for pattern in internal_step_patterns):
            add_warning(f"extending use case '{source_name}' looks like an internal validation/error step; review extend semantics")

    # Direct actor-to-use-case associations.
    assoc_pattern = re.compile(r'^\s*(\w+)\s*-+>\s*(\w+)\s*$', re.MULTILINE)
    direct_actor_links: Counter[str] = Counter()
    actor_targets: defaultdict[str, list[str]] = defaultdict(list)
    for left, right in assoc_pattern.findall(text):
        if left in actor_aliases and right in usecase_aliases:
            direct_actor_links[left] += 1
            actor_targets[left].append(right)
        elif right in actor_aliases and left in usecase_aliases:
            direct_actor_links[right] += 1
            actor_targets[right].append(left)

    for actor, count in direct_actor_links.items():
        if count > 3:
            add_warning(
                f"actor '{actor}' has {count} direct use-case associations; verify the actor is not connected to substeps of one dominant use case"
            )

    included_aliases = {target for _source, target in include_edges}
    extending_aliases = {source for source, _target in extend_edges}
    for actor, targets in actor_targets.items():
        for target in targets:
            if target in included_aliases:
                add_warning(
                    f"use case '{alias_to_usecase[target]}' is directly associated with actor '{actor}' and also included; verify it is an independent actor goal"
                )
            if target in extending_aliases:
                add_warning(
                    f"use case '{alias_to_usecase[target]}' is directly associated with actor '{actor}' and also extends another use case; verify actor initiation"
                )

    # Dominant use case hint check.
    if dominant_hint:
        hint_norm = normalize(dominant_hint)
        matching_aliases = [alias for visible, alias in usecases if hint_norm in normalize(visible)]
        if not matching_aliases:
            add_warning(f"dominant use case hint '{dominant_hint}' not found among declared use cases")
        elif len(matching_aliases) == 1:
            dominant_alias = matching_aliases[0]
            primary_actor_linked = any(dominant_alias in targets for targets in actor_targets.values())
            if not primary_actor_linked:
                add_warning(f"dominant use case '{alias_to_usecase[dominant_alias]}' is not directly associated with any actor")

    print("Use case PlantUML validation report")
    print("===================================")
    if ERRORS:
        print("\nERRORS:")
        for e in ERRORS:
            print(f"- {e}")
    else:
        print("\nERRORS: none")

    if WARNINGS:
        print("\nWARNINGS:")
        for w in WARNINGS:
            print(f"- {w}")
    else:
        print("\nWARNINGS: none")

    return 1 if ERRORS else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a PlantUML use case diagram.")
    parser.add_argument("path", help="Path to .puml file")
    parser.add_argument("--dominant", help="Expected dominant use case name, if known")
    args = parser.parse_args()
    raise SystemExit(main(args.path, args.dominant))
