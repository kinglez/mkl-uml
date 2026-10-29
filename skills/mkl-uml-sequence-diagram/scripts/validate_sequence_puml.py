#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
# Modification notice: validate usable diagram boundaries and retain complete bounded paths.
# Modification notice: include typed create declarations in participant discovery.
"""Detailed-design sequence diagram validator (MKL).

Cross-checks the sequence diagram, robustness diagram, specification, and
 domain model. Most detailed-design defects concern the relationship between
 design and analysis, not the .puml file alone.

Unlike PDR, detailed design legitimately introduces SOLUTION-SPACE classes
 absent from the domain. Only a participant declared `entity` but missing
 from the domain is a finding: `entity` claims domain-class status.

Usage:
    python3 validate_sequence_puml.py --secuencia caso_01_secuencia.puml
        --robustez caso_01_robustez.puml
        --spec caso_01_especificacion.md
        --dominio modelo_dominio.puml

Exit codes:
    0  no errors (warnings may remain)
    1  errors: diagram fails validation
    2  usage error or file not found
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# Declared constants and thresholds (references/notation-rules.md)
# --------------------------------------------------------------------------

TIPOS_BCE = ("actor", "boundary", "control", "entity")
TIPOS_INFRA = ("participant", "database", "queue", "collections")

# Terms suggesting infrastructure mislabeled as a domain entity; multilingual input remains supported.
INFRA_TERMS = (
    "orm", "dao", "base de datos", "basedatos", "database", "db", "repositorio",
    "repository", "conexion", "connection", "driver", "cliente http", "httpclient",
    "cache", "session", "sesion", "transaccion", "transaction", "broker",
    "servlet", "endpoint", "api rest",
)

# Empty verbs: a message containing only these allocates no behavior.
MENSAJES_GENERICOS = (
    "procesar", "proceso", "gestionar", "gestion", "manejar", "hacer",
    "ejecutar", "realizar", "operar", "tratar", "process", "handle", "manage",
    "do", "execute", "perform",
)

# Normalize equivalent flow identifiers: FA-01, FA1, FA 1, fa_01.
FLUJO_RE = re.compile(r"\b(FA|FE)\s*[-_ ]?\s*0*(\d+)\b", re.IGNORECASE)

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
NOTA_ABRE = re.compile(
    r"^\s*(?:/')?\s*(?:h|r)?note\b(?!.*\bend\s*note\b)(?!.*:)", re.IGNORECASE
)
NOTA_CIERRA = re.compile(r"^\s*end\s*note\b", re.IGNORECASE)

FRAG_ABRE = re.compile(
    r"^\s*(?P<kind>alt|opt|loop|par|critical|break|group)\b\s*(?P<guarda>.*)$",
    re.IGNORECASE,
)
FRAG_ELSE = re.compile(r"^\s*else\b\s*(?P<guarda>.*)$", re.IGNORECASE)
FRAG_CIERRA = re.compile(r"^\s*end\b\s*$", re.IGNORECASE)
ACT_RE = re.compile(r"^\s*(?P<op>activate|deactivate)\s+(?P<quien>[\w]+)", re.IGNORECASE)

CLASS_RE = re.compile(
    r'^\s*(?:abstract\s+)?class\s+(?:"(?P<q>[^"]+)"|(?P<n>[\w]+))', re.MULTILINE
)

# Check all three output-contract directives: notation-rules.md makes them
# contractual; checking only the first silently ignored the other two.
REQUIRED_DIRECTIVES = (
    "skinparam style strictuml",
    "skinparam shadowing false",
    "skinparam responseMessageBelowArrow true",
)

STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "de", "del", "al", "y", "o", "en",
    "con", "por", "para", "que", "se", "su", "sus", "lo", "a", "the", "of",
    "to", "and", "or", "in", "on", "for", "is", "are",
}

# THRESHOLDS: skill conventions, NOT published evidence.
#
# Upstream research sought primary numeric readability thresholds for
# lifelines, messages, and nesting, but found NO accessible source.
# Available comprehension studies did not isolate those variables.
# These numbers are therefore local judgment, identifying where to inspect.
# They all generate WARNINGS, never errors. Adjust unsuitable thresholds
# for a domain without implying any standards violation.
UMBRAL_RETORNOS = 0.40       # return-message proportion
UMBRAL_CENTRALIZADO = 0.60   # proportion of messages sent by one participant
PROFUNDIDAD_CADENA = 3       # consecutive self-calls before warning
MAX_CAMINOS = 256            # execution-path enumeration cap
MAX_ANIDAMIENTO = 2          # fragment nesting levels before warning


# --------------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------------

def strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text or "")
        if unicodedata.category(c) != "Mn"
    )


def norm(text: str) -> str:
    return strip_accents(text or "").strip().lower()


def camel_split(text: str) -> str:
    """Split CamelCase: 'RecordDAOFactory' -> 'Record DAO Factory'.

    Whole-word matching needs this: joined names otherwise evade detection,
    while substring matching overfires ('api' occurs within Spanish 'Terapia').
    Split both sides and use word boundaries to avoid both failures.
    """
    t = re.sub(r"(?<=[a-z0-9])(?=[A-ZÁÉÍÓÚÑ])", " ", text or "")
    t = re.sub(r"(?<=[A-ZÁÉÍÓÚÑ])(?=[A-ZÁÉÍÓÚÑ][a-záéíóúñ])", " ", t)
    return re.sub(r"[_\-.]+", " ", t)


def frase(text: str) -> str:
    return " ".join(norm(camel_split(text)).split())


def contiene_termino(nombre: str, terminos) -> str | None:
    """Return a term matched as a complete word sequence, or None."""
    p = frase(nombre)
    for t in terminos:
        needle = frase(t)
        if needle and re.search(rf"(?<![\w]){re.escape(needle)}(?![\w])", p):
            return t
    return None


def key(text: str) -> str:
    """Identity key for a participant or lifeline.

    Used for INDEXING (`out[key(nombre)] = nombre`): collisions overwrite
    earlier entries, silently removing a participant. An empty key is
    dangerous because every empty result collides. Handle both causes:

    1. Stopword-only names. Common aliases `A`/`B` include stopword `a`;
       fall back to unfiltered pieces.
    2. The [a-z0-9] filter erases names in other alphabets and all pieces;
       raw normalized text is the final fallback.
    """
    t = re.sub(r"[^a-z0-9 ]+", " ", frase(text))
    piezas = [w for w in t.split() if w]
    sin_stop = [w for w in piezas if w not in STOPWORDS]
    return "".join(sin_stop or piezas) or re.sub(r"\s+", "", norm(text))


def palabras(text: str) -> set[str]:
    t = re.sub(r"[^a-z0-9 ]+", " ", frase(text))
    return {w for w in t.split() if len(w) > 2 and w not in STOPWORDS}


def flujos_declarados(text: str) -> set[str]:
    return {
        f"{m.group(1).upper()}-{int(m.group(2)):02d}"
        for m in FLUJO_RE.finditer(text or "")
    }


def leer(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeError) as exc:
        print(f"Cannot read input {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)


# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------

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
        return "--" in self.flecha and ">" in self.flecha


@dataclass
class Secuencia:
    path: str
    text: str
    participantes: dict = field(default_factory=dict)
    mensajes: list = field(default_factory=list)
    arbol: list = field(default_factory=list)   # items: ('msg',Message) | ('act',operation,who,line) | ('frag',kind,[operands])
    fragmentos: list = field(default_factory=list)  # (kind, guard, line, depth)
    usa_activaciones: bool = False
    autoactivate: bool = False
    codigo: str = ""  # executable notation, with comments/notes blanked


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
            if NOTA_CIERRA.match(ln):
                en_nota = False
            lineas.append("")
        elif not ln or ln.startswith("'"):
            lineas.append("")
        elif re.match(r"^(?:h|r)?note\b", ln, re.IGNORECASE):
            en_nota = bool(NOTA_ABRE.match(ln))
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
        nlin = text[: m.start()].count("\n") + 1
        s.participantes[alias] = Participante(alias, label, m.group("tipo").lower(), nlin)

    def parsear(i: int, prof: int):
        """Return (items, next_index); stop at 'else' or 'end'."""
        items = []
        while i < len(lineas):
            crudo = lineas[i]
            ln = crudo.strip()
            n = i + 1
            if not ln or ln.startswith("'") or ln.startswith("@") or ln.startswith("=="):
                i += 1
                continue
            # note/hnote/rnote blocks contain free text, often the use case text
            # allowed by the notation guide. It may begin with alt. Skip these blocks
            # so free text does not enter the fragment tree and create false
            # unclosed-fragment findings: end note is not a fragment terminator.
            # Preserve the distinction between notes and fragments.
            if NOTA_ABRE.match(ln):
                i += 1
                while i < len(lineas) and not NOTA_CIERRA.match(lineas[i].strip()):
                    i += 1
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
                # Invalid top-level separators are diagnosed independently; do
                # not let them truncate parsing of the remaining executable input.
                i += 1
                continue
            ma = FRAG_ABRE.match(ln)
            if ma:
                kind = ma.group("kind").lower()
                s.fragmentos.append((kind, ma.group("guarda").strip(), n, prof))
                operandos = []
                j = i + 1
                while True:
                    sub, j = parsear(j, prof + 1)
                    operandos.append(sub)
                    if j >= len(lineas):
                        break
                    mel = FRAG_ELSE.match(lineas[j].strip())
                    if mel:
                        # An else guard can also declare a flow. Register it so an FA/FE
                        # labeled on an alternate branch is not falsely reported missing.
                        # This is the normal case for use cases with multiple alternatives.
                        # Coverage must include identifiers on all operands.
                        # Preserve alternate-branch identifiers.
                        s.fragmentos.append(("else", mel.group("guarda").strip(),
                                             j + 1, prof))
                        j += 1
                        continue
                    if FRAG_CIERRA.match(lineas[j].strip()):
                        j += 1
                        break
                    break
                # opt/loop may be skipped: include an empty path
                if kind in ("opt", "loop", "break"):
                    operandos.append([])
                items.append(("frag", kind, operandos, n))
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
            i += 1
        return items, i

    s.arbol, consumidas = parsear(0, 0)
    if consumidas != len(lineas):
        raise ValueError("internal parser failed to consume the sequence")
    return s


class Caminos(list):
    """Complete retained paths and whether any alternatives were omitted."""
    limitado = False


def enumerar_caminos(items, tope=MAX_CAMINOS):
    """Enumerate execution paths; an N-branch alt multiplies them.

    Linear activation/deactivation counts produce false positives: every
    branch closes independently, but only one branch executes.
    """
    caminos = Caminos([[]])
    for it in items:
        if it[0] == "frag":
            _, _kind, operandos, _n = it
            alternativas = [enumerar_caminos(op, tope) for op in operandos]
            nuevos = Caminos()
            nuevos.limitado = caminos.limitado or any(a.limitado for a in alternativas)
            for c in caminos:
                for op in alternativas:
                    for sub in op:
                        if len(nuevos) == tope:
                            nuevos.limitado = True
                            break
                        nuevos.append(c + sub)
                    if len(nuevos) == tope and nuevos.limitado:
                        break
                if len(nuevos) == tope and nuevos.limitado:
                    break
            caminos = nuevos or caminos
        else:
            # Reaching the cap limits alternative prefixes, never the suffix.
            for c in caminos:
                c.append(it)
    return caminos


# --------------------------------------------------------------------------
# Input-artifact parsers
# --------------------------------------------------------------------------

def parse_robustez(text: str) -> dict:
    """Return {type: {key: original_name}} from the robustness diagram."""
    out = {t: {} for t in TIPOS_BCE}
    for m in DECL_RE.finditer(text):
        tipo = m.group("tipo").lower()
        if tipo not in TIPOS_BCE:
            continue
        label = m.group("label") or m.group("bare") or ""
        alias = m.group("alias") or m.group("bare") or label
        out[tipo][key(label or alias)] = label or alias
    return out


def parse_dominio(text: str) -> dict:
    out = {}
    for m in CLASS_RE.finditer(text):
        nombre = m.group("q") or m.group("n")
        out[key(nombre)] = nombre
    return out


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_estructura(s: Secuencia, errores: list, avisos: list) -> None:
    tag = f"[{s.path}]"
    codigo = s.codigo or codigo_secuencia(s.text)
    lineas = codigo.split("\n")
    inicios = [i for i, ln in enumerate(lineas)
               if re.match(r"^\s*@startuml(?:\s+.*)?\s*$", ln, re.IGNORECASE)]
    finales = [i for i, ln in enumerate(lineas)
               if re.match(r"^\s*@enduml\s*$", ln, re.IGNORECASE)]
    if len(inicios) != 1 or len(finales) != 1 or inicios[0] >= finales[0]:
        errores.append(f"{tag} expected one ordered @startuml / @enduml diagram")
    elif any(ln.strip() for ln in lineas[:inicios[0]] + lineas[finales[0] + 1:]):
        errores.append(f"{tag} executable content outside @startuml / @enduml boundaries")
    if not s.participantes:
        errores.append(f"{tag} the sequence diagram has no declared participants")
    if not s.mensajes:
        errores.append(f"{tag} the sequence diagram has no usable messages")
    abiertos = []
    en_nota = False
    for ln_i, crudo in enumerate(lineas, 1):
        ln = crudo.strip()
        # This independent sweep must also skip notes: free text may start with
        # alt, and end note does not close a fragment. A parser-only repair
        # left the same false positive active here.
        # Keep this sweep consistent with the parser.
        if en_nota:
            if NOTA_CIERRA.match(ln):
                en_nota = False
            continue
        if NOTA_ABRE.match(ln):
            en_nota = True
            continue
        ma = FRAG_ABRE.match(ln)
        if ma:
            abiertos.append(ma.group("kind").lower())
        elif FRAG_ELSE.match(ln):
            if not abiertos or abiertos[-1] not in ("alt", "par"):
                errores.append(f"{tag} L{ln_i}: 'else' requires an open alt or par fragment")
        elif FRAG_CIERRA.match(ln):
            if abiertos:
                abiertos.pop()
            else:
                errores.append(f"{tag} L{ln_i}: 'end' without an open fragment")
    if abiertos:
        errores.append(f"{tag} {len(abiertos)} fragment(s) remain unclosed by 'end'")

    for kind, guarda, n, prof in s.fragmentos:
        if kind == "else":
            continue
        # prof is zero-based; the human-readable level is prof+1. Comparing the
        # raw index to the threshold missed the documented three-level case
        # (alt inside opt inside loop), requiring a fourth level to trigger.
        # Compare the human-readable nesting level.
        nivel = prof + 1
        if nivel > MAX_ANIDAMIENTO:
            avisos.append(
                f"{tag} L{n}: fragment '{kind}' nested at level {nivel}. "
                f"More than {MAX_ANIDAMIENTO} levels usually means the use case "
                f"should be split rather than the diagram shrunk."
            )

    for d in REQUIRED_DIRECTIVES:
        if d not in codigo:
            avisos.append(f"{tag} missing contract directive: {d}")


def check_participantes(s: Secuencia, errores: list, avisos: list) -> None:
    tag = f"[{s.path}]"
    usados = set()
    for m in s.mensajes:
        usados.add(m.emisor)
        usados.add(m.receptor)

    for p in s.participantes.values():
        if p.alias not in usados and p.display not in usados:
            errores.append(
                f"{tag} L{p.linea}: participant '{p.display}' neither sends nor receives "
                f"any messages. A sequence participant exists "
                f"because it participates: connect or remove it."
            )
        etq = p.label or ""
        if re.search(r"<<\s*(boundary|control|entity)\s*>>", etq, re.IGNORECASE):
            avisos.append(
                f"{tag} L{p.linea}: '{p.display}' repeats its stereotype in the label. "
                f"PlantUML keyword `{p.tipo}` already draws the icon."
            )


def check_actor(s: Secuencia, errores: list) -> None:
    tag = f"[{s.path}]"
    actores = {a for a, p in s.participantes.items() if p.tipo == "actor"}
    bordes = {a for a, p in s.participantes.items() if p.tipo == "boundary"}
    for m in s.mensajes:
        for extremo, otro in ((m.emisor, m.receptor), (m.receptor, m.emisor)):
            if extremo in actores and otro not in bordes and otro in s.participantes:
                tipo_otro = s.participantes[otro].tipo
                errores.append(
                    f"{tag} L{m.linea}: actor '{s.participantes[extremo].display}' "
                    f"exchanges messages with '{s.participantes[otro].display}' "
                    f"({tipo_otro}). Actors interact only with Boundary objects."
                )
                break


def check_activaciones(s: Secuencia, errores: list, avisos: list, pidio_activaciones: bool) -> None:
    tag = f"[{s.path}]"
    if not s.usa_activaciones:
        return
    if not pidio_activaciones:
        avisos.append(
            f"{tag} the diagram uses unrequested activations. Reference material "
            f"prefers omitting them for simplicity, while explicitly stating this "
            f"is a matter of taste rather than an error."
        )
    if s.autoactivate:
        avisos.append(
            f"{tag} the diagram uses 'autoactivate on': PlantUML manages automatic "
            f"regions; per-path balance is checked for explicit manual activations "
            f"while autoactivation is off."
        )
    caminos = enumerar_caminos(s.arbol)
    problemas = set()
    for camino in caminos:
        pila, modo_auto = {}, False
        for it in camino:
            if it[0] == "auto":
                modo_auto = it[1] == "on"
                continue
            if it[0] != "act" or modo_auto:
                continue
            _, op, quien, n = it
            if op == "activate":
                pila[quien] = pila.get(quien, 0) + 1
            else:
                pila[quien] = pila.get(quien, 0) - 1
                if pila[quien] < 0:
                    problemas.add(
                        f"{tag} L{n}: 'deactivate {quien}' without an open activation on "
                        f"some execution path"
                    )
                    pila[quien] = 0
        for quien, v in pila.items():
            if v > 0:
                problemas.add(
                    f"{tag} activation leak: '{quien}' remains active without 'deactivate' "
                    f"on some execution path"
                )
    for p in sorted(problemas):
        errores.append(p)


def check_retornos(s: Secuencia, avisos: list) -> None:
    tag = f"[{s.path}]"
    if not s.mensajes:
        return
    ret = [m for m in s.mensajes if m.es_retorno]
    prop = len(ret) / len(s.mensajes)
    if prop > UMBRAL_RETORNOS:
        avisos.append(
            f"{tag} {len(ret)} of {len(s.mensajes)} messages are returns ({prop:.0%}). "
            f"Sources agree on omission unless useful: a consumed value, "
            f"a meaningful synchronous reply, or an error branch. Model an asynchronous "
            f"callback as its own call or Signal."
        )


def check_nombres_mensaje(s: Secuencia, avisos: list) -> None:
    tag = f"[{s.path}]"
    for m in s.mensajes:
        if not m.etiqueta:
            continue
        hit = contiene_termino(m.etiqueta, MENSAJES_GENERICOS)
        if hit and len(palabras(m.etiqueta)) <= 2:
            avisos.append(
                f"{tag} L{m.linea}: message '{m.etiqueta}' is generic ('{hit}'). "
                f"State the message intent precisely; for an operation call, "
                f"use an identifier that states what it does."
            )


def check_control_centralizado(s: Secuencia, avisos: list) -> None:
    tag = f"[{s.path}]"
    if len(s.mensajes) < 5:
        return
    emisiones = {}
    for m in s.mensajes:
        if m.es_retorno:
            continue
        emisiones[m.emisor] = emisiones.get(m.emisor, 0) + 1
    total = sum(emisiones.values())
    if not total:
        return
    for alias, n in sorted(emisiones.items(), key=lambda x: -x[1]):
        prop = n / total
        if prop > UMBRAL_CENTRALIZADO:
            disp = s.participantes[alias].display if alias in s.participantes else alias
            avisos.append(
                f"{tag} centralized control: '{disp}' sends {n} of {total} messages "
                f"({prop:.0%}). Check whether each receiver could own its work; "
                f"one participant doing everything suggests behavior "
                f"accumulated rather than being allocated."
            )
        break


def check_autollamadas(s: Secuencia, avisos: list) -> None:
    """Consecutive self-calls suggest an algorithm rather than collaboration.

    This is the automatable symptom of a disguised flowchart.
    Deliberately NOT a Law of Demeter check: detecting A requesting an object
    from B and then messaging that returned object requires knowing which
    returns carry references. The diagram does not establish this.
    A naive A->B->C->D chain check flags DISTRIBUTED DELEGATION, precisely
    what the source recommends. Penalizing sound design is worse than
    omitting a check. Message chains remain human review, documented in
    references/behavior-allocation.md.
    """
    tag = f"[{s.path}]"
    # PER PATH, not file order. Calls on distinct alt branches are mutually
    # exclusive and never consecutive. Linear counting reproduces the earlier
    # scanner false positive. Deduplicate findings by line, as for activation
    # balance, while examining each actual execution path.
    # Preserve branch-sensitive interpretation.
    hallazgos = {}
    for camino in enumerar_caminos(s.arbol):
        seguidas, inicio = 0, None
        for it in camino:
            if it[0] != "msg":
                continue
            m = it[1]
            if m.es_retorno:
                seguidas = 0
                continue
            if m.emisor == m.receptor:
                seguidas += 1
                if seguidas == 1:
                    inicio = m.linea
                if seguidas >= PROFUNDIDAD_CADENA:
                    hallazgos[m.linea] = (seguidas, inicio)
                    seguidas = 0
            else:
                seguidas = 0
    for linea in sorted(hallazgos):
        seguidas, inicio = hallazgos[linea]
        avisos.append(
            f"{tag} L{linea}: {seguidas} consecutive self-calls from L{inicio} on "
            f"one execution path. An object repeatedly calling itself "
            f"is executing an algorithm rather than collaborating: check whether "
            f"that behavior belongs to another class."
        )


def check_cierre_dominio(s: Secuencia, dominio: dict, errores: list, infos: list) -> None:
    """The domain model is AUTHORITATIVE about domain-class membership.

    Apply infrastructure terms only to entities ABSENT from the domain:
    'Parking Session' contains 'session', but a declared domain class is
    authoritative. Term lists overriding the domain would falsely flag
    legitimate business concepts such as session, transaction, or record.
    """
    tag = f"[{s.path}]"
    solucion = []
    for p in s.participantes.values():
        if p.tipo == "entity":
            if key(p.display) in dominio:
                continue  # domain model is authoritative: domain class
            hit = contiene_termino(p.display, INFRA_TERMS)
            if hit:
                errores.append(
                    f"{tag} L{p.linea}: '{p.display}' is declared `entity` but is "
                    f"infrastructure ('{hit}') absent from the domain model. "
                    f"`entity` is reserved for domain classes; use `participant`, "
                    f"`database`, or `queue`."
                )
            else:
                errores.append(
                    f"{tag} L{p.linea}: entity '{p.display}' claims to be a domain "
                    f"class but is absent from the domain model. Either it was discovered late or "
                    f"its name drifted from the preceding artifact."
                )
        elif p.es_infra or p.tipo == "control":
            if key(p.display) not in dominio:
                solucion.append(p.display)
    if solucion:
        infos.append(
            "SOLUTION-space participants (expected in detailed design; "
            "record them in the operation delta): " + ", ".join(sorted(solucion))
        )
    usadas = {key(p.display) for p in s.participantes.values()}
    no_usadas = [n for k, n in dominio.items() if k not in usadas]
    if no_usadas:
        infos.append(
            "Domain classes unused by this use case (information, not a defect): "
            + ", ".join(sorted(no_usadas))
        )


def check_cobertura_controladores(s: Secuencia, rob: dict, errores: list) -> int:
    """Guideline #7: use case behavior IS the robustness Controllers."""
    tag = f"[{s.path}]"
    controladores = rob.get("control", {})
    if not controladores:
        return 0
    # Vocabulary that may cover a Controller.
    vocab_participantes = {key(p.display) for p in s.participantes.values()}
    texto_etiquetas = " ".join(m.etiqueta for m in s.mensajes if m.etiqueta)
    palabras_etiquetas = palabras(texto_etiquetas)

    sin_cubrir = 0
    for k, nombre in sorted(controladores.items()):
        if k in vocab_participantes:
            continue
        # Deliberately permissive: ONE shared meaningful word suffices.
        # A Controller becomes one or several operations and may legitimately
        # change name. Strict matching would turn legitimate renaming into
        # false errors. Detect a DISAPPEARED Controller, not a renamed one.
        # Allocation coverage is heuristic, not exact-name matching.
        pal = palabras(nombre)
        if pal and (pal & palabras_etiquetas):
            continue
        sin_cubrir += 1
        errores.append(
            f"{tag} robustness Controller '{nombre}' appears neither as "
            f"message nor participant. Use case behavior is represented by "
            f"Controllers: allocate it to a class or justify its disappearance."
        )
    return sin_cubrir


def check_cobertura_flujos(s: Secuencia, spec_text: str, spec_path: str, errores: list) -> int:
    tag = f"[{s.path}]"
    declarados = flujos_declarados(spec_text)
    if not declarados:
        return 0
    texto_frag = " ".join(f"{k} {g}" for k, g, _n, _p in s.fragmentos)
    dibujados = flujos_declarados(texto_frag) | flujos_declarados(
        " ".join(m.etiqueta for m in s.mensajes if m.etiqueta)
    )
    faltan = sorted(declarados - dibujados)
    for fid in faltan:
        errores.append(
            f"{tag} flow {fid}, declared in {spec_path}, has no fragment in the "
            f"diagram. Basic and all alternate courses belong on the same diagram."
        )
    return len(faltan)


def check_se_quedo_en_robustez(s: Secuencia, rob: dict, avisos: list) -> None:
    """Anti-pattern 8: exact one-to-one correspondence with Controllers."""
    tag = f"[{s.path}]"
    controladores = rob.get("control", {})
    if len(controladores) < 3:
        return
    etiquetas = [m.etiqueta for m in s.mensajes if m.etiqueta and not m.es_retorno]
    if not etiquetas:
        return
    exactos = sum(
        1 for c in controladores.values()
        if any(key(c) == key(e) for e in etiquetas)
    )
    if exactos == len(controladores) and len(etiquetas) == len(controladores):
        avisos.append(
            f"{tag} each robustness Controller appears as a message with "
            f"the same name, one to one ({exactos}/{len(controladores)}). This suggests "
            f"mechanical steps ran without step 4: copying Controllers "
            f"does not allocate them to a class."
        )


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def validar(s, rob, dominio, spec_text, spec_path, hay_rob, hay_dom, hay_spec,
            pidio_activaciones):
    errores, avisos, infos = [], [], []
    capas = {}
    metricas = {"controladores_sin_cubrir": None, "flujos_sin_fragmento": None}

    check_estructura(s, errores, avisos)
    check_participantes(s, errores, avisos)
    check_actor(s, errores)
    check_activaciones(s, errores, avisos, pidio_activaciones)
    check_retornos(s, avisos)
    check_nombres_mensaje(s, avisos)
    check_control_centralizado(s, avisos)
    check_autollamadas(s, avisos)
    if enumerar_caminos(s.arbol).limitado:
        avisos.append(
            f"[{s.path}] path enumeration exceeded its cap of {MAX_CAMINOS}; "
            f"per-path checks used complete retained paths as a sample, not exhaustively."
        )
    capas["notacion y estructura"] = "ejecutada"
    capas["asignacion de comportamiento (heuristica)"] = "ejecutada"

    if hay_rob:
        metricas["controladores_sin_cubrir"] = check_cobertura_controladores(s, rob, errores)
        check_se_quedo_en_robustez(s, rob, avisos)
        capas["cobertura de Controladores (guia #7)"] = "ejecutada"
        faltan_part = []
        for tipo in ("boundary", "entity", "actor"):
            for k, nombre in rob.get(tipo, {}).items():
                pass
        for p in s.participantes.values():
            if p.tipo in ("boundary", "entity", "actor"):
                if key(p.display) not in rob.get(p.tipo, {}):
                    faltan_part.append(f"{p.display} ({p.tipo})")
        if faltan_part:
            avisos.append(
                f"[{s.path}] participants absent from the robustness diagram: "
                + ", ".join(sorted(faltan_part))
                + ". Preserve upstream names or declare the change."
            )
        capas["cierre de participantes contra DR-XX"] = "ejecutada"
    else:
        capas["cobertura de Controladores (guia #7)"] = "NO EJECUTADA - falta el diagrama de robustez"
        capas["cierre de participantes contra DR-XX"] = "NO EJECUTADA - falta el diagrama de robustez"

    if hay_dom:
        check_cierre_dominio(s, dominio, errores, infos)
        capas["cierre de entidades contra el dominio"] = "ejecutada"
    else:
        capas["cierre de entidades contra el dominio"] = "NO EJECUTADA - falta el modelo de dominio"

    if hay_spec:
        metricas["flujos_sin_fragmento"] = check_cobertura_flujos(s, spec_text, spec_path, errores)
        capas["cobertura de flujos alternativos"] = "ejecutada"
        capas["barrido texto <-> mensajes (guia #6)"] = "parcial - la correspondencia fina la haces tu"
    else:
        capas["cobertura de flujos alternativos"] = "NO EJECUTADA - falta la especificacion"
        capas["barrido texto <-> mensajes (guia #6)"] = "NO EJECUTADA - falta la especificacion"

    capas["paso 4: asignacion a la clase correcta"] = "NO MECANIZABLE - requiere tu juicio"

    return errores, avisos, infos, capas, metricas


# Legacy result keys remain stable; CLI layer labels are displayed in English.
DISPLAY_LABELS = {'NO EJECUTADA - falta el diagrama de robustez': 'NOT EXECUTED - robustness diagram missing',
 'NO EJECUTADA - falta el diagrama de secuencia': 'NOT EXECUTED - sequence diagram missing',
 'NO EJECUTADA - falta el modelo de dominio': 'NOT EXECUTED - domain model missing',
 'NO EJECUTADA - falta la especificacion': 'NOT EXECUTED - specification missing',
 'NO MECANIZABLE - requiere tu juicio': 'NOT AUTOMATABLE - requires your judgment',
 'anemia y responsabilidades': 'anemia and responsibilities',
 'asignacion de comportamiento (heuristica)': 'behavior allocation (heuristic)',
 'barrido texto <-> mensajes (guia #6)': 'text <-> message sweep (guideline #6)',
 'cierre de entidades contra el dominio': 'entity closure against domain',
 'cierre de participantes contra DR-XX': 'participant closure against DR-XX',
 'cobertura de Controladores (guia #7)': 'Controller coverage (guideline #7)',
 'cobertura de flujos alternativos': 'alternate-flow coverage',
 'ejecutada': 'executed',
 'granularidad y firmas': 'granularity and signatures',
 'modelo vacio': 'empty model',
 'notacion y contrato': 'notation and contract',
 'notacion y estructura': 'notation and structure',
 'parcial - la correspondencia fina la haces tu': 'partial - detailed correspondence requires your '
                                                  'judgment',
 'paso 4: asignacion a la clase correcta': 'step 4: allocation to the correct class',
 'procedencia de atributos': 'attribute provenance',
 'procedencia de clases': 'class provenance',
 'procedencia de operaciones': 'operation provenance',
 'procedencia de relaciones': 'relationship provenance'}


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    p = argparse.ArgumentParser(
        description="Validate a detailed-design sequence diagram against its inputs."
    )
    p.add_argument("--secuencia", required=True, help="sequence diagram (.puml)")
    p.add_argument("--robustez", help="robustness diagram DR-XX (.puml)")
    p.add_argument("--spec", help="use case specification (.md)")
    p.add_argument("--dominio", help="domain model (.puml)")
    p.add_argument("--con-activaciones", action="store_true",
                   help="declare that activation bars were explicitly requested")
    args = p.parse_args(argv)

    s = parse_secuencia(args.secuencia, leer(args.secuencia))
    rob = parse_robustez(leer(args.robustez)) if args.robustez else {}
    dominio = parse_dominio(leer(args.dominio)) if args.dominio else {}
    spec_text = leer(args.spec) if args.spec else ""

    errores, avisos, infos, capas, metricas = validar(
        s, rob, dominio, spec_text, args.spec or "",
        hay_rob=bool(args.robustez), hay_dom=bool(args.dominio), hay_spec=bool(args.spec),
        pidio_activaciones=args.con_activaciones,
    )

    print("Sequence diagram validation (detailed design)")
    print("=" * 54)
    n_ctrl = len(rob.get("control", {})) if rob else 0
    print(f"Participants: {len(s.participantes)} | Messages: {len(s.mensajes)} | "
          f"Fragments: {len(s.fragmentos)} | Controllers in DR: {n_ctrl}")
    caminos = enumerar_caminos(s.arbol)
    print(f"Enumerated execution paths: {len(caminos)}"
          + (f" (bounded sample, cap {MAX_CAMINOS})" if caminos.limitado else ""))
    print()

    print("METRICS")
    for clave, etiqueta in (
        ("controladores_sin_cubrir", "Uncovered Controllers ........."),
        ("flujos_sin_fragmento", "Flows without fragments ......."),
    ):
        v = metricas[clave]
        print(f"  {etiqueta} {'n/a' if v is None else v}   (target: 0)")
    print()

    print("LAYER COVERAGE")
    for c in sorted(capas):
        print(f"  {DISPLAY_LABELS.get(c, c)}: {DISPLAY_LABELS.get(capas[c], capas[c])}")
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

    print("Remember: errors are deterministic violations; warnings "
          "require judgment. Step 4, deciding which class receives each operation, "
          "cannot be automated: this script checks completeness, not correct "
          "allocation.")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
