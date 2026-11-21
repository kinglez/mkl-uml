# Copyright 2026 kingle.zhuang. Organization: mkl. See NOTICE.
"""Parse the local sequence structure and branch evidence for sequence and CDR.

This is a literal profile. Unparsed statements are retained as unknown evidence.
Consumers decide diagnostics and cross-artifact review policy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re


TIPOS_INFRA = ("participant", "database", "queue", "collections")

# Participant declarations.
# Trailing color (#LightCoral) and stereotype (<<x>>) are supported. Without
# this suffix, colored declarations were NOT parsed, despite the robustness
# contract REQUIRING color for alternate-only objects. Omitting it silently
# disabled coverage for alternate-flow Controllers, precisely those most
# easily forgotten during design.
DECL_RE = re.compile(
    r"^\s*(?:create\s+)?(?P<tipo>actor|boundary|control|entity|participant|database|queue|collections)\s+"
    r'(?:"(?P<label>[^"]+)"|(?P<bare>[\w]+))'
    r"(?:\s+as\s+(?P<alias>[\w]+))?"
    r"(?:\s+(?:#[#\w]+|<<[^>]+>>))*\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Messages support common PlantUML arrows and activation SHORTHAND
# (`++`, `--`, `**`, `!!`) following the receiver.
#
# Without `corto`, `A -> B ++ : msg` did not match: the whole message
# disappeared, making diagrams appear empty and producing false orphan
# participant and uncovered-Controller errors. This syntax is recommended
# by references/notation-rules.md. A parser failing its own documented
# syntax is worse than a strict parser.
MSG_RE = re.compile(
    r'^\s*(?P<emisor>"[^"]+"|[\w]+)\s*'
    r"(?P<flecha>--?>>?|<<?--?|->>|-->|->|<-)\s*"
    r'(?P<receptor>"[^"]+"|[\w]+)'
    r"(?:\s*(?P<corto>\+\+|--|\*\*|!!))?"
    r"\s*(?::\s*(?P<etiqueta>.*))?$"
)
AUTOACT_RE = re.compile(r"^\s*autoactivate\s+(?P<estado>on|off)\b", re.IGNORECASE)
MESSAGE_SORT_RE = re.compile(
    r"<<\s*(synchCall|asynchCall|reply|asynchSignal|createMessage|deleteMessage)\s*>>",
    re.IGNORECASE,
)
# Single-line presentation directives do not supply interaction evidence.
DISPLAY_LINE_RE = re.compile(
    r"(?:@startuml(?:\s+.+)?|@enduml|==.*==|(?:hide|show) footbox|"
    r"(?:title|autonumber|newpage)(?:\s+.+)?|skinparam\s+\w+\s+[^{}]+)",
    re.IGNORECASE,
)
NOTA_ABRE = re.compile(
    r"^\s*(?:/')?\s*(?:h|r)?note\b(?!.*\bend\s*note\b)(?!.*:)", re.IGNORECASE
)
FRAG_ABRE = re.compile(
    r"^\s*(?P<kind>alt|opt|loop|par|critical|break|group)\b\s*(?P<guarda>.*)$",
    re.IGNORECASE,
)
FRAG_ELSE = re.compile(r"^\s*else\b\s*(?P<guarda>.*)$", re.IGNORECASE)
FRAG_CIERRA = re.compile(r"^\s*end\b\s*$", re.IGNORECASE)
ACT_RE = re.compile(r"^\s*(?P<op>activate|deactivate)\s+(?P<quien>[\w]+)", re.IGNORECASE)

@dataclass
class Participante:
    alias: str
    label: str
    tipo: str
    linea: int

    @property
    def display(self) -> str:
        return self.label or self.alias

    @property
    def es_infra(self) -> bool:
        return self.tipo in TIPOS_INFRA


@dataclass
class Mensaje:
    emisor: str
    receptor: str
    etiqueta: str
    flecha: str
    linea: int

    @property
    def es_retorno(self) -> bool:
        sorts = {match.casefold() for match in MESSAGE_SORT_RE.findall(self.etiqueta)}
        if sorts:
            return sorts == {"reply"}
        return "--" in self.flecha and ">" in self.flecha


@dataclass
class Operando:
    tipo: str
    guarda: str
    linea: int
    profundidad: int
    items: list = field(default_factory=list)


@dataclass
class Secuencia:
    path: str
    text: str
    participantes: dict = field(default_factory=dict)
    mensajes: list = field(default_factory=list)
    arbol: list = field(default_factory=list)   # items: ('msg',Message) | ('act',operation,who,line) | ('frag',kind,[operands])
    fragmentos: list[Operando] = field(default_factory=list)
    usa_activaciones: bool = False
    autoactivate: bool = False
    codigo: str = ""  # executable notation, with comments/notes blanked
    lineas_no_parseadas: list[int] = field(default_factory=list)
    errores_estructura: list[str] = field(default_factory=list)
    fragmentos_abiertos: int = 0


# --------------------------------------------------------------------------
# Sequence parser with fragment tree
# --------------------------------------------------------------------------

def codigo_secuencia(text: str) -> str:
    """Blank comments and note text, preserving source line numbers."""
    text = re.sub(r"^[ \t]*/'[\s\S]*?(?:'/|\Z)",
                  lambda m: "\n" * m.group().count("\n"), text, flags=re.MULTILINE)
    lineas, en_nota = [], False
    for crudo in text.split("\n"):
        ln = crudo.strip()
        if en_nota:
            if re.match(r"^end\s*(?:[hr]?note|legend)\b", ln, re.I):
                en_nota = False
            lineas.append("")
        elif not ln or ln.startswith("'"):
            lineas.append("")
        elif re.match(r"^(?:(?:h|r)?note|legend)\b", ln, re.IGNORECASE):
            en_nota = ln.lower().startswith("legend") or bool(NOTA_ABRE.match(ln))
            lineas.append("")
        else:
            lineas.append(crudo)
    return "\n".join(lineas)


def parse_secuencia(path: str, text: str) -> Secuencia:
    s = Secuencia(path=path, text=text)
    text = s.codigo = codigo_secuencia(text)
    lineas = text.split("\n")

    for m in DECL_RE.finditer(text):
        label = m.group("label") or m.group("bare") or ""
        alias = m.group("alias") or m.group("bare") or label
        nlin = text.count("\n", 0, m.start("tipo")) + 1
        s.participantes[alias] = Participante(alias, label, m.group("tipo").lower(), nlin)

    def parsear(i: int, prof: int):
        """Return (items, next_index); stop at 'else' or 'end'."""
        items = []
        while i < len(lineas):
            crudo = lineas[i]
            ln = crudo.strip()
            n = i + 1
            if not ln or DISPLAY_LINE_RE.fullmatch(ln) or DECL_RE.fullmatch(ln):
                i += 1
                continue
            mauto = AUTOACT_RE.match(ln)
            if mauto:
                if mauto.group("estado").lower() == "on":
                    s.autoactivate = True
                    s.usa_activaciones = True
                items.append(("auto", mauto.group("estado").lower(), n))
                i += 1
                continue
            if FRAG_CIERRA.match(ln) or FRAG_ELSE.match(ln):
                if prof:
                    return items, i
                if FRAG_ELSE.match(ln):
                    s.errores_estructura.append(f"L{n}: 'else' requires an open alt or par fragment")
                else:
                    s.errores_estructura.append(f"L{n}: 'end' without an open fragment")
                # Recover so a stray separator cannot hide the rest of the input.
                i += 1
                continue
            ma = FRAG_ABRE.match(ln)
            if ma:
                kind = ma.group("kind").lower()
                operand = Operando(kind, ma.group("guarda").strip(), n, prof)
                operands = []
                j = i + 1
                while True:
                    s.fragmentos.append(operand)
                    operand.items, j = parsear(j, prof + 1)
                    operands.append(operand.items)
                    if j >= len(lineas):
                        s.fragmentos_abiertos += 1
                        break
                    mel = FRAG_ELSE.match(lineas[j].strip())
                    if mel:
                        if kind not in ("alt", "par"):
                            s.errores_estructura.append(f"L{j + 1}: 'else' requires an open alt or par fragment")
                        operand = Operando("else", mel.group("guarda").strip(), j + 1, prof)
                        j += 1
                        continue
                    if FRAG_CIERRA.match(lineas[j].strip()):
                        j += 1
                        break
                    break
                # opt/loop may be skipped: include an empty path
                if kind in ("opt", "loop", "break"):
                    operands.append([])
                items.append(("frag", kind, operands, n))
                i = j
                continue
            mact = ACT_RE.match(ln)
            if mact:
                s.usa_activaciones = True
                items.append(("act", mact.group("op").lower(), mact.group("quien"), n))
                i += 1
                continue
            mm = MSG_RE.match(ln)
            if mm:
                emisor = mm.group("emisor").strip('"')
                receptor = mm.group("receptor").strip('"')
                flecha = mm.group("flecha")
                # Left-facing arrow: sender is on the RIGHT.
                # Without normalization, B <-- E was counted as sent by B, corrupting
                # the distribution used by the centralized-control check. It also failed
                # return recognition because the pattern looked for >.
                # Normalize direction before assessing either property.
                if flecha.startswith("<"):
                    emisor, receptor = receptor, emisor
                    flecha = flecha[1:][::-1].replace("<", ">") + ">"
                    flecha = ("--" + ">") if "--" in mm.group("flecha") else "->"
                msg = Mensaje(emisor, receptor, (mm.group("etiqueta") or "").strip(),
                              flecha, n)
                s.mensajes.append(msg)
                items.append(("msg", msg))
                # Shorthand: ++ activates the receiver; -- deactivates the sender.
                # Translate to the same items as long-form commands for per-path
                # activation-balance checking.
                corto = mm.group("corto")
                if corto in ("++", "--"):
                    s.usa_activaciones = True
                    if corto == "++":
                        items.append(("act", "activate", receptor, n))
                    else:
                        items.append(("act", "deactivate", emisor, n))
                i += 1
                continue
            s.lineas_no_parseadas.append(n)
            items.append(("unknown", n))
            i += 1
        return items, i

    s.arbol, consumidas = parsear(0, 0)
    if consumidas != len(lineas):
        raise ValueError("internal parser failed to consume the sequence")
    return s


def operand_coverage(items) -> str:
    """Interpret the parsed operand, including what the parser could not read."""
    partial = False
    pending = list(items)
    while pending:
        item = pending.pop()
        if item[0] == "msg":
            return "covered"
        if item[0] == "unknown":
            partial = True
        elif item[0] == "frag":
            for operand in item[2]:
                pending.extend(operand)
    return "partial" if partial else "empty"


def branch_evidence(sequence, identify_flows):
    """Return the strongest parsed operand evidence for each explicit flow label."""
    strengths = {"empty": 0, "partial": 1, "covered": 2}
    states = {}
    for operand in sequence.fragmentos:
        identifiers = identify_flows(operand.guarda)
        if identifiers:
            state = operand_coverage(operand.items)
            for key in identifiers:
                if strengths[state] > strengths[states.get(key, "empty")] or key not in states:
                    states[key] = state
    return states
