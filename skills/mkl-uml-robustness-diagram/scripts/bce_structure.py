# Copyright 2026 kingle.zhuang. Organization: mkl. See NOTICE.
"""Read literal PlantUML BCE structure for both standalone MKL validators.

Distributed unchanged with robustness and PDR. Connection rules, severity,
and review dispositions belong to the calling skill.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import NamedTuple


_QUOTED = r'"(?:\\.|[^"\\])*"'
_NAME = rf"(?:{_QUOTED}|\w+)"
_ROLE = r"actor|boundary|control|entity"
_STEREOTYPES = r"(?:\s*<<[^>]+>>)*"
_DECL_START = re.compile(rf"^(?:{_ROLE})\s+", re.I)
_DECL = re.compile(
    rf"^(?P<role>{_ROLE})\s+(?P<name>{_NAME}){_STEREOTYPES}"
    rf"(?:\s+as\s+(?P<other>{_NAME}){_STEREOTYPES})?"
    r"(?:\s+(?P<color>#[#\w]+))?$",
    re.I,
)
# PlantUML accepts full direction names and their one- and two-letter forms.
# https://plantuml.com/class-diagram
_DIRECTION = r"(?:left|le|l|right|ri|r|up|u|down|do|d)"
_STYLE = r"\[[^\]]*\]"
_CONNECTOR = (
    rf"(?:<\|?)?[-.]+(?:{_STYLE}[-.]*)?"
    rf"(?:{_DIRECTION}(?:{_STYLE})?[-.]+)?(?:\|?>+)?"
)
_REL = re.compile(
    rf"^(?P<left>{_NAME})\s*(?P<connector>{_CONNECTOR})\s*"
    rf"(?P<right>{_NAME})\s*(?::\s*(?P<label>.*))?$",
    re.I,
)
_REL_LIKE = re.compile(r"[-.]{2}|[-.][a-z]+[-.]", re.I)
_HIDDEN = re.compile(r"\[[^\]]*\bhidden\b[^\]]*\]", re.I)
_ANNOTATION = re.compile(r"^(?:[hr]?note|legend)\b", re.I)
_ANNOTATION_END = re.compile(r"\bend\s*(?:[hr]?note|legend)\b", re.I)
_NOTE_ALIAS = re.compile(rf'^[hr]?note\s+(?:{_QUOTED}\s+)?as\s+(?P<alias>\w+)\b', re.I)
_INLINE_NOTE = re.compile(rf"^[hr]?note\s+{_QUOTED}", re.I)
_DISPLAY = re.compile(r"^(?:skinparam|title|hide|caption|footer|header|left to|top to)\b", re.I)


@dataclass(frozen=True)
class Element:
    alias: str
    label: str
    etype: str
    line: int
    color: str = ""

    @property
    def display(self) -> str:
        return self.label or self.alias


class Relationship(NamedTuple):
    left: str
    right: str
    label: str
    line: int
    connector: str


@dataclass(frozen=True)
class Source:
    code: str
    notes: str
    comments: str
    note_aliases: frozenset[str]


@dataclass(frozen=True)
class BceStructure:
    source: Source
    elements: dict[str, Element]
    # Only communication relationships with two resolved BCE endpoints.
    relations: list[Relationship]
    unchecked: list[tuple[int, str]]


def split_source(text: str) -> Source:
    """Separate annotations and retain source locations and metadata comments."""
    text = re.sub(r"^[ \t]*/'[\s\S]*?(?:'/|\Z)",
                  lambda match: "\n" * match.group().count("\n"), text, flags=re.M)
    code, notes, comments = [], [], []
    aliases = set()
    in_note = False
    for raw in text.split("\n"):
        line = raw.strip()
        if in_note:
            notes.append(raw)
            code.append("")
            if _ANNOTATION_END.match(line):
                in_note = False
        elif _ANNOTATION.match(line):
            notes.append(raw)
            code.append("")
            alias = _NOTE_ALIAS.match(line)
            if alias:
                aliases.add(alias["alias"])
            header = re.sub(_QUOTED, "", line)
            in_note = ":" not in header and not _INLINE_NOTE.match(line) and not _ANNOTATION_END.search(header)
        elif line.startswith("'"):
            comments.append(raw)
            code.append("")
        else:
            code.append(raw)
    return Source("\n".join(code), "\n".join(notes), "\n".join(comments), frozenset(aliases))


def _unquote(name: str) -> str:
    return name[1:-1] if name.startswith('"') else name


def parse_bce(text: str) -> BceStructure:
    """Resolve forward references; distinguish unverified syntax from missing aliases."""
    source = split_source(text)
    elements: dict[str, Element] = {}
    pending: list[Relationship] = []
    unchecked: list[tuple[int, str]] = []
    declarations_incomplete = False
    for number, raw in enumerate(source.code.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("@") or _DISPLAY.match(line):
            continue
        if line.startswith("!"):
            if not re.match(r"^!(?:theme|pragma)\b", line, re.I):
                unchecked.append((number, f"PlantUML preprocessing is not checked: {line}"))
                declarations_incomplete = True
            continue
        decl = _DECL.match(line)
        if decl:
            label, alias = decl.group("name", "other")
            if alias and alias.startswith('"') and not label.startswith('"'):
                alias, label = label, alias
            alias = _unquote(alias or label)
            elements[alias] = Element(alias, _unquote(label), decl["role"].lower(),
                                      number, decl["color"] or "")
            continue
        if _DECL_START.match(line):
            unchecked.append((number, f"BCE declaration syntax could not be parsed: {line}"))
            declarations_incomplete = True
            continue
        relation = _REL.match(line)
        if relation:
            if not _HIDDEN.search(relation["connector"]):
                pending.append(Relationship(_unquote(relation["left"]), _unquote(relation["right"]),
                                            (relation["label"] or "").strip(), number,
                                            relation["connector"]))
        elif _REL_LIKE.search(line):
            unchecked.append((number, f"relationship-like syntax could not be parsed: {line}"))

    relations = []
    for link in pending:
        missing = [endpoint for endpoint in dict.fromkeys((link.left, link.right)) if endpoint not in elements]
        if any(name in source.note_aliases for name in missing):
            continue
        if missing:
            aliases = ", ".join(map(repr, missing))
            reason = ("unsupported declarations or preprocessing may supply the endpoint"
                      if declarations_incomplete else "no typed declaration in this source")
            unchecked.append((link.line, f"cannot check BCE relationship; unresolved endpoint(s) {aliases}; {reason}"))
        else:
            relations.append(link)
    return BceStructure(source, elements, relations, sorted(unchecked))
