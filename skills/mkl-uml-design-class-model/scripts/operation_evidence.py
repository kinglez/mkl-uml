"""Operation-call and declared-origin evidence for the local MKL profile.

Distributed unchanged with each consumer so a single skill stays self-contained.
This validates declarations and located source excerpts, not their semantic truth.
"""
import json
from pathlib import Path
import re
import unicodedata
from dataclasses import dataclass
from collections import Counter, defaultdict


MESSAGE_RE = re.compile(
    r'^\s*(?P<sender>"[^"]+"|\w+)\s*(?P<arrow>--?>>?|<<?--?)\s*'
    r'(?P<receiver>"[^"]+"|\w+)(?:\s*(?P<lifecycle>\+\+|--|\*\*|!!))?'
    r'\s*(?::\s*(?P<label>.*))?$')
PARTICIPANT_RE = re.compile(
    r'^\s*(?:create\s+)?(?P<kind>actor|boundary|control|entity|participant|database|collections|queue)\s+'
    r'(?:"(?P<label>[^"]+)"|(?P<bare>\w+))(?:\s+as\s+(?P<alias>\w+))?', re.I | re.M)
SORT_RE = re.compile(r'<<\s*(synchCall|asynchCall|reply|asynchSignal|createMessage|deleteMessage)\s*>>', re.I)
CREATE_RE = re.compile(
    r'^\s*create\s+(?:(?:participant|actor|boundary|control|entity|database|queue|collections)\s+)?'
    r'(?P<name>"[^"]+"|\w+)(?:\s+as\s+(?P<alias>\w+))?', re.I)
OPERATION_RE = re.compile(r'^([A-Za-z_]\w*)\s*\(.*\)\s*$', re.S)


@dataclass(frozen=True)
class OperationMessage:
    receiver: str
    operation: str
    label: str
    kind: str
    line: int
    path: str = ""
    sender: str = ""


def sequence_source(text):
    """Mask annotations without changing source line numbers."""
    text = re.sub(r"^[ \t]*/'[\s\S]*?(?:'/|\Z)",
                  lambda match: "\n" * match.group().count("\n"), text, flags=re.M)
    lines, annotation = [], False
    for raw in text.split("\n"):
        line = raw.strip()
        if annotation:
            lines.append("")
            if re.match(r'^end\s*(?:[hr]?note|legend)\b', line, re.I):
                annotation = False
        elif re.match(r'^(?:[hr]?note|legend)\b', line, re.I):
            header = re.sub(r'"(?:\\.|[^"\\])*"', '', line)
            annotation = (":" not in header and not re.match(r'^(?:[hr]?note)\s+"', line, re.I)
                          and not re.search(r'\bend\s*(?:[hr]?note|legend)\b', line, re.I))
            lines.append("")
        else:
            lines.append("" if line.startswith("'") else raw)
    return "\n".join(lines)


def extract_operation_messages(text, path=""):
    """Extract classified call candidates once for both independent validators.

    Arrow appearance does not turn a reply, Signal or lifecycle message into an
    Operation. Explicit instance labels (instance : Classifier) identify the type.
    No argument expression is interpreted as a type or operation declaration.
    """
    code = sequence_source(text)
    aliases = {}
    for match in PARTICIPANT_RE.finditer(code):
        label = match['label'] or match['bare']
        typed = re.fullmatch(r'[^:]*:\s*([A-Za-z_]\w*)', label)
        aliases[match['alias'] or match['bare'] or label] = typed[1] if typed else label
    messages, creating = [], set()
    for number, line in enumerate(code.split("\n"), 1):
        creation = CREATE_RE.match(line)
        if creation:
            creating.add(creation['alias'] or creation['name'].strip('"'))
            continue
        match = MESSAGE_RE.match(line)
        if not match:
            continue
        sender, receiver = match['sender'].strip('"'), match['receiver'].strip('"')
        if match['arrow'].startswith('<'):
            sender, receiver = receiver, sender
        label = (match['label'] or '').strip()
        sorts = {m[1].lower() for m in SORT_RE.finditer(label)}
        label = SORT_RE.sub('', label).strip()
        operation = OPERATION_RE.fullmatch(label)
        kind = 'call' if operation else 'legacy'
        if receiver in creating or match['lifecycle'] in ('**', '!!'):
            kind = 'lifecycle'
            creating.discard(receiver)
        elif sorts:
            if len(sorts) != 1 or not sorts <= {'synchcall', 'asynchcall'}:
                kind = 'non_operation'
            elif not operation:
                kind = 'unresolved_call'
        elif '--' in match['arrow']:
            kind = 'non_operation'
        elif '>>' in match['arrow'] or '<<' in match['arrow']:
            kind = 'unresolved_async'
        messages.append(OperationMessage(aliases.get(receiver, receiver),
            operation[1] if operation and kind == 'call' else '', label, kind, number,
            path, aliases.get(sender, sender)))
    return messages


def legacy_name(text):
    """Whole-label comparison for review hints only, never exact-call matching."""
    text = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    return ''.join(c for c in text.casefold() if c.isalnum())


def operation_origins(declarations, messages, parents=None, abstract=(), explicit=None):
    """Return declaration -> exact/declared/candidate/ambiguous/misplaced/missing.

    Inheritance forwards actual call evidence, not mere ancestor declarations.
    Full-name calls distinguish operations; unresolved natural language and
    overloads remain review candidates instead of success or invented defects.
    """
    parents, explicit = parents or {}, explicit or {}
    def ancestors(name):
        found, pending = set(), list(parents.get(name, ()))
        while pending:
            current = pending.pop()
            if current not in found:
                found.add(current)
                pending.extend(parents.get(current, ()))
        return found
    classes = {d[0] for d in declarations} | set(parents)
    lineage = {name: ancestors(name) for name in classes}
    operation_counts = Counter(d[:2] for d in declarations)
    declared_signatures = defaultdict(lambda: defaultdict(set))
    for declaration in declarations:
        declared_signatures[declaration[0]][declaration[1]].add(operation_key(*declaration)[2])
    receiver_signatures = defaultdict(lambda: defaultdict(set))
    for classifier in classes:
        for owner in {classifier} | lineage[classifier]:
            for name, signatures in declared_signatures[owner].items():
                receiver_signatures[classifier][name].update(signatures)
    exact_receivers = defaultdict(set)
    legacy_by_receiver = defaultdict(set)
    unresolved_receivers, legacy_labels = set(), set()
    for message in messages:
        if message.kind == 'call':
            exact_receivers[message.operation].add(message.receiver)
        elif message.kind == 'legacy':
            receiver, label = legacy_name(message.receiver), legacy_name(message.label)
            legacy_by_receiver[receiver].add(label)
            unresolved_receivers.add(receiver)
            legacy_labels.add(label)
        elif message.kind == 'unresolved_call':
            unresolved_receivers.add(legacy_name(message.receiver))
    receivers_by_classifier = {}
    legacy_receivers_by_classifier = {}
    for classifier in classes:
        receivers = {classifier} | lineage.get(classifier, set())
        if classifier in abstract:
            for child in classes:
                if classifier in lineage.get(child, set()):
                    receivers |= {child} | lineage[child]
        receivers_by_classifier[classifier] = receivers
        legacy_receivers_by_classifier[classifier] = {legacy_name(r) for r in receivers}
    results = {}
    for declaration in declarations:
        classifier, name, parameters = declaration
        key = operation_key(*declaration)
        if key in explicit:
            results[key] = 'declared'
            continue
        receivers = receivers_by_classifier[classifier]
        legacy_receivers = legacy_receivers_by_classifier[classifier]
        calls = exact_receivers.get(name, set())
        addressed = calls & receivers
        if addressed:
            results[key] = ('exact' if operation_counts[declaration[:2]] == 1 and all(
                operation_counts[(receiver, name)] <= 1
                and receiver_signatures[receiver][name] == {key[2]}
                for receiver in addressed)
                else 'ambiguous')
        elif any(legacy_name(name) in legacy_by_receiver.get(receiver, ())
                 for receiver in legacy_receivers):
            results[key] = 'candidate'
        elif legacy_receivers & unresolved_receivers:
            results[key] = 'ambiguous'
        elif calls or legacy_name(name) in legacy_labels:
            results[key] = 'misplaced'
        else:
            results[key] = 'missing'
    return results


def operation_key(classifier, operation, parameters):
    """Preserve parameter tokens while ignoring notation-only whitespace."""
    return classifier, operation, tuple(re.findall(r"\w+|[^\w\s]", parameters))


def modeled_field_accessor(kind, attributes, name):
    """Name-only query contracts are never an accessor exemption."""
    match = re.match(r"^(?:get|set|is|has|Get|Set|Is|Has)([A-Z_].*)$", name)
    if kind == "interface" or not match:
        return False
    normalize = lambda value: value.replace("_", "").casefold()
    return normalize(match[1]) in {normalize(attribute) for attribute in attributes}


def load_operation_evidence(path, declarations):
    """Return exact modeled operations with their inspected source locations.

    Sources are local files contained beside/below the record; no includes,
    commands or remote references are evaluated. Invalid/stale records fail closed.
    """
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    record = Path(path).resolve()
    try:
        data = json.loads(record.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError(f"operation evidence {path}: {exc}") from exc
    if (not isinstance(data, dict) or set(data) != {"schema_version", "operations"}
            or type(data["schema_version"]) is not int or data["schema_version"] != 1
            or not isinstance(data["operations"], list) or not data["operations"]):
        raise ValueError("operation evidence needs schema_version 1 and a nonempty operations list")
    modeled = list(declarations)
    evidence = {}
    fields = {"classifier", "operation", "kind", "source", "line", "quote", "rationale"}
    for index, entry in enumerate(data["operations"], 1):
        location = f"operation evidence {path}, entry {index}"
        if (not isinstance(entry, dict) or not fields <= set(entry)
                or set(entry) - fields - {"parameters"}):
            raise ValueError(f"{location}: expected {', '.join(sorted(fields))}; parameters is optional")
        for field in fields - {"line"}:
            if not isinstance(entry[field], str) or not entry[field].strip():
                raise ValueError(f"{location}: {field} must be nonempty text")
        if entry["kind"] not in {"requirement", "contract", "decision"}:
            raise ValueError(f"{location}: kind must be requirement, contract or decision")
        if type(entry["line"]) is not int or entry["line"] < 1:
            raise ValueError(f"{location}: line must be a positive integer")
        matches = [d for d in modeled if d[:2] == (entry["classifier"], entry["operation"])]
        if "parameters" in entry:
            if not isinstance(entry["parameters"], str):
                raise ValueError(f"{location}: parameters must be the modeled parameter text")
            selected = operation_key(entry["classifier"], entry["operation"], entry["parameters"])
            matches = [d for d in matches if operation_key(*d) == selected]
        if len(matches) != 1:
            raise ValueError(f"{location}: unknown or ambiguous modeled operation; use its visible "
                             "classifier name and exact parameters to distinguish overloads")
        key = operation_key(*matches[0])
        if key in evidence:
            raise ValueError(f"{location}: duplicate operation evidence")
        relative = Path(entry["source"])
        source = (record.parent / relative).resolve()
        if relative.is_absolute() or not source.is_relative_to(record.parent):
            raise ValueError(f"{location}: source must stay inside the record directory")
        try:
            lines = source.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            raise ValueError(f"{location}: unreadable source {entry['source']}: {exc}") from exc
        if (entry["line"] > len(lines)
                or lines[entry["line"] - 1].strip() != entry["quote"].strip()):
            raise ValueError(f"{location}: stale source location; quote must match the complete source line")
        evidence[key] = (f"{entry['classifier']}.{entry['operation']}({matches[0][2]}): "
                         f"declared {entry['kind']} at {source}:{entry['line']} — {entry['rationale']}")
    return evidence
