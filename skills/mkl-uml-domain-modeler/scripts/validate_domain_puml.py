#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Validate a PlantUML domain model against academic conceptual-modeling rules.

This validator reports mechanical errors and review warnings. It does not replace
analyst judgment about domain centrality, use-case traceability, or whether a
hub-like class is legitimate in the domain.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

REQUIRED_LINES = [
    "@startuml",
    "skinparam linetype ortho",
    "skinparam classAttributeIconSize 0",
    "hide methods",
    "hide empty members",
    "@enduml",
]

TECHNICAL_CLASS_TERMS = {
    "Sistema",
    "Aplicacion",
    "Aplicación",
    "Plataforma",
    "Software",
    "Modulo",
    "Módulo",
    "BaseDatos",
    "Database",
    "Tabla",
    "Repositorio",
    "Repository",
    "Controller",
    "Controlador",
    "API",
    "Endpoint",
    "Interfaz",
    "Pantalla",
    "Formulario",
    "Boton",
    "Botón",
    "Pagina",
    "Página",
    "Microservicio",
    "Framework",
    "Servidor",
    # English terms supplement the legacy Spanish input vocabulary.
    "System", "Application", "Platform", "Module", "Table", "UserInterface",
    "Interface", "Screen", "Form", "Button", "Page", "Microservice", "Server",
}

PROCESS_CLASS_PATTERNS = [
    r"^Validacion",
    r"^Validación",
    r"^Calculo",
    r"^Cálculo",
    r"^Proceso",
    r"^Gestion",
    r"^Gestión",
    r"^Crear[A-ZÁÉÍÓÚÑ]",
    r"^Editar[A-ZÁÉÍÓÚÑ]",
    r"^Eliminar[A-ZÁÉÍÓÚÑ]",
    r"^Consultar[A-ZÁÉÍÓÚÑ]",
    r"^Registrar[A-ZÁÉÍÓÚÑ]",
    r"Validation", r"Calculation", r"Process", r"Management",
    r"^Create[A-Z]", r"^Edit[A-Z]", r"^Delete[A-Z]", r"^Query[A-Z]", r"^Register[A-Z]",
]

DESIGN_PATTERN_CLASS_PATTERNS = [
    r"Factory$",
    r"Singleton$",
    r"Strategy$",
    r"Builder$",
    r"Observer$",
    r"Adapter$",
    r"Facade$",
    r"Proxy$",
    r"Decorator$",
    r"Composite$",
    r"Visitor$",
    r"Mediator$",
    r"Manager$",
]


PROCEDURAL_LABEL_TERMS = {
    "valida", "validar", "calcula", "calcular", "muestra", "mostrar",
    "guarda", "guardar", "consulta", "consultar", "notifica", "notificar",
    "genera", "generar", "comunica", "comunicar", "actualiza", "actualizar",
    "impide", "impedir", "verifica", "verificar", "aprueba", "aprobar",
    "rechaza", "rechazar", "afecta", "afectar",
    "validates", "validate", "calculates", "calculate", "displays", "display",
    "saves", "save", "queries", "query", "notifies", "notify",
    "generates", "generate", "communicates", "communicate", "updates", "update",
    "prevents", "prevent", "verifies", "verify", "approves", "approve",
    "rejects", "reject", "affects", "affect",
}

RELATION_RE = re.compile(r"^\s*([A-Za-z_ÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ]*)\s+.*?(?:--|\.\.|<\|).+?\s+([A-Za-z_ÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ]*)\b")
CLASS_RE = re.compile(r"^\s*(?:abstract\s+)?(?:class|enum)\s+([A-Za-z_ÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ]*)")


def read_model(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def camel_split(text: str) -> str:
    """Split CamelCase into words: 'CopyTable' -> 'Copy Table'."""
    out = re.sub(r"(?<=[a-z0-9])(?=[A-ZÁÉÍÓÚÑ])", " ", text or "")
    out = re.sub(r"(?<=[A-ZÁÉÍÓÚÑ])(?=[A-ZÁÉÍÓÚÑ][a-záéíóúñ])", " ", out)
    return re.sub(r"[_\-.]+", " ", out)


def technical_term_in(name: str) -> str | None:
    """Return the technical term found in a class name as a WHOLE WORD, or None.

    Three failure modes had to be handled at once, and each one was observed:

    1. Exact set membership (the original `name in TECHNICAL_CLASS_TERMS`) is
       mute for every compound name. `CopyTable`, `CatalogModule` and
       `BorrowerDatabase` all passed silently — and those are the forms people
       actually write.
    2. Plain substring matching over-fires: "api" is a substring of "Capital".
    3. Whole-word matching on the split words alone misses multi-word terms:
       `UserInterface` splits to "User Interface", so it is never a single word.

    Splitting CamelCase on BOTH the name and the term, then matching the term as
    a contiguous word sequence, is the only form that handles all three.
    """
    phrase = " ".join(camel_split(name).split()).lower()
    for term in TECHNICAL_CLASS_TERMS:
        needle = " ".join(camel_split(term).split()).lower()
        if re.search(rf"(?<![\w]){re.escape(needle)}(?![\w])", phrase):
            return term
    return None


def class_blocks(text: str):
    pattern = re.compile(r"class\s+([A-Za-z_ÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ]*)\s*\{(?P<body>.*?)\}", re.S)
    for match in pattern.finditer(text):
        yield match.group(1), match.group("body")


def detect_classes(text: str) -> list[str]:
    classes = []
    for line in text.splitlines():
        match = CLASS_RE.match(line)
        if match:
            classes.append(match.group(1))
    return classes



def relation_pairs(text: str) -> list[tuple[str, str, str]]:
    pairs: list[tuple[str, str, str]] = []
    relation_op = re.compile(r"(--|-->|<--|--\|>|<\|--|o--|--o|\*--|--\*)")
    name_re = r"[A-Za-z_ÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ]*"
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("'") or line.startswith("@") or line.startswith("skinparam"):
            continue
        if not relation_op.search(line):
            continue
        label = ""
        body = line
        if ":" in line:
            body, label = line.split(":", 1)
            label = label.strip()
        names = re.findall(rf"\b({name_re})\b", relation_op.sub(" ", body))
        if len(names) >= 2:
            pairs.append((names[0], names[1], label))
    return pairs


def generalization_pairs(text: str) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    name_re = r"[A-Za-z_ÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ]*"
    for raw in text.splitlines():
        line = raw.strip()
        if "--|>" in line:
            names = re.findall(rf"\b({name_re})\b", line.split(":", 1)[0])
            if len(names) >= 2:
                pairs.add((names[0], names[1]))  # child, parent
        elif "<|--" in line:
            names = re.findall(rf"\b({name_re})\b", line.split(":", 1)[0])
            if len(names) >= 2:
                pairs.add((names[1], names[0]))  # child, parent
    return pairs

def model_code(text: str) -> str:
    """Mask annotations so their examples cannot become domain evidence."""
    text = re.sub(r"^[ \t]*/'[\s\S]*?(?:'/|\Z)",
                  lambda m: "\n" * m.group().count("\n"), text, flags=re.M)
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


def validate(text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    original_text, text = text, model_code(text)

    stripped = text.strip()
    if not stripped.startswith("@startuml"):
        errors.append("The script must start with @startuml.")
    if not stripped.endswith("@enduml"):
        errors.append("The script must end with @enduml.")

    for required in REQUIRED_LINES[1:-1]:
        if required not in text:
            warnings.append(f"Missing recommended line: {required}")

    # Multiplicities usually appear as quoted role/cardinality markers on associations.
    multiplicity_pattern = re.compile(r'"\s*(?:\d+|\*|\d+\.\.\d+|\d+\.\.\*|0\.\.1|1\.\.\*)\s*"')
    if multiplicity_pattern.search(text):
        errors.append("Multiplicity/cardinality markers were detected; remove them from the domain model.")

    # Look inside class bodies for methods, types, visibility, and IDs.
    for class_name, body in class_blocks(text):
        for raw in body.splitlines():
            line = raw.strip()
            if not line:
                continue
            if "(" in line or ")" in line:
                errors.append(f"Operation-like member detected in {class_name}: {line}")
            if re.match(r"^[+\-#~]", line):
                errors.append(f"Visibility marker detected in {class_name}: {line}")
            if re.search(r":\s*[A-Za-z_]", line):
                errors.append(f"Type annotation detected in {class_name}: {line}")
            if re.search(r"\b(?:id|ID|Id|codigo|Codigo|Código|fk|FK)[A-Za-z_]*\b|[a-z](?:ID|Id)\b", line):
                warnings.append(f"Identifier-like attribute in {class_name}: {line}")

    classes = detect_classes(text)
    if not classes:
        errors.append("The domain model has no usable class declarations.")
    for name in classes:
        hit = technical_term_in(name)
        if hit:
            suffix = "" if name.lower() == hit.lower() else f" (technical term: {hit})"
            warnings.append(f"Possible technical/UI class: {name}{suffix}")

    for name in classes:
        if any(re.search(pattern, name) for pattern in PROCESS_CLASS_PATTERNS):
            warnings.append(f"Possible process/action class: {name}")

    for name in classes:
        if any(re.search(pattern, name) for pattern in DESIGN_PATTERN_CLASS_PATTERNS):
            warnings.append(f"Possible design-pattern/solution-space class: {name}. Patterns like Factory, Singleton, Strategy, or Manager belong to design, not the problem-domain model.")

    if len(classes) > 12 and "package " not in text:
        warnings.append("More than 12 classes without packages; consider conceptual grouping for readability if it improves the rendered diagram.")

    pairs = relation_pairs(text)
    related_names: set[str] = set()
    relation_counts: Counter[str] = Counter()
    for left, right, label in pairs:
        if left in classes:
            related_names.add(left)
            relation_counts[left] += 1
        if right in classes:
            related_names.add(right)
            relation_counts[right] += 1
        label_terms = {term.lower() for term in re.findall(r"\w+", label, flags=re.UNICODE)}
        procedural_hits = sorted(label_terms.intersection(PROCEDURAL_LABEL_TERMS))
        if procedural_hits:
            warnings.append(
                f"Procedural relationship label between {left} and {right}: '{label}'. "
                "Prefer conceptual labels such as has, corresponds to, is documented by, is reported through, is supported by, occupies, applies to, or depends on."
            )

    # Warn about disconnected classes. A superclass may be abstract and still valid if linked by generalization.
    for name in classes:
        if name not in related_names:
            warnings.append(f"Class with no detected relationship: {name}. Connect it, justify it as a superclass/traceable vocabulary, or remove it.")

    # Warn when a base class and lexical specializations coexist without inheritance.
    gen_pairs = generalization_pairs(text)
    class_set = set(classes)
    for base in classes:
        if len(base) < 4:
            continue
        specializations = [name for name in classes if name != base and name.startswith(base) and len(name) > len(base)]
        if len(specializations) >= 1:
            missing = [child for child in specializations if (child, base) not in gen_pairs]
            if missing:
                warnings.append(
                    f"Possible missing generalization: {', '.join(missing)} may specialize {base}. "
                    "Use --|> when the relation is truly is-a, or remove the general class if it adds no conceptual value."
                )

    for name, count in relation_counts.items():
        if count > 6:
            warnings.append(f"Hub-like class with {count} relationships: {name}. Review, do not automatically remove; preserve if it is a genuine central domain concept or needed for use-case traceability.")

    # In clean code-only output, comments are usually unnecessary unless the user requested annotations.
    comment_lines = [line for line in original_text.splitlines() if line.strip().startswith("'")]
    if comment_lines:
        warnings.append("Comment lines detected. Remove role declarations, metadata, or explanatory comments from code-only PlantUML unless annotated output was requested.")

    return errors, warnings


def main(argv: list[str]) -> int:
    # Class names in a domain model are domain vocabulary, so they carry accents
    # in most languages. Without this, a Windows console using cp1252 turns
    # an accented domain name into question marks in every message that names the class, which
    # makes the findings hard to act on.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass  # older consoles: better to continue than to abort

    if len(argv) != 2:
        print("Usage: validate_domain_puml.py path/to/model.puml")
        return 2

    path = Path(argv[1])
    try:
        text = read_model(path)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot read UTF-8 input {path}: {exc}")
        return 2

    errors, warnings = validate(text)

    if errors:
        print("ERRORS")
        for item in errors:
            print(f"- {item}")
    else:
        print("ERRORS: none")

    if warnings:
        print("WARNINGS")
        for item in warnings:
            print(f"- {item}")
    else:
        print("WARNINGS: none")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
