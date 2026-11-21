# Copyright 2026 kinglezhuang. Organization: mkl. See NOTICE.
"""Check stated message prerequisites in the supported sequence profile."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re

from sequence_structure import parse_secuencia


@dataclass(frozen=True)
class MessageSelector:
    sender: str
    receiver: str
    label: str

    def matches(self, message):
        return (self.sender, self.receiver, self.label) == (
            message.emisor, message.receptor, message.etiqueta)


@dataclass(frozen=True)
class OrderingRule:
    identifier: str
    sequence: Path
    sequence_name: str
    source: Path
    line: int
    before: MessageSelector
    after: MessageSelector


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def local_path(root, value, field):
    relative = Path(value)
    path = (root / relative).resolve()
    if relative.is_absolute() or not path.is_relative_to(root):
        raise ValueError(f"{field} must be a relative path inside the record directory")
    return path


def message_selector(value):
    fields = {"sender", "receiver", "label"}
    if (not isinstance(value, dict) or set(value) != fields
            or any(not isinstance(text, str) or not text.strip() for text in value.values())):
        raise ValueError("message selectors need exact nonempty sender, receiver and label")
    return MessageSelector(**{key: text.strip() for key, text in value.items()})


def load_ordering_evidence(path):
    record = Path(path).resolve()
    try:
        data = json.loads(record.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, ValueError) as error:
        raise ValueError(f"ordering evidence {path}: {error}") from error
    if (not isinstance(data, dict) or set(data) != {"schema_version", "rules"}
            or type(data["schema_version"]) is not int or data["schema_version"] != 1
            or not isinstance(data["rules"], list) or not data["rules"]):
        raise ValueError("ordering evidence needs schema_version 1 and a nonempty rules list")

    rules = {}
    fields = {"id", "sequence", "source", "line", "quote", "before", "after"}
    for index, entry in enumerate(data["rules"], 1):
        try:
            if not isinstance(entry, dict) or set(entry) != fields:
                raise ValueError(f"expected fields: {', '.join(sorted(fields))}")
            for field in ("id", "sequence", "source", "quote"):
                if not isinstance(entry[field], str) or not entry[field].strip():
                    raise ValueError(f"{field} must be nonempty text")
            line = entry["line"]
            if type(line) is not int or line < 1:
                raise ValueError("line must be a positive integer")
            identifier = entry["id"].strip()
            if identifier in rules:
                raise ValueError(f"duplicate rule id {identifier}")
            sequence = local_path(record.parent, entry["sequence"], "sequence")
            source = local_path(record.parent, entry["source"], "source")
            lines = source.read_text(encoding="utf-8").splitlines()
            if line > len(lines) or lines[line - 1].strip() != entry["quote"].strip():
                raise ValueError("stale source location; quote must match the complete source line")
            before, after = message_selector(entry["before"]), message_selector(entry["after"])
            if before == after:
                raise ValueError("before and after must select different messages")
            rules[identifier] = OrderingRule(identifier, sequence, entry["sequence"],
                                             source, line, before, after)
        except (OSError, ValueError) as error:
            raise ValueError(f"ordering evidence {path}, rule {index}: {error}") from error
    return list(rules.values())


def unsupported_reason(sequence):
    if sequence.fragmentos_abiertos or sequence.errores_estructura:
        return "unbalanced or invalid fragment structure"
    if sequence.lineas_no_parseadas:
        return f"unsupported sequence statement at L{sequence.lineas_no_parseadas[0]}"
    source = [line.strip() for line in sequence.codigo.splitlines() if line.strip()]
    starts = [index for index, line in enumerate(source)
              if re.fullmatch(r"@startuml(?:\s+.+)?", line, re.I)]
    ends = [index for index, line in enumerate(source) if line.casefold() == "@enduml"]
    if starts != [0] or not source or ends != [len(source) - 1]:
        return "ordering checks require one complete @startuml/@enduml interaction"
    for operand in sequence.fragmentos:
        if operand.tipo in {"par", "critical"}:
            return f"unsupported {operand.tipo} fragment at L{operand.linea}"
        if operand.tipo == "break" and (operand.profundidad or not operand.guarda):
            return f"ordering checks require a guarded top-level break at L{operand.linea}"
    return ""


def match_paths(sequence, rule):
    """Propagate the two possible prerequisite states through each operand."""
    defaults = {id(operand.items) for operand in sequence.fragmentos
                if operand.tipo == "else" and not operand.guarda}
    after_lines, violations = set(), set()

    def visit(items, states):
        for item in items:
            if item[0] == "msg":
                message = item[1]
                if rule.after.matches(message):
                    after_lines.add(message.linea)
                    if False in states:
                        violations.add(message.linea)
                if rule.before.matches(message):
                    states = {True}
            elif item[0] == "frag":
                _, kind, operands, _ = item
                if kind == "break":
                    # The taken operand is checked, but only the skipped path continues.
                    visit(operands[0], states)
                    continue
                following = set()
                for operand in operands:
                    following.update(visit(operand, states))
                if kind == "alt" and not any(id(operand) in defaults for operand in operands):
                    following.update(states)
                states = following
        return states

    # This property is monotone. Loop skip and one iteration yield all possible
    # states and expose the same violations as additional iterations.
    visit(sequence.arbol, {False})
    return after_lines, violations


def check_ordering(sequences, rules):
    """Return located violations, coverage gaps and checked rule descriptions."""
    sources = {Path(sequence.path).resolve(): sequence for sequence in sequences}
    parsed = {}
    errors, gaps, checked = [], [], []
    for rule in rules:
        prefix = f"ORDERING {rule.identifier} ({rule.source}:{rule.line})"
        current = sources.get(rule.sequence)
        if current is None:
            gaps.append(f"{prefix}: sequence {rule.sequence_name} was not supplied with --secuencia")
            continue
        if rule.sequence not in parsed:
            structure = parse_secuencia(current.path, current.text)
            parsed[rule.sequence] = structure, unsupported_reason(structure)
        structure, reason = parsed[rule.sequence]
        if reason:
            gaps.append(f"{prefix}: [{current.path}] {reason}")
            continue
        after_lines, violations = match_paths(structure, rule)
        if not after_lines:
            gaps.append(f"{prefix}: [{current.path}] no message matches the after selector")
            continue
        for line in sorted(violations):
            errors.append(f"{prefix}: [{current.path}] L{line}: a modeled path reaches "
                          f"'{rule.after.label}' without prior '{rule.before.label}'")
        checked.append(f"{prefix}: [{current.path}] checked {len(after_lines)} selected message(s) "
                       "for the declared prerequisite on supported paths")
    return errors, gaps, checked
