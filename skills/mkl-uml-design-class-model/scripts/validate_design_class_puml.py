#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
# Modification notice: resolve class aliases in relationship and inheritance endpoints.
# Modification notice: operation provenance excludes replies, Signals and lifecycle events.
# Modification notice: preserve typed create declarations and separate Signal receptions.
"""Design class model validator (MKL step 7).

Cross-checks multiple artifacts, as the PDR and sequence validators do.
PROVENANCE is central: every model element must trace to a source artifact.
An untraceable element is a finding, not permission to invent.

Usage:
    python3 validate_design_class_puml.py --clases modelo_clases_diseno.puml
        --dominio modelo_dominio.puml
        [--secuencia caso_01_secuencia.puml ...]
        [--spec caso_01_especificacion.md ...]

Exit codes:
    0  no errors (warnings may remain)
    1  errors: model is not ready for CDR
    2  usage error or file not found

Message provenance: annotate labels with <<synchCall>>, <<asynchCall>>,
<<reply>>, <<asynchSignal>>, <<createMessage>> or <<deleteMessage>>.
Explicit call annotations require an operation signature, such as approve().
Unannotated solid synchronous arrows retain legacy lexical call matching;
unannotated asynchronous arrows remain unresolved. Dashed replies and
creation/destruction commands or shorthand do not establish operations.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# THRESHOLDS: skill conventions, NOT evidence.
# No corpus source specifies these numbers. They generate WARNINGS, never
# errors: an invented threshold must not block work.
# --------------------------------------------------------------------------
MAX_OPERACIONES = 12          # above this: God-class candidate
MAX_ATRIBUTOS = 12
MIN_CLASES_ENJAMBRE = 8       # minimum class count for swarm assessment
MAX_PROP_CLASES_MINIMAS = 0.5  # proportion of classes with <=1 operation
SIMILITUD_DERIVA = 0.72       # similarity threshold for vocabulary drift suggestions

# SOLUTION-space terms. An unmarked class containing these terms is
# usually undeclared infrastructure. Spanish terms remain supported input.
TERMINOS_SOLUCION = (
    "dao", "repository", "repositorio", "factory", "fabrica", "singleton",
    "strategy", "estrategia", "adapter", "adaptador", "proxy", "observer",
    "builder", "facade", "fachada", "manager", "gestor", "service", "servicio",
    "controller", "controlador", "handler", "helper", "util", "utils",
    "mapper", "orm", "dto", "session", "sesion", "cache", "buffer", "parser",
    "validator", "validador", "config", "logger",
)

# Design patterns: flag only WITHOUT provenance (anti-pattern 10).
TERMINOS_PATRON = (
    "factory", "singleton", "strategy", "adapter", "proxy", "observer",
    "builder", "facade", "decorator", "visitor", "mediator", "composite",
)

# Getters/setters: the source discourages drawing them.
ACCESOR_RE = re.compile(r"^(get|set|is|has)[A-Z_]", re.IGNORECASE)

STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "de", "del", "al", "y", "o", "en",
    "con", "por", "para", "que", "se", "su", "sus", "lo", "a",
    "the", "of", "to", "and", "or", "in", "on", "for", "is", "are",
}

REQUIRED_DIRECTIVES = (
    "skinparam classAttributeIconSize 0",
    "skinparam linetype ortho",
    "skinparam shadowing false",
)

# --- PlantUML class declarations with optional stereotypes ---
CLASE_RE = re.compile(
    r'^\s*(?P<abstracta>abstract\s+)?(?P<tipo>class|interface|enum)\s+'
    r'(?:"(?P<q>[^"]+)"|(?P<n>[\w]+))'
    r'(?:\s+as\s+(?P<alias>[\w]+))?'
    r'(?P<estereotipos>(?:\s*<<[^>]+>>)*)',
    re.MULTILINE,
)
# Members inside a class body.
#
# Fowler syntax documented in `references/notation-rules.md`:
# `visibility name : type multiplicity = default {property-string}`; the
# `{static}` modifier may PRECEDE it. Earlier patterns rejected defaults,
# multiplicity, and leading modifiers, SILENTLY discarding members written
# exactly as the skill prescribed. Silence was dangerous:
# an entity whose attributes all had defaults appeared to have none,
# incorrectly triggering the entity-without-attributes anti-pattern.
# Preserve those valid member forms.
#
# The same gap affected UML DERIVED ATTRIBUTES, written with a leading
# slash (`/age`, `+/total: int`). This is standard notation:
# UML 2.5.1 §9.5.4; also used by Fowler in UML Distilled. Silently losing
# derived attributes made classes appear anemic and corrupted granularity
# and signature counts. Accept the slash and PRESERVE its meaning:
# derived is semantic rather than decorative.
# The value is derivable from other information. Storage, caching and indexing
# remain separate design decisions.
_MOD = r'(?:\{[^}]*\}\s*)?'
_TIPO = r'[\w<>\[\]\., ]+?'
_COLA = r'(?:\s*\[[^\]]*\])?(?:\s*=\s*[^{}\n]+?)?(?:\s*\{[^}]*\})?'
_NOMBRE = r'[A-Za-zÁÉÍÓÚÑáéíóúñ_][\wÁÉÍÓÚÑáéíóúñ]*'
ATRIB_RE = re.compile(
    rf'^\s*{_MOD}(?P<vis>[+\-#~])?\s*{_MOD}'
    rf'(?P<derivado>/)?\s*'
    rf'(?P<nombre>{_NOMBRE})'
    rf'\s*(?::\s*(?P<tipo>{_TIPO}))?{_COLA}\s*$'
)
OPER_RE = re.compile(
    rf'^\s*{_MOD}(?P<vis>[+\-#~])?\s*{_MOD}'
    rf'(?P<nombre>{_NOMBRE})'
    rf'\s*\((?P<params>[^)]*)\)'
    rf'\s*(?::\s*(?P<retorno>{_TIPO}))?{_COLA}\s*$'
)
RECEPCION_RE = re.compile(
    rf'^\s*{_MOD}(?P<vis>[+\-#~])?\s*<<\s*signal\s*>>\s*'
    rf'(?P<nombre>{_NOMBRE})\s*\((?P<params>[^)]*)\)\s*$', re.IGNORECASE,
)
# Class relationships accept PlantUML direction hints
# (`-up-|>`, `-down-`, `-left-`, `-right-`) and color (`#--`):
# equivalent relationship forms. Ignoring them mislabeled legitimate
# specializations as classes without provenance, undermining the very
# mechanism this validator is intended to enforce.
REL_RE = re.compile(
    r'^\s*(?P<izq>"[^"]+"|[\w]+)\s*(?:"[^"]*"\s*)?'
    r'(?P<conn>[<>ox|*.#\-]*(?:up|down|left|right)?[<>ox|*.#\-]*)'
    r'\s*(?:"[^"]*"\s*)?(?P<der>"[^"]+"|[\w]+)\s*(?::\s*(?P<etiqueta>.*))?$',
    re.MULTILINE,
)
DIRECCION_RE = re.compile(r'-(?:up|down|left|right)-')
# Sequence messages for operation provenance.
MSG_SEC_RE = re.compile(
    r'^\s*(?:"[^"]+"|[\w]+)\s*(?:--?>>?|<<?--?)\s*(?:"[^"]+"|[\w]+)'
    r'(?:\s*(?:\+\+|--|\*\*|!!))?\s*(?::\s*(?P<etiqueta>.*))?$',
    re.MULTILINE,
)


def strip_accents(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t or "")
                   if unicodedata.category(c) != "Mn")


def norm(t: str) -> str:
    return strip_accents(t or "").strip().lower()


def camel_split(text: str) -> str:
    """Split CamelCase: 'RecordDAOFactory' -> 'Record DAO Factory'.

    Whole-word matching needs this: joined names otherwise evade detection,
    while substring matching overfires ('api' occurs within Spanish 'Terapia').
    Split both sides and use word boundaries to avoid both failures.
    """
    t = re.sub(r"(?<=[a-z0-9])(?=[A-ZÁÉÍÓÚÑ])", " ", text or "")
    t = re.sub(r"(?<=[A-ZÁÉÍÓÚÑ])(?=[A-ZÁÉÍÓÚÑ][a-záéíóúñ])", " ", t)
    return re.sub(r"[_\-.]+", " ", t)


def contiene_termino(nombre: str, terminos) -> str | None:
    frase = " ".join(camel_split(nombre).split()).lower()
    for t in terminos:
        aguja = " ".join(camel_split(t).split()).lower()
        if re.search(rf"(?<![\w]){re.escape(aguja)}(?![\w])", frase):
            return t
    return None


def clave(text: str) -> str:
    """Identity key for a class, lifeline, or relationship endpoint.

    `m.clases` is indexed by this key; collisions overwrite earlier entries.
    Removing stopwords matches 'Record of Incident' with 'RecordIncident'.
    An empty key, however, makes ALL affected names collide: a class silently
    disappears, its operations are skipped, and counts become unreliable.
    Last declaration wins arbitrarily, hiding either valid or defective classes.
    Two empty-key paths are handled:

    1. Names containing only stopwords (`El`, `Un`, `De La`, and common aliases
       `A`/`B`) fall back to unfiltered pieces.
    2. The [a-z0-9] filter erases names in other alphabets, leaving `piezas`
       empty too. Raw normalized text is the final fallback.

    Any stable key is preferable to '', which collides with every other empty key.
    """
    t = re.sub(r"[^a-z0-9 ]+", " ", norm(text))
    piezas = [w for w in t.split() if w]
    sin_stop = [w for w in piezas if w not in STOPWORDS]
    return "".join(sin_stop or piezas) or re.sub(r"\s+", "", norm(text))


def similitud(a: str, b: str) -> float:
    a, b = clave(a), clave(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    ga = {a[i:i + 2] for i in range(len(a) - 1)}
    gb = {b[i:i + 2] for i in range(len(b) - 1)}
    if not ga or not gb:
        return 0.0
    return 2 * len(ga & gb) / (len(ga) + len(gb))


def palabras(text: str) -> set[str]:
    t = re.sub(r"[^a-z0-9 ]+", " ", norm(camel_split(text)))
    return {w for w in t.split() if len(w) > 2 and w not in STOPWORDS}


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class Miembro:
    nombre: str
    visibilidad: str
    linea: int
    tipo: str = ""          # attribute type or operation return type
    params: str = ""
    es_operacion: bool = False
    derivado: bool = False  # UML derived attribute: written `/name`, meaning
                            # computed from other information; storage is unspecified


@dataclass
class Clase:
    nombre: str
    linea: int
    abstracta: bool = False
    kind: str = "class"     # class | interface | enum
    estereotipos: set = field(default_factory=set)
    atributos: list = field(default_factory=list)
    operaciones: list = field(default_factory=list)
    recepciones: list = field(default_factory=list)  # Signal receptions, not Operations
    no_parseadas: list = field(default_factory=list)   # (line, text)

    @property
    def es_abstracta(self) -> bool:
        # `abstract class X` and `class X <<abstract>>` are equivalent. Recognizing
        # only the former caused stereotype-declared abstract classes to trigger
        # false anemia findings.
        return self.abstracta or any('abstract' in norm(e) for e in self.estereotipos)

    @property
    def es_solucion(self) -> bool:
        return any("solucion" in norm(e) or "solution" in norm(e)
                   for e in self.estereotipos)


@dataclass
class Modelo:
    path: str
    text: str
    clases: dict = field(default_factory=dict)
    relaciones: list = field(default_factory=list)
    aliases: dict = field(default_factory=dict)  # PlantUML identifier -> visible name


# --------------------------------------------------------------------------
# Parsers
# --------------------------------------------------------------------------

def cuerpo_de_clase(text: str, desde: int) -> tuple[str, int]:
    """Return the {...} body beginning after `desde` and its end position."""
    resto = text[desde:]
    if not resto.lstrip().startswith("{"):
        return "", desde
    inicio = desde + resto.index("{")
    prof, i = 0, inicio
    while i < len(text):
        if text[i] == "{":
            prof += 1
        elif text[i] == "}":
            prof -= 1
            if prof == 0:
                return text[inicio + 1:i], i + 1
        i += 1
    return text[inicio + 1:], len(text)


def parse_clases(path: str, text: str) -> Modelo:
    m = Modelo(path=path, text=text)
    for mc in CLASE_RE.finditer(text):
        nombre = mc.group("q") or mc.group("n") or ""
        linea = text[: mc.start()].count("\n") + 1
        estereotipos = set(re.findall(r"<<([^>]+)>>", mc.group("estereotipos") or ""))
        c = Clase(
            nombre=nombre, linea=linea,
            abstracta=bool(mc.group("abstracta")),
            kind=mc.group("tipo").lower(),
            estereotipos=estereotipos,
        )
        cuerpo, _fin = cuerpo_de_clase(text, mc.end())
        base = text[: mc.end()].count("\n") + 1
        for off, cruda in enumerate(cuerpo.split("\n"), start=1):
            ln = cruda.strip()
            if not ln or ln.startswith("'") or ln.startswith(".."):
                continue
            if ln.startswith("--") or ln.startswith("=="):
                continue  # compartment separators
            n_linea = base + off
            mr = RECEPCION_RE.match(ln)
            if mr:
                c.recepciones.append(Miembro(
                    nombre=mr.group("nombre"), visibilidad=mr.group("vis") or "",
                    linea=n_linea, params=(mr.group("params") or "").strip()))
                continue
            mo = OPER_RE.match(ln)
            if mo:
                c.operaciones.append(Miembro(
                    nombre=mo.group("nombre"), visibilidad=mo.group("vis") or "",
                    linea=n_linea, tipo=(mo.group("retorno") or "").strip(),
                    params=(mo.group("params") or "").strip(), es_operacion=True))
                continue
            ma = ATRIB_RE.match(ln)
            if ma:
                c.atributos.append(Miembro(
                    nombre=ma.group("nombre"), visibilidad=ma.group("vis") or "",
                    linea=n_linea, tipo=(ma.group("tipo") or "").strip(),
                    derivado=bool(ma.group("derivado"))))
                continue
            # RECORD unparsed body lines instead of discarding them: silently lost
            # members corrupt all dependent counts (anemia, granularity, signatures)
            # while otherwise leaving no evidence that a member was lost.
            # Retain the location and text for a diagnostic.
            c.no_parseadas.append((n_linea, ln))
        m.clases[clave(nombre)] = c
        if mc.group("alias"):
            m.aliases[mc.group("alias")] = nombre

    # Normalize direction hints BEFORE matching relationships, on a copy with
    # the same line count, so source locators remain stable.
    # Preserve source-line correspondence.
    texto_rel = DIRECCION_RE.sub("-", text)
    for mr in REL_RE.finditer(texto_rel):
        conn = mr.group("conn") or ""
        if len(re.sub(r"[^<>ox|*.\-]", "", conn)) < 2:
            continue                       # not a relationship connector
        izq = mr.group("izq").strip('"')
        der = mr.group("der").strip('"')
        izq = m.aliases.get(izq, izq)
        der = m.aliases.get(der, der)
        if izq.lower() in ("startuml", "enduml") or der.lower() in ("startuml", "enduml"):
            continue
        m.relaciones.append((izq, der, conn,
                             texto_rel[: mr.start()].count("\n") + 1))
    return m


def parse_dominio(text: str) -> dict:
    """Return {key: (original_name, {attributes})} from the domain model."""
    out = {}
    for mc in CLASE_RE.finditer(text):
        nombre = mc.group("q") or mc.group("n") or ""
        cuerpo, _ = cuerpo_de_clase(text, mc.end())
        attrs = set()
        for cruda in cuerpo.split("\n"):
            ln = cruda.strip()
            if not ln or ln.startswith("'") or "(" in ln:
                continue
            ma = ATRIB_RE.match(ln)
            if ma:
                attrs.add(norm(ma.group("nombre")))
        out[clave(nombre)] = (nombre, attrs)
    return out


def parse_generalizaciones(mod: Modelo) -> dict:
    """Return {child_key: parent_key} from inheritance relationships.

    A subclass discovered during design (the book's 'opportunity for
    generalization') is absent from the domain but is not solution space:
    it traces to the problem through its parent. Otherwise legitimate new
    hierarchies would be incorrectly reported as classes without provenance.
    """
    padres = {}
    for izq, der, conn, _n in mod.relaciones:
        ki, kd = clave(izq), clave(der)
        if "<|" in conn:          # Parent <|-- Child
            padres[kd] = ki
        elif "|>" in conn:        # Child --|> Parent
            padres[ki] = kd
    return padres


def traza_al_dominio(k: str, dominio: dict, padres: dict, vistos=None) -> bool:
    """True if the key is in the domain or transitively inherits from a domain class."""
    if k in dominio:
        return True
    vistos = vistos or set()
    if k in vistos:
        return False              # stop inheritance cycles
    vistos.add(k)
    padre = padres.get(k)
    return bool(padre) and traza_al_dominio(padre, dominio, padres, vistos)


def parse_relaciones_dominio(text: str) -> set:
    pares = set()
    for mr in REL_RE.finditer(text):
        izq = clave(mr.group("izq").strip('"'))
        der = clave(mr.group("der").strip('"'))
        if izq and der:
            pares.add(frozenset({izq, der}))
    return pares


MSG_DIR_RE = re.compile(
    r'^\s*(?P<emisor>"[^"]+"|[\w]+)\s*(?P<flecha>--?>>?|<<?--?)\s*'
    r'(?P<receptor>"[^"]+"|[\w]+)'
    r'(?:\s*(?P<corto>\+\+|--|\*\*|!!))?\s*(?::\s*(?P<etiqueta>.*))?$',
    re.MULTILINE,
)
DECL_SEC_RE = re.compile(
    r'^\s*(?:create\s+)?(?:actor|boundary|control|entity|participant|database|collections|queue)\s+'
    r'(?:"(?P<label>[^"]+)"|(?P<bare>[\w]+))(?:\s+as\s+(?P<alias>[\w]+))?',
    re.IGNORECASE | re.MULTILINE,
)


SORT_SEC_RE = re.compile(
    r'<<\s*(synchCall|asynchCall|reply|asynchSignal|createMessage|deleteMessage)\s*>>',
    re.IGNORECASE,
)
CREATE_SEC_RE = re.compile(
    r'^\s*create\s+(?:(?:participant|actor|boundary|control|entity|database|queue|collections)\s+)?'
    r'(?P<quien>"[^"]+"|[\w]+)(?:\s+as\s+(?P<alias>[\w]+))?'
    r'(?:\s+(?:#[#\w]+|<<[^>]+>>))*\s*$', re.IGNORECASE,
)


def etiqueta_de_llamada(mm, creaciones: set) -> tuple[str, bool]:
    """Return (call label, unresolved async); a Signal is not an Operation."""
    et = (mm.group("etiqueta") or "").strip()
    flecha = mm.group("flecha") or ""
    receptor = mm.group("emisor") if flecha.startswith("<") else mm.group("receptor")
    receptor = receptor.strip('"')
    if receptor in creaciones:
        creaciones.remove(receptor)
        return "", False
    if mm.group("corto") in ("**", "!!"):
        return "", False
    sorts = {norm(m.group(1)) for m in SORT_SEC_RE.finditer(et)}
    if sorts:
        if len(sorts) != 1 or not sorts <= {"synchcall", "asynchcall"}:
            return "", False
        etiqueta = SORT_SEC_RE.sub("", et).strip()
        if not re.match(r"^[A-Za-z_][\w]*\s*\(", etiqueta):
            return "", False
        return etiqueta, False
    if "--" in flecha:
        return "", False
    if ">>" in flecha or "<<" in flecha:
        return "", bool(et)
    return et, False


def codigo_mensajes(text: str) -> str:
    """Blank block comments and notes without changing message line numbers."""
    text = re.sub(r"^[ \t]*/'[\s\S]*?(?:'/|\Z)",
                  lambda m: "\n" * m.group().count("\n"), text, flags=re.MULTILINE)
    lineas, en_nota = [], False
    for crudo in text.split("\n"):
        ln = crudo.strip()
        if en_nota:
            if re.match(r"^end\s*note\b", ln, re.IGNORECASE):
                en_nota = False
            lineas.append("")
        elif re.match(r"^(?:h|r)?note\b", ln, re.IGNORECASE):
            en_nota = ":" not in ln and not re.search(r"\bend\s*note\b", ln, re.IGNORECASE)
            lineas.append("")
        else:
            lineas.append("" if ln.startswith("'") else crudo)
    return "\n".join(lineas)


def parse_mensajes(text: str, avisos=None) -> tuple:
    """Return (global_vocabulary, {class_key: {vocabulary addressed to it}}).

    Receiver-specific vocabulary checks the provenance promise: operations
    originate in messages **addressed to that class**. A global bag accepts
    the book's Queue defect: an operation placed on the wrong class.
    """
    text = codigo_mensajes(text)
    alias = {}
    for md in DECL_SEC_RE.finditer(text):
        etiqueta = md.group("label") or md.group("bare") or ""
        a = md.group("alias") or md.group("bare") or etiqueta
        if a:
            alias[a] = etiqueta

    voc, por_receptor, creaciones = set(), {}, set()
    for linea, cruda in enumerate(text.split("\n"), 1):
        mc = CREATE_SEC_RE.match(cruda)
        if mc:
            creaciones.add(mc.group("alias") or mc.group("quien").strip('"'))
            continue
        mm = MSG_DIR_RE.match(cruda)
        if not mm:
            continue
        et, sin_resolver = etiqueta_de_llamada(mm, creaciones)
        if sin_resolver and avisos is not None:
            avisos.append(f"L{linea}: unresolved asynchronous message provenance; declare "
                          f"<<asynchCall>> with an Operation signature or <<asynchSignal>>.")
        if not et:
            continue
        p = palabras(et)
        mfun = re.match(r"^([A-Za-z_][\w]*)\s*\(", et)
        if mfun:
            p.add(norm(mfun.group(1)))
        voc |= p
        emisor = mm.group("emisor").strip('"')
        receptor = mm.group("receptor").strip('"')
        if (mm.group("flecha") or "").startswith("<"):
            emisor, receptor = receptor, emisor
        destino = alias.get(receptor, receptor)
        por_receptor.setdefault(clave(destino), set()).update(p)
    return voc, por_receptor


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_modelo_vacio(mod: Modelo, errores: list) -> bool:
    """A model without classes cannot be declared ready.

    Without this check, an empty file or bare @startuml returned READY FOR CDR
    and exit 0: provenance metrics were zero only because nothing could fail.
    A favorable verdict on an empty artifact manufactures confidence.
    """
    if not mod.clases:
        errores.append(
            f"[{mod.path}] the model declares no classes. There is nothing to "
            f"validate or take to the CDR."
        )
        return True
    return False


def check_lineas_no_parseadas(mod: Modelo, avisos: list) -> None:
    """An unparsed member PREVENTS model certification.

    This remains a warning: the model may be valid and the parser incomplete.
    However, `hay_miembros_perdidos` blocks a favorable verdict because missing
    members invalidate dependent anemia, granularity, and signature counts.
    Certifying explicitly unreliable metrics would manufacture confidence,
    exactly what `check_modelo_vacio` also prevents.
    """
    for c in mod.clases.values():
        for n, texto in c.no_parseadas:
            avisos.append(
                f"[{mod.path}] L{n}: could not parse this member of "
                f"'{c.nombre}': «{texto[:60]}». It was counted as neither attribute nor "
                f"operation, so counts for this class are unreliable "
                f"and the model CANNOT be certified until this is resolved."
            )


def hay_miembros_perdidos(mod: Modelo) -> bool:
    """True if any class body contains unparsed lines."""
    return any(c.no_parseadas for c in mod.clases.values())


def check_directivas(mod: Modelo, avisos: list) -> None:
    tag = f"[{mod.path}]"
    if not mod.text.lstrip().startswith("@startuml"):
        avisos.append(f"{tag} the script should start with @startuml")
    for d in REQUIRED_DIRECTIVES:
        if d not in mod.text:
            avisos.append(f"{tag} missing contract directive: {d}")
    if re.search(r"^\s*hide\s+methods", mod.text, re.MULTILINE):
        avisos.append(
            f"{tag} the model declares 'hide methods', intended for DOMAIN models; "
            f"operations are the primary contribution here and must be visible."
        )


def check_accesores(mod: Modelo, avisos: list) -> None:
    """Anti-pattern 11: getters and setters in the model."""
    tag = f"[{mod.path}]"
    for c in mod.clases.values():
        hallados = [o for o in c.operaciones if ACCESOR_RE.match(o.nombre)]
        if hallados:
            ejemplo = ", ".join(o.nombre for o in hallados[:3])
            avisos.append(
                f"{tag} L{c.linea}: class '{c.nombre}' declares {len(hallados)} "
                f"accessor(s) ({ejemplo}). The source discourages them: they are generated "
                f"from attributes and only clutter the diagram."
            )


def check_procedencia_clases(mod: Modelo, dominio: dict, errores: list,
                             avisos: list, infos: list) -> int:
    """Central rule: each class traces to the domain or is declared as solution space."""
    tag = f"[{mod.path}]"
    padres = parse_generalizaciones(mod)
    sin_procedencia = 0
    for c in mod.clases.values():
        if c.kind == 'enum':
            continue          # a design enum is not a domain class
        k = clave(c.nombre)
        if k in dominio:
            continue                      # problem-space class
        if traza_al_dominio(k, dominio, padres):
            # Design specialization traces to the domain through its parent:
            # one of the three opportunities the source asks designers to seek.
            infos.append(
                f"design specialization: '{c.nombre}' (L{c.linea}) inherits from a "
                f"domain class and therefore traces to the problem space"
            )
            continue
        if c.es_solucion:
            infos.append(
                f"declared SOLUTION-space class: '{c.nombre}' "
                f"(L{c.linea})"
            )
            continue
        # Neither in the domain nor declared: anti-pattern 2.
        sin_procedencia += 1
        pista = contiene_termino(c.nombre, TERMINOS_SOLUCION)
        extra = (f" Its name suggests infrastructure ('{pista}'): if so, "
                 f"mark it <<solution>>." if pista else "")
        errores.append(
            f"{tag} L{c.linea}: class '{c.nombre}' is absent from the domain "
            f"model and lacks <<solution>>. Every class must trace to the problem "
            f"or be declared as solution space; silently mixing them destroys "
            f"traceability.{extra}"
        )
        # Vocabulary drift: possibly a renamed domain class.
        for dk, (dnombre, _a) in dominio.items():
            s = similitud(k, dk)
            if s >= SIMILITUD_DERIVA:
                avisos.append(
                    f"{tag} L{c.linea}: possible vocabulary drift: '{c.nombre}' "
                    f"resembles domain class '{dnombre}' (similarity {s:.2f}). "
                    f"Confirm whether they represent the same concept before adding a class."
                )
    return sin_procedencia


def check_dominio_completo(mod: Modelo, dominio: dict, avisos: list) -> None:
    """No domain class disappears without justification."""
    presentes = set(mod.clases.keys())
    for k, (nombre, _a) in sorted(dominio.items()):
        if k not in presentes:
            avisos.append(
                f"[{mod.path}] class '{nombre}' exists in the domain model but "
                f"not in the design model. It may belong to another use case; "
                f"declare that scope explicitly."
            )


def check_procedencia_operaciones(mod: Modelo, voc_mensajes: set,
                                  por_receptor: dict, hay_secuencia: bool,
                                  errores: list, avisos: list) -> int:
    """Every operation originates in a message ADDRESSED TO ITS CLASS.

    Two levels:
      - absent from ALL messages -> ERROR: no source
      - present but addressed to ANOTHER class -> WARNING: misplaced operation,
        the book's Queue defect
    The latter is a warning because class/lifeline matching is heuristic:
    a lifeline may have a different name from its class.
    """
    if not hay_secuencia:
        return 0
    tag = f"[{mod.path}]"
    padres = parse_generalizaciones(mod)
    huerfanas = 0
    for c in mod.clases.values():
        propio = por_receptor.get(clave(c.nombre), set())
        # A subclass inherits ancestor provenance. Overriding does not require
        # a separate message addressed to the subclass: messages target the
        # general type; specialization is a design decision.
        k, guard = clave(c.nombre), set()
        while k in padres and k not in guard:
            guard.add(k)
            k = padres[k]
            propio |= por_receptor.get(k, set())
            padre_cls = mod.clases.get(k)
            if padre_cls:
                propio |= {norm(op.nombre) for op in padre_cls.operaciones}
        for o in c.operaciones:
            if ACCESOR_RE.match(o.nombre):
                continue                  # warned separately
            p = palabras(o.nombre) | {norm(o.nombre)}
            if p & propio:
                continue
            if p & voc_mensajes:
                avisos.append(
                    f"{tag} L{o.linea}: '{c.nombre}.{o.nombre}()' appears in the "
                    f"sequence diagrams, but NOT as a message addressed to "
                    f"'{c.nombre}'. It may be on the wrong class: the defect "
                    f"illustrated by the class that can only add and never "
                    f"remove."
                )
                continue
            huerfanas += 1
            errores.append(
                f"{tag} L{o.linea}: operation '{c.nombre}.{o.nombre}()' does not "
                f"match any message in the supplied sequence diagrams. "
                f"Revisit the sequence: if the behavior is needed, "
                f"the message is missing; otherwise the operation is unnecessary."
            )
    return huerfanas


def check_procedencia_atributos(mod: Modelo, dominio: dict, voc_spec: set,
                                hay_spec: bool, avisos: list) -> None:
    if not hay_spec:
        return
    tag = f"[{mod.path}]"
    for c in mod.clases.values():
        if c.es_solucion or c.kind == 'enum':
            continue          # design attributes / enum literals
        attrs_dom = dominio.get(clave(c.nombre), ("", set()))[1]
        for a in c.atributos:
            if norm(a.nombre) in attrs_dom:
                continue
            if palabras(a.nombre) & voc_spec or norm(a.nombre) in voc_spec:
                continue
            avisos.append(
                f"{tag} L{a.linea}: attribute '{c.nombre}.{a.nombre}' appears in neither "
                f"the domain model nor the specification text. "
                f"Attributes derive from use case details."
            )


def check_relaciones(mod: Modelo, rel_dominio: set, dominio: dict,
                     hay_dominio: bool, avisos: list) -> None:
    if not hay_dominio or not rel_dominio:
        return
    tag = f"[{mod.path}]"
    for izq, der, _conn, n in mod.relaciones:
        ki, kd = clave(izq), clave(der)
        # Check only relationships between PROBLEM classes. Relationships involving
        # solution classes arise from design by definition.
        ci = mod.clases.get(ki)
        cd = mod.clases.get(kd)
        if not ci or not cd or ci.es_solucion or cd.es_solucion:
            continue
        if ki not in dominio or kd not in dominio:
            continue
        if frozenset({ki, kd}) not in rel_dominio:
            avisos.append(
                f"{tag} L{n}: relationship '{izq}' - '{der}' joins two domain "
                f"classes but is absent from the domain model. Relationships come from the domain "
                f"or an operation requirement; declare the latter explicitly."
            )


def check_anemia(mod: Modelo, dominio: dict, avisos: list) -> None:
    """Anti-patterns 4, 6, and 7."""
    tag = f"[{mod.path}]"
    for c in mod.clases.values():
        if c.kind != "class" or c.es_abstracta:
            continue
        del_dominio = clave(c.nombre) in dominio
        if del_dominio and c.atributos and not c.operaciones:
            avisos.append(
                f"{tag} L{c.linea}: '{c.nombre}' is a domain class with "
                f"{len(c.atributos)} attribute(s) and NO operations. This suggests "
                f"an anemic domain model: check whether its behavior "
                f"was placed in a controller or service."
            )
        if del_dominio and not c.atributos and not c.es_solucion:
            avisos.append(
                f"{tag} L{c.linea}: entity '{c.nombre}' declares no "
                f"attributes. This is the last opportunity to add them before coding."
            )


def check_granularidad(mod: Modelo, avisos: list) -> None:
    """Anti-patterns 8 and 9. Thresholds are conventions, not evidence."""
    tag = f"[{mod.path}]"
    for c in mod.clases.values():
        if len(c.operaciones) > MAX_OPERACIONES:
            avisos.append(
                f"{tag} L{c.linea}: '{c.nombre}' declares {len(c.operaciones)} "
                f"operations (convention threshold: {MAX_OPERACIONES}). God-class "
                f"candidate: apply the discordant attributes test."
            )
        if len(c.atributos) > MAX_ATRIBUTOS:
            avisos.append(
                f"{tag} L{c.linea}: '{c.nombre}' declares {len(c.atributos)} attributes "
                f"(convention threshold: {MAX_ATRIBUTOS}). Check for multiple "
                f"responsibilities."
            )
    # A swarm is PROLIFERATION of tiny classes. Two legitimate low-operation
    # cases must be excluded:
    #   - a subclass overriding only varying behavior (good design)
    #   - a single-purpose solution class
    # Counting these as a swarm falsely flagged sound hierarchies.
    hijos = set(parse_generalizaciones(mod).keys())
    reales = [c for c in mod.clases.values()
              if c.kind == "class" and not c.es_solucion
              and clave(c.nombre) not in hijos]
    if len(reales) >= MIN_CLASES_ENJAMBRE:
        minimas = [c for c in reales if len(c.operaciones) <= 1]
        prop = len(minimas) / len(reales)
        if prop > MAX_PROP_CLASES_MINIMAS:
            avisos.append(
                f"{tag} {len(minimas)} of {len(reales)} classes have one operation or "
                f"none ({prop:.0%}). Possible overnormalization: a swarm of "
                f"tiny classes is as problematic as a monolithic class."
            )


def check_firmas(mod: Modelo, avisos: list) -> None:
    """CDR guideline #3: complete types, returns, and parameters."""
    tag = f"[{mod.path}]"
    for c in mod.clases.values():
        if c.kind == 'enum':
            continue          # enum literals do not declare a type
        for a in c.atributos:
            if not a.tipo:
                avisos.append(
                    f"{tag} L{a.linea}: attribute '{c.nombre}.{a.nombre}' declares no "
                    f"type. CDR requires correctly typed attributes."
                )
        for o in c.operaciones:
            if not o.tipo:
                avisos.append(
                    f"{tag} L{o.linea}: operation '{c.nombre}.{o.nombre}()' does not "
                    f"declare a return type. CDR requires complete parameter lists and "
                    f"return types."
                )
            if o.params and not re.search(r":", o.params):
                avisos.append(
                    f"{tag} L{o.linea}: parameters of '{c.nombre}.{o.nombre}()' are not "
                    f"typed."
                )


def check_patrones(mod: Modelo, voc_mensajes: set, hay_secuencia: bool,
                   avisos: list) -> None:
    """Anti-pattern 10: pattern without provenance.

    Patterns are welcome here: pre-CDR cleanup includes 'identifying useful
    design patterns'. Flag only patterns required by no sequence message.
    """
    if not hay_secuencia:
        return
    tag = f"[{mod.path}]"
    for c in mod.clases.values():
        hit = contiene_termino(c.nombre, TERMINOS_PATRON)
        if not hit:
            continue
        if palabras(c.nombre) & voc_mensajes:
            continue                       # pattern appears in the sequence
        avisos.append(
            f"{tag} L{c.linea}: '{c.nombre}' introduces pattern '{hit}', but no "
            f"sequence message mentions it. Patterns are welcome at this "
            f"stage, but must emerge from design rather than a catalog."
        )


def check_delta_completo(mod: Modelo, voc_mensajes: set, hay_secuencia: bool,
                         avisos: list) -> None:
    """Anti-pattern 14: CDR entry criterion."""
    if not hay_secuencia or not voc_mensajes:
        return
    declaradas = set()
    for c in mod.clases.values():
        for o in c.operaciones:
            declaradas |= palabras(o.nombre) | {norm(o.nombre)}
    sin_reflejar = sorted(voc_mensajes - declaradas)
    # Warn only for a substantial gap: message vocabulary includes label words,
    # not just operation names.
    if len(sin_reflejar) > len(voc_mensajes) * 0.6:
        avisos.append(
            f"[{mod.path}] CDR ENTRY CRITERION: much of the vocabulary in "
            f"sequence messages does not "
            f"appear in model operations. The CDR entry criterion "
            f"requires all operations allocated in sequences to be "
            f"reflected in the static model."
        )


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def leer(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        raise SystemExit(2)


def validar(mod, dominio, rel_dominio, voc_mensajes, por_receptor, voc_spec,
            hay_dominio, hay_secuencia, hay_spec):
    errores, avisos, infos = [], [], []
    capas, degradadas = {}, []

    if check_modelo_vacio(mod, errores):
        capas["modelo vacio"] = "ejecutada"
        return errores, avisos, infos, {
            "clases_sin_procedencia": None, "operaciones_sin_mensaje": None}, capas, []

    check_lineas_no_parseadas(mod, avisos)
    check_directivas(mod, avisos)
    check_accesores(mod, avisos)
    check_granularidad(mod, avisos)
    check_firmas(mod, avisos)
    capas["notacion y contrato"] = "ejecutada"
    capas["granularidad y firmas"] = "ejecutada"

    if hay_dominio:
        sin_proc = check_procedencia_clases(mod, dominio, errores, avisos, infos)
        check_dominio_completo(mod, dominio, avisos)
        check_relaciones(mod, rel_dominio, dominio, hay_dominio, avisos)
        check_anemia(mod, dominio, avisos)
        capas["procedencia de clases"] = "ejecutada"
        capas["procedencia de relaciones"] = "ejecutada"
        capas["anemia y responsabilidades"] = "ejecutada"
    else:
        sin_proc = 0
        for c in ("procedencia de clases", "procedencia de relaciones",
                  "anemia y responsabilidades"):
            capas[c] = "NO EJECUTADA - falta el modelo de dominio"
        degradadas += list(("procedencia de clases", "procedencia de relaciones",
                            "anemia y responsabilidades"))

    if hay_secuencia:
        huerfanas = check_procedencia_operaciones(
            mod, voc_mensajes, por_receptor, True, errores, avisos)
        check_patrones(mod, voc_mensajes, True, avisos)
        check_delta_completo(mod, voc_mensajes, True, avisos)
        capas["procedencia de operaciones"] = "ejecutada"
    else:
        huerfanas = 0
        capas["procedencia de operaciones"] = "NO EJECUTADA - falta el diagrama de secuencia"
        degradadas.append("procedencia de operaciones")

    if hay_spec:
        check_procedencia_atributos(mod, dominio, voc_spec, True, avisos)
        capas["procedencia de atributos"] = "ejecutada"
    else:
        capas["procedencia de atributos"] = "NO EJECUTADA - falta la especificacion"
        degradadas.append("procedencia de atributos")

    metricas = {
        "clases_sin_procedencia": sin_proc if hay_dominio else None,
        "operaciones_sin_mensaje": huerfanas if hay_secuencia else None,
    }
    return errores, avisos, infos, metricas, capas, degradadas


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
        description="Validate the design class model against its source artifacts."
    )
    p.add_argument("--clases", required=True, help="design class model (.puml)")
    p.add_argument("--dominio", help="domain model (.puml)")
    p.add_argument("--secuencia", action="append", default=[],
                   help="sequence diagram (.puml); repeatable.")
    p.add_argument("--spec", action="append", default=[],
                   help="use case specification (.md); repeatable.")
    args = p.parse_args(argv)

    mod = parse_clases(args.clases, leer(args.clases))
    dom_text = leer(args.dominio) if args.dominio else ""
    dominio = parse_dominio(dom_text) if args.dominio else {}
    rel_dominio = parse_relaciones_dominio(dom_text) if args.dominio else set()

    voc_mensajes, por_receptor, avisos_semanticos = set(), {}, []
    for s in args.secuencia:
        avisos_archivo = []
        v, pr = parse_mensajes(leer(s), avisos_archivo)
        avisos_semanticos.extend(f"[{s}] {a}" for a in avisos_archivo)
        voc_mensajes |= v
        for k, vals in pr.items():
            por_receptor.setdefault(k, set()).update(vals)
    voc_spec = set()
    for s in args.spec:
        t = leer(s)
        voc_spec |= palabras(t)
        voc_spec |= {norm(w) for w in re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ_]{3,}", t)}

    errores, avisos, infos, metricas, capas, degradadas = validar(
        mod, dominio, rel_dominio, voc_mensajes, por_receptor, voc_spec,
        hay_dominio=bool(args.dominio), hay_secuencia=bool(args.secuencia),
        hay_spec=bool(args.spec),
    )
    avisos.extend(avisos_semanticos)

    n_ops = sum(len(c.operaciones) for c in mod.clases.values())
    n_recepciones = sum(len(c.recepciones) for c in mod.clases.values())
    n_attrs = sum(len(c.atributos) for c in mod.clases.values())
    n_sol = sum(1 for c in mod.clases.values() if c.es_solucion)

    print("Design class model validation")
    print("=" * 42)
    print(f"Classes: {len(mod.clases)} ({n_sol} solution-space) | "
          f"Attributes: {n_attrs} | Operations: {n_ops} | Receptions: {n_recepciones} | "
          f"Relationships: {len(mod.relaciones)}")
    print(f"Domain classes: {len(dominio)} | Sequences: {len(args.secuencia)} | "
          f"Specifications: {len(args.spec)}")
    print()

    print("PROVENANCE")
    for etiqueta, k in (("classes without provenance ..", "clases_sin_procedencia"),
                        ("operations without message ..", "operaciones_sin_mensaje")):
        v = metricas[k]
        print(f"  {etiqueta} {'n/a' if v is None else v}   (target: 0)")
    print()

    print("LAYERS")
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

    perdidos = hay_miembros_perdidos(mod)

    if degradadas:
        print("STATUS: NOT FULLY VERIFIED")
        print(f"  {len(degradadas)} layer(s) not executed due to missing inputs: "
              f"{', '.join(DISPLAY_LABELS.get(c, c) for c in degradadas)}")
    elif errores:
        print("STATUS: NOT READY FOR CDR")
    elif perdidos:
        # The model may be valid, but the validator cannot certify counts that
        # its own report explicitly declared unreliable.
        # Require parser gaps to be resolved first.
        print("STATUS: CANNOT CERTIFY")
        print("  Some class members could not be parsed. Anemia, granularity, and "
              "signature counts depend on them; none of these metrics can "
              "represent the model reliably until those gaps are resolved.")
    else:
        print("STATUS: READY FOR CDR (subject to your review of warnings)")
    print()
    print("Remember: errors violate provenance rules; "
          "warnings require your judgment. Granularity thresholds are "
          "skill conventions, not evidence from a source.")

    return 1 if (errores or perdidos) else 0


if __name__ == "__main__":
    raise SystemExit(main())
