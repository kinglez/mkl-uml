# Copyright 2026 kingle.zhuang. Organization: mkl. See NOTICE.
"""Review control connectivity using parsed BCE and optional located behavior claims.

This PDR-local module owns the record and its structural interpretation. It does
not infer mandatory behavior from vocabulary or turn a robustness view into a
sequence diagram.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from bce_structure import BceStructure


class BehaviorMapError(ValueError):
    """Invalid or stale input record, rather than a proved diagram defect."""


@dataclass
class ControlReview:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    information: list[str] = field(default_factory=list)
    partial: bool = False


def _unique_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise BehaviorMapError(f"duplicate JSON key {name!r}")
        result[name] = value
    return result


def _contained_file(base: Path, relative, field_name: str) -> Path:
    if not isinstance(relative, str) or not relative.strip() or Path(relative).is_absolute():
        raise BehaviorMapError(f"{field_name} must be a nonempty relative local file path")
    try:
        target = (base / relative).resolve()
        is_file = target.is_file()
    except (OSError, ValueError, RuntimeError) as exc:
        raise BehaviorMapError(f"invalid {field_name} file path: {relative!r}") from exc
    try:
        target.relative_to(base)
    except ValueError as exc:
        raise BehaviorMapError(f"{field_name} escapes the behavior-map directory") from exc
    if not is_file:
        raise BehaviorMapError(f"{field_name} file does not exist: {relative}")
    return target


def _read_claims(path: str, diagrams: dict[Path, tuple[str, BceStructure]]):
    record = Path(path).resolve()
    try:
        value = json.loads(record.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BehaviorMapError(f"cannot read behavior map {path}: {exc}") from exc
    if (not isinstance(value, dict) or set(value) != {"schema_version", "required_controls"}
            or type(value["schema_version"]) is not int or value["schema_version"] != 1):
        raise BehaviorMapError("expected schema_version 1 and required_controls")
    entries = value["required_controls"]
    if not isinstance(entries, list) or not entries:
        raise BehaviorMapError("required_controls must be a nonempty list")
    fields = {"diagram", "entry", "control", "step", "source", "line", "quote"}
    seen, claims = set(), []
    for number, item in enumerate(entries, 1):
        if not isinstance(item, dict) or set(item) != fields:
            raise BehaviorMapError(f"required_controls entry {number}: expected {', '.join(sorted(fields))}")
        if any(not isinstance(item[key], str) or not item[key].strip()
               for key in fields - {"line"}):
            raise BehaviorMapError(f"required_controls entry {number}: string fields must be nonempty")
        if type(item["line"]) is not int or item["line"] < 1:
            raise BehaviorMapError(f"required_controls entry {number}: line must be a positive integer")
        diagram = _contained_file(record.parent, item["diagram"], "diagram")
        if diagram not in diagrams:
            raise BehaviorMapError(f"diagram is not one of the supplied --robustez targets: {item['diagram']}")
        source = _contained_file(record.parent, item["source"], "source")
        try:
            lines = source.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            raise BehaviorMapError(f"cannot read behavior source {item['source']}: {exc}") from exc
        if item["line"] > len(lines) or lines[item["line"] - 1].strip() != item["quote"].strip():
            raise BehaviorMapError(f"stale behavior source excerpt: {item['source']}:{item['line']}")
        identity = (diagram, item["entry"], item["control"], source, item["line"], item["step"])
        if identity in seen:
            raise BehaviorMapError(f"duplicate required-control mapping at entry {number}")
        seen.add(identity)
        structure = diagrams[diagram][1]
        for key, expected in (("entry", "boundary"), ("control", "control")):
            element = structure.elements.get(item[key])
            if element is not None and element.etype != expected:
                raise BehaviorMapError(f"{key} alias {item[key]!r} is {element.etype}, expected {expected}")
        claims.append((diagram, source, item))
    return claims


def _reachable_controls(structure: BceStructure, entry: str) -> set[str]:
    # Only explicit control coordination connects behavior to this entry. An
    # actor or shared data entity is not a shortcut between independent flows.
    allowed = {name for name, element in structure.elements.items() if element.etype == "control"}
    allowed.add(entry)
    graph = {name: set() for name in allowed}
    for left, right, _label, _line, _connector in structure.relations:
        if left in allowed and right in allowed:
            graph[left].add(right)
            graph[right].add(left)
    reached, pending = set(), [entry]
    while pending:
        current = pending.pop()
        if current not in reached:
            reached.add(current)
            pending.extend(graph.get(current, set()) - reached)
    return reached


def review_control_connectivity(targets: dict[str, BceStructure], behavior_map: str | None = None) -> ControlReview:
    """Warn on proved isolation; enforce only explicitly located required controls."""
    review = ControlReview()
    diagrams = {Path(name).resolve(): (name, structure) for name, structure in targets.items()}
    for name, structure in targets.items():
        if structure.unchecked:
            review.partial = True
            review.information.append(f"[{name}] control connectivity is partial: unresolved or unsupported BCE evidence; isolation not inferred")
            continue
        connected = {alias for link in structure.relations for alias in (link.left, link.right)}
        for alias, element in structure.elements.items():
            if element.etype == "control" and alias not in connected:
                review.warnings.append(
                    f"[{name}] L{element.line}: isolated control {alias!r} ({element.display!r}) has no communication relationships; review its behavioral responsibility")
    if behavior_map is None:
        return review
    for diagram, source, item in _read_claims(behavior_map, diagrams):
        name, structure = diagrams[diagram]
        origin = f"{source}:{item['line']} (step {item['step']})"
        description = f"required control {item['control']!r} from entry {item['entry']!r}; declared at {origin}"
        if structure.unchecked:
            review.warnings.append(f"[{name}] {description}: connectivity unverified because BCE coverage is partial")
            continue
        control = structure.elements.get(item["control"])
        entry = structure.elements.get(item["entry"])
        location = f" L{control.line}:" if control else ":"
        if entry is None or control is None:
            missing = item["entry"] if entry is None else item["control"]
            review.errors.append(f"[{name}]{location} {description}: mapped alias {missing!r} is absent from this complete diagram")
        elif item["control"] not in _reachable_controls(structure, item["entry"]):
            review.errors.append(f"[{name}]{location} {description}: not reachable through boundary/control coordination")
        else:
            review.information.append(f"[{name}] L{control.line}: {description}: structural connectivity checked; execution order and mandatory traversal remain manual")
    return review
