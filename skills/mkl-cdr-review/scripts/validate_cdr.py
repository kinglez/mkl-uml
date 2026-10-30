#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
# Modification notice: distinguish operation calls from replies, Signals and lifecycle events.
# Modification notice: preserve typed create declarations and separate Signal receptions.
"""Critical Design Review Validator (CDR, MKL, step 8).

Automates preparation checks for a technical review. The user determines the
review disposition; automated coverage does not replace human inspection.

Usage:
    python validate_cdr.py --clases model_design_classes.puml \\
        --secuencia case_01_sequence.puml [--secuencia ...] \\
        [--spec case_01_specification.md ...] \\
        [--robustez case_01_robustez.puml ...] \\
        [--dominio domain_model.puml] \\
        [--requisitos requirements.md] \\
        [--pruebas test_plan.md]

Only --clases and --secuencia are required. Each absent input deactivates
specific rules, which are declared as NOT EXECUTED in the output and downgrade
the status.

Message provenance: annotate labels with <<synchCall>>, <<asynchCall>>,
<<reply>>, <<asynchSignal>>, <<createMessage>> or <<deleteMessage>>.
Explicit call annotations require an operation signature, such as approve().
Unannotated solid synchronous arrows retain lexical call matching; ambiguous
asynchronous messages require manual classification and provide no operation
evidence. Reply, Signal and lifecycle labels do not establish operations.

Exit codes:
    0 no errors (warnings may occur)
    1 there are errors: the design cannot proceed to code
    2 usage error or file not found
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# NUMBERS: each one with its origin. See references/metrics-and-triage.md.
#
# Historical planning assumptions inherited from upstream's IEEE 1028 citation.
# These are not current normative requirements or acceptance thresholds.
PPH_DISENO_DETALLADO = (3, 4)      # pages/hour
PPH_PLAN_PRUEBAS = (5, 7)
PPH_CODIGO = 100                   # pages/hour (or 200 lines/hour)

# Historical session-size assumptions; calibrate to the actual review team.
PAGINAS_RECOMENDADO = 20
PAGINAS_INSERVIBLE = 50

# CONVENTION OF THIS SKILL, declared as such:
LINEAS_POR_PAGINA = 40             # equivalence .puml -> page. None
                                   # source defines it; one is needed.
MAX_OPERACIONES = 12               # God class candidate. Warning only.
MAX_ATRIBUTOS = 12
# THERE IS NO cyclomatic complexity threshold in the corpus, and ISO 25023
# §8.8.1 expressly delegates it to each organization. You don't invent one.
# --------------------------------------------------------------------------

TIPOS_IMPRECISOS = ("object", "var", "dynamic", "any", "mixed")
NOMBRES_SIN_INTENCION = ("dostuff", "process", "handle", "manage", "data",
                         "doit", "execute", "run", "action", "info")
TERMINOS_TECNOLOGIA = (
    "jdbc", "hibernate", "spring", "jpa", "orm", "servlet", "jsp", "ejb",
    "mysql", "postgres", "oracle", "mongo", "redis", "kafka", "django",
    "flask", "rails", "dotnet", "entityframework", "sqlalchemy",
)
# Accessors. WITHOUT IGNORECASE, and it is deliberate: with that flag `[A-Z_]` accepts
# also lowercase, and then `isla()`, `hasta()`, `issue()`, `settle()` or
# `setenta()` passed through accessors. The consequence was serious and silent:
# rule #8 SKIP the accessors, so those operations were exempt from
# verification of origin without anyone seeing it. Both are accepted
# usual spellings (camelCase and PascalCase) by enumerating them, not relaxing the
# pattern.
#
# KNOWN AND ACCEPTED LIMIT: names ALL IN CAPS (`GETNOMBRE`,
# `SETVALOR`, `HASCICLO`) are NOT recognized as accessors, and an audit
# I report it independently. **It is not corrected, and the reason matters**: any
# pattern that captures `GETNOMBRE` also captures `HASTA` (HAS+TA), `SETENTA`
# (SET+ENTA) and `ISLA` (IS+LA) in capital letters, and that reintroduces the exemption
# SILENT that this pattern came to eliminate. Only `GET` would be unambiguous in
# Spanish, and covering one of the four would leave an incoherence worse than the
# limit.
#
# The remaining bug is LOUD—a reported operation that you discard—and
# not silent—an exempt operation that no one sees. In this skill the noisy
# always win. Additionally, the pipeline notation is camelCase in all its
# rules and sets: an uppercase method does not belong in this contract.
ACCESOR_RE = re.compile(r"^(?:get|set|is|has|Get|Set|Is|Has)[A-Z_]")

STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "de", "del", "al", "y", "o", "en",
    "con", "por", "para", "que", "se", "su", "sus", "lo", "a", "es", "si",
    "the", "of", "to", "and", "or", "in", "on", "for", "is", "are",
}

# --- PlantUML: classes ---
CLASE_RE = re.compile(
    r'^\s*(?P<abstracta>abstract\s+)?(?P<tipo>class|interface|enum)\s+'
    r'(?:"(?P<q>[^"]+)"|(?P<n>[\w]+))'
    r'(?:\s+as\s+(?P<alias>[\w]+))?'
    r'(?P<estereotipos>(?:\s*<<[^>]+>>)*)',
    re.MULTILINE,
)
_MOD = r'(?:\{[^}]*\}\s*)?'
_TIPO = r'[\w<>\[\]\., ]+?'
_COLA = r'(?:\s*\[[^\]]*\])?(?:\s*=\s*[^{}\n]+?)?(?:\s*\{[^}]*\})?'
_COLA_ATRIB = (r'(?:\s*\[(?P<multiplicidad>[^\]]+)\])?'
               r'(?:\s*=\s*[^{}\n]+?)?(?:\s*\{[^}]*\})?')
ATRIB_RE = re.compile(
    rf'^\s*{_MOD}(?P<vis>[+\-#~])?\s*{_MOD}'
    rf'(?P<derivado>/)?\s*'
    rf'(?P<nombre>[A-Za-zÁÉÍÓÚÑáéíóúñ_][\wÁÉÍÓÚÑáéíóúñ]*)'
    rf'\s*(?::\s*(?P<tipo>{_TIPO}))?{_COLA_ATRIB}\s*$'
)
OPER_RE = re.compile(
    rf'^\s*{_MOD}(?P<vis>[+\-#~])?\s*{_MOD}'
    rf'(?P<nombre>[A-Za-zÁÉÍÓÚÑáéíóúñ_][\wÁÉÍÓÚÑáéíóúñ]*)'
    rf'\s*\((?P<params>[^)]*)\)'
    rf'\s*(?::\s*(?P<retorno>{_TIPO}))?{_COLA}\s*$'
)
RECEPCION_RE = re.compile(
    rf'^\s*{_MOD}(?P<vis>[+\-#~])?\s*<<\s*signal\s*>>\s*'
    r'(?P<nombre>[A-Za-zÁÉÍÓÚÑáéíóúñ_][\wÁÉÍÓÚÑáéíóúñ]*)'
    r'\s*\((?P<params>[^)]*)\)\s*$', re.IGNORECASE,
)
REL_RE = re.compile(
    r'^\s*(?P<izq>"[^"]+"|[\w]+)\s*(?P<mizq>"[^"]*"\s*)?'
    r'(?P<conn>[<>ox|*.#\-]*(?:up|down|left|right)?[<>ox|*.#\-]*)'
    r'\s*(?P<mder>"[^"]*"\s*)?(?P<der>"[^"]+"|[\w]+)\s*(?::\s*(?P<etiqueta>.*))?$',
    re.MULTILINE,
)
DIRECCION_RE = re.compile(r'-(?:up|down|left|right)-')

# --- PlantUML: sequence ---
MSG_DIR_RE = re.compile(
    r'^\s*(?P<emisor>"[^"]+"|[\w]+)\s*(?P<flecha>--?>>?|<<?--?)\s*'
    r'(?P<receptor>"[^"]+"|[\w]+)'
    r'(?:\s*(?P<corto>\+\+|--|\*\*|!!))?\s*(?::\s*(?P<etiqueta>.*))?$',
    re.MULTILINE,
)
DECL_SEC_RE = re.compile(
    r'^\s*(?:create\s+)?(?P<kind>actor|boundary|control|entity|participant|database|'
    r'collections|queue)\s+'
    r'(?:"(?P<label>[^"]+)"|(?P<bare>[\w]+))(?:\s+as\s+(?P<alias>[\w]+))?',
    re.IGNORECASE | re.MULTILINE,
)
FRAGMENTO_RE = re.compile(
    r'^\s*(?P<kw>alt|else|opt|loop|par|break|critical|group)\b(?P<etiqueta>.*)$',
    re.IGNORECASE | re.MULTILINE,
)
NOTA_ABRE = re.compile(
    r"^\s*(?:/')?\s*(?:h|r)?note\b(?!.*\bend\s*note\b)(?!.*:)", re.IGNORECASE)
NOTA_CIERRA = re.compile(r"^\s*end\s*note\b", re.IGNORECASE)

# --- Pipeline identifiers ---
FLUJO_RE = re.compile(r'\b(F[AE])\s*[-–—]?\s*(\d{1,3})\b', re.IGNORECASE)
REQ_RE = re.compile(r'\b(RNF|RF)\s*[-–—]?\s*(\d{1,3})\b', re.IGNORECASE)
CU_RE = re.compile(r'\bCU\s*[-–—]?\s*(\d{1,3})\b', re.IGNORECASE)
CP_RE = re.compile(r'\bCP\s*[-–—]?\s*(\d{1,3})\b', re.IGNORECASE)


def strip_accents(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t or "")
                   if unicodedata.category(c) != "Mn")


def norm(t: str) -> str:
    return strip_accents(t or "").strip().lower()


def camel_split(text: str) -> str:
    """Separate CamelCase: 'DAOFactory Registry' -> 'DAO Factory Registry'.

    Without this the check remains MUTE in the pasted names, which are the ones that most
    they need it; and with loose substring over-triggers ('api' is inside
    'Therapy'). Separate on both sides and compare with word border
    handles both faults.
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
    """Identity key of a class or life line.

    Removing stopwords helps match 'Incident Log' with
    'IncidentRecord'. But if when you remove them there IS NOTHING LEFT, you have to
    keep the text: names like `A`, `El`, `Un` or `En` are rare but
    legitimate —and `A`/`B` are common aliases in sequence diagrams—,
    and returning empty string causes ALL to collide on the same input.
    The effect was that a class disappeared from the model without a trace: no
    Their operations were reviewed and the counts went wrong.

    There is a second mode of collapse, more difficult to see: the filter of
    characters only preserves [a-z0-9], so a name written in another
    alphabet is cleared ENTIRE before the stopwords come into play, and
    returning to `piezas` does not save it because `piezas` is also empty. That's why
    The last network is the raw normalized text: any stable key
    is preferable to '', which is the only one that collides with all the others.
    """
    t = re.sub(r"[^a-z0-9 ]+", " ", norm(text))
    piezas = [w for w in t.split() if w]
    sin_stop = [w for w in piezas if w not in STOPWORDS]
    return "".join(sin_stop or piezas) or re.sub(r"\s+", "", norm(text))


def palabras(text: str) -> set:
    t = re.sub(r"[^a-z0-9 ]+", " ", norm(camel_split(text)))
    return {w for w in t.split() if len(w) > 2 and w not in STOPWORDS}


def flujos_de(texto: str) -> set:
    """Normalizes the graphs FA-01, FA1, FA 1 to a unique identifier."""
    return {f"{m.group(1).upper()}-{int(m.group(2)):02d}"
            for m in FLUJO_RE.finditer(texto or "")}


def requisitos_de(texto: str) -> set:
    return {f"{m.group(1).upper()}-{int(m.group(2)):02d}"
            for m in REQ_RE.finditer(texto or "")}


def casos_de(texto: str) -> set:
    return {f"CU-{int(m.group(1)):02d}" for m in CU_RE.finditer(texto or "")}


def pruebas_de(texto: str) -> set:
    return {f"CP-{int(m.group(1)):02d}" for m in CP_RE.finditer(texto or "")}


def texto_documento(texto: str) -> str:
    """Exclude closed/unclosed Markdown HTML comments from supporting evidence."""
    return re.sub(r"<!--.*?(?:-->|$)",
                  lambda m: "\n" * m.group(0).count("\n"), texto or "", flags=re.S)


def identidad_cu(texto: str) -> set:
    """Read artifact identity from its heading/title/metadata, not body references."""
    limpio = codigo_modelo(texto, conservar_comentarios=True)
    cabeceras, comentarios = [], []
    for linea in limpio.splitlines():
        ln = linea.strip()
        if re.match(r"^(?:#{1,6}\s|title\b|@startuml\b|\*\*(?:ID|Use case|Caso de uso)\b)", ln, re.I):
            cabeceras.append(ln)
        elif ln.startswith("'"):
            comentarios.append(ln)
    return casos_de("\n".join(cabeceras)) or casos_de("\n".join(comentarios))


def especificacion_util(texto: str) -> bool:
    """A CU identity and at least one actual prose/table step are indispensable."""
    limpio = texto_documento(texto)
    return bool(identidad_cu(limpio) and re.search(
        r"^\s*(?:\d+[.)]\s+\S|\|\s*(?:\d+|F[AE][-–—]?\d+[.]\d+)\s*\|\s*[^|]+\|\s*\S)",
        limpio, re.M | re.I))


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class Miembro:
    nombre: str
    visibilidad: str
    linea: int
    tipo: str = ""
    params: str = ""
    # Modifiers per member. The parser accepted them but threw them away, like this
    # that the header generator could not distinguish a specific method of
    # an abstract one within an abstract class, nor mark the static ones.
    estatico: bool = False
    abstracto: bool = False
    derivado: bool = False
    multiplicidad: str = ""


@dataclass
class Clase:
    nombre: str
    linea: int
    abstracta: bool = False
    kind: str = "class"
    estereotipos: set = field(default_factory=set)
    atributos: list = field(default_factory=list)
    operaciones: list = field(default_factory=list)
    recepciones: list = field(default_factory=list)  # Signal receptions, not Operations
    no_parseadas: list = field(default_factory=list)

    @property
    def es_abstracta(self) -> bool:
        return self.abstracta or any('abstract' in norm(e)
                                     for e in self.estereotipos)

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


@dataclass
class Secuencia:
    path: str
    text: str
    lineas_vida: dict = field(default_factory=dict)   # key -> tag
    kinds: dict = field(default_factory=dict)         # key -> actor|entity|...
    receptores: dict = field(default_factory=dict)    # key -> {vocabulario}
    con_mensaje: set = field(default_factory=set)     # keys that receive something
    vocabulario: set = field(default_factory=set)
    fragmentos: list = field(default_factory=list)    # (kw, label, line)
    n_mensajes: int = 0
    avisos_semanticos: list = field(default_factory=list)


# --------------------------------------------------------------------------
# Parsers
# --------------------------------------------------------------------------

# The comment block is ONLY recognized when `/'` opens AT THE BEGINNING OF
# LINE. Masking quoted strings was not enough: in PlantUML a
# relationship tag does NOT need quotes, so `A -- B : current /' from
# 2024` abria un bloque falso que se cerraba en el siguiente `'/` legitimate
# file and deleted everything in between — three declared classes, two
# parsed, without error or warning. Requiring the beginning of the line covers the form of
# actual authorship (comment a piece) and leaves any embedded `/'` harmless
# in free text.
BLOQUE_COMENTARIO_RE = re.compile(r"^[ \t]*/'.*?'/", re.S | re.M)
APERTURA_BLOQUE_RE = re.compile(r"^[ \t]*/'", re.M)
CIERRE_BLOQUE_RE = re.compile(r"'/")
ENTRECOMILLADO_RE = re.compile(r'"[^"\n]*"')


def sin_comentarios(text: str) -> str:
    """Empty the `/' ... '/` blocks CONSERVING the number of lines.

    Commenting on a piece of model while iterating is authoring practice.
    normal. Without this, a commented class would be parsed as if it existed and
    generated findings about elements that are not in the design — a design
    blameless received a rejection verdict for dead code.

    **Quoted strings are protected first**, and it's not a detail:
    a message tag containing `/'`—a path, a date, a
    apostrophe—opened a false block that closed on the next real `'/`
    of the file, and EVERYTHING in between disappeared silently. In the
    proof that he uncovered it, two classes disappeared from the model. mask,
    Cleaning and restoring costs little and avoids destroying the artifact.

    It is replaced by line breaks instead of empty so that the
    locators (L{n}) keep pointing where they should.
    """
    t = text or ""
    protegidas = []

    def _guardar(m):
        protegidas.append(m.group(0))
        return f"\x00{len(protegidas) - 1}\x00"

    t = ENTRECOMILLADO_RE.sub(_guardar, t)
    t = BLOQUE_COMENTARIO_RE.sub(
        lambda m: "\n" * m.group(0).count("\n"), t)
    return re.sub(r"\x00(\d+)\x00", lambda m: protegidas[int(m.group(1))], t)


def leer(path: str) -> str:
    try:
        # utf-8-sig, not utf-8: a BOM survives `.strip()`—not space in
        # white for Python—and caused the first line to not be recognized
        # as `@startuml`, unsquaring the page count of the
        # budget.
        with open(path, "r", encoding="utf-8-sig") as fh:
            return sin_comentarios(fh.read())
    except FileNotFoundError:
        print(f"File does not exist: {path}", file=sys.stderr)
        raise SystemExit(2)
    except (OSError, UnicodeError) as exc:
        print(f"Cannot read input file: {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def codigo_modelo(text: str, conservar_comentarios: bool = False) -> str:
    """Mask annotation content while preserving source line locations.

    CU metadata in a line comment may identify an artifact, but declarations,
    operations and branch evidence must come from executable notation.
    """
    limpio = sin_comentarios(text)
    # An unclosed block comments out the rest of the file in PlantUML.
    abierto = APERTURA_BLOQUE_RE.search(limpio)
    if abierto:
        limpio = limpio[:abierto.start()] + "\n" * limpio[abierto.start():].count("\n")
    lineas, anotacion = [], ""
    for cruda in limpio.splitlines(keepends=True):
        ln = cruda.strip()
        ocultar = bool(anotacion)
        if anotacion:
            cierre = r"^end\s*legend\b" if anotacion == "legend" else r"^end\s*(?:h|r)?note\b"
            if re.match(cierre, ln, re.I):
                anotacion = ""
        elif re.match(r"^legend\b", ln, re.I):
            ocultar, anotacion = True, "legend"
        elif re.match(r"^(?:h|r)?note\b", ln, re.I):
            ocultar = True
            # Inline notes and quoted standalone notes occupy a single line.
            multilinea = not (":" in ENTRECOMILLADO_RE.sub("", ln)
                              or re.match(r'^(?:h|r)?note\s+"', ln, re.I)
                              or re.search(r"\bend\s*(?:h|r)?note\b", ln, re.I))
            anotacion = "note" if multilinea else ""
        elif ln.startswith("'") and not conservar_comentarios:
            ocultar = True
        lineas.append("\n" if ocultar and cruda.endswith("\n") else "" if ocultar else cruda)
    return "".join(lineas)


def separar_nivel(texto: str, separador: str) -> list:
    """Split signature separators only outside nested types/quoted defaults."""
    partes, inicio, pila, comilla, escape = [], 0, [], "", False
    cierres = {"<": ">", "[": "]", "(": ")", "{": "}"}
    for i, char in enumerate(texto):
        if comilla:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == comilla:
                comilla = ""
        elif char in ('"', "'"):
            comilla = char
        elif char in cierres:
            pila.append(cierres[char])
        elif pila and char == pila[-1]:
            pila.pop()
        elif char == separador and not pila:
            partes.append(texto[inicio:i].strip())
            inicio = i + 1
    partes.append(texto[inicio:].strip())
    return partes


def parametros_de(texto: str) -> list:
    """Return (name, type, default) for each UML parameter, without guessing."""
    out = []
    for parametro in separar_nivel(texto or "", ","):
        if not parametro:
            continue
        por_defecto = separar_nivel(parametro, "=")
        firma = separar_nivel(por_defecto[0], ":")
        out.append((firma[0], ":".join(firma[1:]).strip(),
                    "=".join(por_defecto[1:]).strip()))
    return out


def limites_multiplicidad(texto: str):
    """Return integer lower/upper bounds (None = unbounded), or unsupported."""
    if texto == "*":
        return 0, None
    m = re.fullmatch(r"(\d+)(?:\s*\.\.\s*(\d+|\*))?", texto)
    if not m:
        return None
    minimo = int(m.group(1))
    maximo = m.group(2) or m.group(1)
    if maximo == "*":
        return minimo, None
    return (minimo, int(maximo)) if int(maximo) >= minimo else None


def cuerpo_de_clase(text: str, desde: int):
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
    text = codigo_modelo(text)
    alias = {}
    for mc in CLASE_RE.finditer(text):
        nombre = mc.group("q") or mc.group("n") or ""
        linea = text[: mc.start()].count("\n") + 1
        estereotipos = set(re.findall(r"<<([^>]+)>>",
                                      mc.group("estereotipos") or ""))
        c = Clase(nombre=nombre, linea=linea,
                  abstracta=bool(mc.group("abstracta")),
                  kind=mc.group("tipo").lower(), estereotipos=estereotipos)
        cuerpo, _ = cuerpo_de_clase(text, mc.end())
        base = text[: mc.end()].count("\n") + 1
        for off, cruda in enumerate(cuerpo.split("\n"), start=1):
            ln = cruda.strip()
            if (not ln or ln.startswith("'") or ln.startswith("..")
                    or ln.startswith("--") or ln.startswith("==")):
                continue
            n_linea = base + off
            mods = {norm(x) for x in re.findall(r"\{([^}]*)\}", ln)}
            est, abst = "static" in mods, "abstract" in mods
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
                    params=(mo.group("params") or "").strip(),
                    estatico=est, abstracto=abst))
                continue
            ma = ATRIB_RE.match(ln)
            if ma:
                c.atributos.append(Miembro(
                    nombre=ma.group("nombre"), visibilidad=ma.group("vis") or "",
                    linea=n_linea, tipo=(ma.group("tipo") or "").strip(),
                    estatico=est, abstracto=abst, derivado=bool(ma.group("derivado")),
                    multiplicidad=(ma.group("multiplicidad") or "").strip()))
                continue
            # What could not be interpreted is RECORDED: a limb lost in
            # Silence falsifies all the counts that depend on it.
            c.no_parseadas.append((n_linea, ln))
        m.clases[clave(nombre)] = c
        if mc.group("alias"):
            alias[mc.group("alias")] = nombre

    texto_rel = DIRECCION_RE.sub("-", text)
    for mr in REL_RE.finditer(texto_rel):
        conn = mr.group("conn") or ""
        if len(re.sub(r"[^<>ox|*.\-]", "", conn)) < 2:
            continue
        izq = mr.group("izq").strip('"')
        der = mr.group("der").strip('"')
        izq, der = alias.get(izq, izq), alias.get(der, der)
        if izq.lower() in ("startuml", "enduml") or der.lower() in ("startuml", "enduml"):
            continue
        mizq = (mr.group("mizq") or "").strip().strip('"')
        mder = (mr.group("mder") or "").strip().strip('"')
        m.relaciones.append({
            "izq": izq, "der": der, "conn": conn,
            "multiplicidad": bool(mizq and mder),
            "multiplicidad_izq": mizq, "multiplicidad_der": mder,
            # The label distinguishes two associations to the same type
            # (`: facturacion` vs. `: envio`). Without saving it, the
            # generator deduplicated them into one and lost a field.
            "etiqueta": (mr.group("etiqueta") or "").strip(),
            "linea": texto_rel[: mr.start()].count("\n") + 1,
        })
    return m


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
    """Return (call label, unresolved async); a Signal is not an Operation.

    Label annotations: <<synchCall>>, <<asynchCall>>, <<reply>>,
    <<asynchSignal>>, <<createMessage>>, <<deleteMessage>>. Explicit calls
    require an operation signature. Unannotated solid synchronous arrows
    retain legacy lexical matching; unannotated async arrows need review.
    """
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


def parse_secuencia(path: str, text: str) -> Secuencia:
    s = Secuencia(path=path, text=text)
    text = codigo_modelo(text)
    alias = {}
    for md in DECL_SEC_RE.finditer(text):
        etiqueta = md.group("label") or md.group("bare") or ""
        a = md.group("alias") or md.group("bare") or etiqueta
        if a:
            alias[a] = etiqueta
            s.lineas_vida[clave(etiqueta)] = etiqueta
            s.kinds[clave(etiqueta)] = (md.group("kind") or "").lower()

    en_nota, creaciones = False, set()
    for i, cruda in enumerate(text.split("\n"), start=1):
        ln = cruda.strip()
        # Note blocks contain free text that can start with 'alt' or
        # look like a message. Skipping them avoids fragments and ghost messages.
        if en_nota:
            if NOTA_CIERRA.match(ln):
                en_nota = False
            continue
        if NOTA_ABRE.match(ln):
            en_nota = True
            continue
        mc = CREATE_SEC_RE.match(ln)
        if mc:
            creaciones.add(mc.group("alias") or mc.group("quien").strip('"'))
            continue
        mf = FRAGMENTO_RE.match(ln)
        if mf:
            s.fragmentos.append((mf.group("kw").lower(),
                                 (mf.group("etiqueta") or "").strip(), i))
            continue
        mm = MSG_DIR_RE.match(ln)
        if not mm:
            continue
        et, sin_resolver = etiqueta_de_llamada(mm, creaciones)
        if sin_resolver:
            s.avisos_semanticos.append(
                f"[{path}] L{i}: unresolved asynchronous message provenance; declare "
                f"<<asynchCall>> with an Operation signature or <<asynchSignal>>.")
        emisor = mm.group("emisor").strip('"')
        receptor = mm.group("receptor").strip('"')
        if (mm.group("flecha") or "").startswith("<"):
            emisor, receptor = receptor, emisor
        destino = clave(alias.get(receptor, receptor))
        origen = clave(alias.get(emisor, emisor))
        s.n_mensajes += 1
        s.con_mensaje.add(destino)
        for k in (origen, destino):
            s.lineas_vida.setdefault(k, k)
        if et:
            p = palabras(et)
            mfun = re.match(r"^([A-Za-z_][\w]*)\s*\(", et)
            if mfun:
                p.add(norm(mfun.group(1)))
            s.vocabulario |= p
            s.receptores.setdefault(destino, set()).update(p)
    return s


def parse_dominio(text: str) -> dict:
    out = {}
    text = codigo_modelo(text)
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
    """{clave_hijo: {claves_ascendientes}} — inheritance AND implementation.

    Returns SETS, not a single parent. A previous version kept a
    only parent per class and the last relationship overwrote the previous ones:
    with `X -up-|> Base` followed by `X ..|> Interfaz`, the ascendant of
    It remained the interface and the base class was lost. The consequence was
    a FALSE POSITIVE on a legitimate overwrite — the operation of
    redefines the Base was reported as "possibly in the class
    wrong."

    The interface implementation (`..|>`) counts as ancestry for purposes
    of origin: implementing an interface is committing to its
    operations.
    """
    padres = {}
    for r in mod.relaciones:
        ki, kd = clave(r["izq"]), clave(r["der"])
        conn = r["conn"]
        if "<|" in conn:              # Father <|-- Son / Father <|.. Son
            padres.setdefault(kd, set()).add(ki)
        elif "|>" in conn:            # Child --|> Parent/Child..|> Interface
            padres.setdefault(ki, set()).add(kd)
    return padres


def ascendientes(k: str, padres: dict) -> list:
    """All ascendants of k, in width and without cycles."""
    vistos, cola, out = {k}, list(padres.get(k, ())), []
    while cola:
        p = cola.pop(0)
        if p in vistos:
            continue
        vistos.add(p)
        out.append(p)
        cola.extend(padres.get(p, ()))
    return out


def realizadores(k: str, padres: dict) -> list:
    """Classes that declare k as an ancestor (implement or inherit from k).

    An operation declared in an INTERFACE does not usually receive messages: the
    receives whoever implements it. Without this, any correct interface would produce
    orphan operations.
    """
    return [h for h, ps in padres.items() if k in ps]


def realizadores_transitivos(k: str, padres: dict) -> list:
    """All those who perform k, directly or indirectly.

    With `IntB --|> IntA` and `ClaseX ..|> IntB`, whoever receives the
    IntA is ClassX, which is not performed directly. Looking at just one level left
    to IntA without covering — and the ruling appeared twice, in rule #8
    and in #6. That's why the route lives here and is not duplicated at each check.
    """
    pendientes, vistos, out = list(realizadores(k, padres)), {k}, []
    while pendientes:
        h = pendientes.pop()
        if h in vistos:
            continue
        vistos.add(h)
        out.append(h)
        pendientes.extend(realizadores(h, padres))
    return out


def parse_controladores(text: str) -> list:
    """Controllers of a robustness diagram: the verification unit
    that rule #1 establishes ('test cases for the controllers')."""
    out = []
    for md in DECL_SEC_RE.finditer(codigo_modelo(text)):
        if (md.group("kind") or "").lower() != "control":
            continue
        label = md.group("label") or md.group("bare") or ""
        # PlantUML display escapes separate visible words; they are not part
        # of a controller's responsibility vocabulary in a Markdown test table.
        label = label.replace(r"\n", " ").replace(r"\r", " ")
        out.append(" ".join(label.split()))
    return [c for c in out if c]


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_modelo_vacio(mod: Modelo, errores: list) -> bool:
    if not mod.clases:
        errores.append(
            f"[{mod.path}] the class model does not declare any classes. No "
            f"There is a design to review.")
        return True
    return False


def check_criterio_entrada(mod, secuencias, specs, errores, avisos) -> bool:
    """IEEE 1028 §5.4.2 and Rosenberg 4556: without this, NOT reviewed.

    Returns True if the criterion fails (must stop).
    """
    falla = False
    # EVERY diagram, not "some." The source requires that ALL be complete.
    # the release sequences; just check that some have messages
    # let a half-finished diagram pass through the gate itself that
    # skill presents as his most important stop.
    vacias = [s.path for s in secuencias if not s.n_mensajes]
    if vacias:
        errores.append(
            f"ENTRY CRITERIA: {len(vacias)} sequence diagram(s) without "
            f"messages ({', '.join(vacias)}). Complete their interactions "
            f"before reviewing message coverage and operation allocation.")
        falla = True

    # Each CU mentioned in the specifications should have sequence.
    cus_spec = set()
    for t in specs:
        # Release-scope declarations may name additional CUs in prose even
        # though local FA/FE IDs belong only to the artifact's own heading CU.
        cus_spec |= casos_de(texto_documento(t))
    cus_seq = set()
    for s in secuencias:
        cus_seq |= identidad_cu(s.text)
    if cus_spec and cus_seq:
        sin_secuencia = sorted(cus_spec - cus_seq)
        if sin_secuencia:
            errores.append(
                f"ENTRY CRITERIA: {', '.join(sin_secuencia)} appears in "
                f"the specification but no sequence diagram "
                f"identifies. Lack of release scope design.")
            falla = True
    elif cus_spec and not cus_seq:
        avisos.append(
            "The sequence diagrams do not cite any CU-XX, so it is not "
            "was able to verify that they covered the scope. Identify them so that the "
            "entry criterion is verifiable.")
    return falla


def check_r9_flujos(secuencias, specs, errores) -> int:
    """Compare (CU, local flow) identities using executable branch labels only."""
    por_cu = {}
    for s in secuencias:
        cus = identidad_cu(s.text)
        if len(cus) != 1:
            errores.append(
                f"RULE #9: [{s.path}] has no unambiguous CU identity; "
                f"cannot pair its local flow evidence with a specification.")
            continue
        cubiertos = por_cu.setdefault(next(iter(cus)), set())
        for _kw, etiqueta, _n in s.fragmentos:
            cubiertos |= flujos_de(etiqueta)
    faltan, declarados_cu = set(), set()
    for i, texto in enumerate(specs, start=1):
        cus = identidad_cu(texto)
        if len(cus) != 1:
            errores.append(
                f"RULE #9: specification {i} has no unambiguous CU identity; "
                f"cannot scope its local flow identifiers.")
            continue
        cu = next(iter(cus))
        if cu in declarados_cu:
            errores.append(
                f"RULE #9: {cu} has multiple supplied specifications; pairing "
                f"is ambiguous. Supply one authoritative specification per CU.")
        declarados_cu.add(cu)
        for flujo in flujos_de(texto) - por_cu.get(cu, set()):
            faltan.add((cu, flujo))
    for cu, flujo in sorted(faltan):
        errores.append(
            f"RULE #9: {cu} flow {flujo} is specified but does not appear in "
            f"an executable branch of its sequence diagrams.")
    for cu in sorted(set(por_cu) - declarados_cu):
        errores.append(
            f"RULE #9: {cu} sequence has no matching supplied specification; "
            f"its flow coverage has not been checked.")
    return len(faltan)


def check_r8_asignacion(mod, secuencias, errores, avisos) -> int:
    """Rule #8: each operation comes from a message ADDRESSED TO ITS CLASS.

    Comparing against a global bag of vocabulary misses exactly the
    book `Queue` defect: an operation on the wrong class.
    """
    voc_global, por_receptor = set(), {}
    for s in secuencias:
        voc_global |= s.vocabulario
        avisos.extend(s.avisos_semanticos)
        for k, v in s.receptores.items():
            por_receptor.setdefault(k, set()).update(v)

    padres = parse_generalizaciones(mod)
    huerfanas = 0
    # First pass: UPWARD origin of each class. a subclass
    # inherits that of its ancestry — overwriting does not require its own message
    # addressed to her, because the message goes to the general type.
    # Provenance is ALWAYS evidence of messages, never names
    # declared. An earlier version also linked operation names
    # that the ancestors declared, and that "washed" the origin: a
    # interface retrieved its own names through any producer
    # indirect, and an operation that no message invoked went from ERROR to
    # total silence. Joining names was redundant as well as dangerous: if the
    # ascendant is legitimately covered, your message is ALREADY here for the
    # chain of ancestors; If it is not, there is nothing to inherit.
    heredada = {}
    for c in mod.clases.values():
        kc = clave(c.nombre)
        propio = set(por_receptor.get(kc, set()))
        for a in ascendientes(kc, padres):
            propio |= por_receptor.get(a, set())
        heredada[kc] = propio

    # Second pass: DOWN. The operations of an interface or a
    # abstract class does not receive them, it receives them whoever makes them — and there are
    # You have to look at the ENTIRE source of the filmmaker, not just what he or she receives
    # directly: if the creator in turn inherits the operation of a class
    # base, the interface is still covered.
    for c in mod.clases.values():
        kc = clave(c.nombre)
        propio = heredada[kc]
        if c.kind == "interface" or c.es_abstracta:
            for h in realizadores_transitivos(kc, padres):
                propio |= heredada.get(h, set())
        for o in c.operaciones:
            if ACCESOR_RE.match(o.nombre):
                continue
            p = palabras(o.nombre) | {norm(o.nombre)}
            if p & propio:
                continue
            if p & voc_global:
                avisos.append(
                    f"RULE #8 [{mod.path}] L{o.linea}: "
                    f"'{c.nombre}.{o.nombre}()' appears in the diagrams "
                    f"sequence but NOT as a message addressed to '{c.nombre}'. "
                    f"You may be in the wrong class. Check responsibility "
                    f"allocation and the receiving end of the sequence message.")
                continue
            huerfanas += 1
            errores.append(
                f"RULE #8 [{mod.path}] L{o.linea}: the operation "
                f"'{c.nombre}.{o.nombre}()' does not correspond to any message "
                f"sequence diagrams. Either the message is missing, or there is too much "
                f"operacion.")
    return huerfanas


def check_r7_responsabilidades(mod, dominio, hay_dominio, avisos) -> None:
    """Rule #7: Appropriate attributes and operations."""
    tag = f"[{mod.path}]"
    for c in mod.clases.values():
        if c.kind != "class" or c.es_abstracta:
            continue
        if c.atributos and not c.operaciones:
            avisos.append(
                f"RULE #7 {tag} L{c.linea}: '{c.nombre}' has "
                f"{len(c.atributos)} attribute(s) and NO operation. Check whether "
                f"behavior belonging to this class has been placed in a controller "
                f"or service, or whether a data-only role is intentional.")
        if not c.atributos and not c.es_solucion and not c.operaciones:
            avisos.append(
                f"RULE #7 {tag} L{c.linea}: '{c.nombre}' does not declare attributes "
                f"nor operations. An empty class usually indicates layout "
                f"incompleto.")
        if hay_dominio and clave(c.nombre) in dominio and not c.atributos:
            avisos.append(
                f"RULE #7 {tag} L{c.linea}: entity '{c.nombre}' does not declare "
                f"no attribute. The data that the system manages does not have "
                f"where to live")
        if len(c.operaciones) > MAX_OPERACIONES:
            avisos.append(
                f"RULE #7 {tag} L{c.linea}: '{c.nombre}' declares "
                f"{len(c.operaciones)} operations (CONVENTION threshold "
                f"this skill: {MAX_OPERACIONES}; no source fixes it). "
                f"Candidate for God class: apply the test of sets of "
                f"unrelated operations.")
        if len(c.atributos) > MAX_ATRIBUTOS:
            avisos.append(
                f"RULE #7 {tag} L{c.linea}: '{c.nombre}' declares "
                f"{len(c.atributos)} attributes (CONVENTION threshold: "
                f"{MAX_ATRIBUTOS}). Check if you have more than one responsibility.")


def check_envoltorio(mod, avisos) -> None:
    """Wrapper class: X adds to Y, attributes of X are subset of
    those of Y, and the operations of X are all accessors.

    This is a review heuristic; framework integration may justify the wrapper.
    """
    # The address matters and a previous version ignored it: it built the
    # aggregation as a symmetric relationship, so an object of value
    # CONTENTS (`Dinero` within `Factura`) was accused of involving his
    # container. The envelope is the one who SUPPORTS the other — in the case of the
    # book, the Command holds the entity—that is, the side of the rhombus.
    agrega = {}
    for r in mod.relaciones:
        conn = r["conn"]
        if "o-" in conn or "*-" in conn:        # rhombus on the left
            agrega.setdefault(clave(r["izq"]), set()).add(clave(r["der"]))
        elif "-o" in conn or "-*" in conn:      # rhombus to the right
            agrega.setdefault(clave(r["der"]), set()).add(clave(r["izq"]))
    for c in mod.clases.values():
        if not c.operaciones or not c.atributos:
            continue
        if not all(ACCESOR_RE.match(o.nombre) for o in c.operaciones):
            continue
        mios = {norm(a.nombre) for a in c.atributos}
        for otra_k in agrega.get(clave(c.nombre), set()):
            otra = mod.clases.get(otra_k)
            if not otra or otra is c or not otra.atributos:
                continue
            suyos = {norm(a.nombre) for a in otra.atributos}
            comunes = mios & suyos
            if comunes and mios <= suyos:
                avisos.append(
                    f"RULE #7 [{mod.path}] L{c.linea}: '{c.nombre}' looks like a "
                    f"WRAPPER CLASS of '{otra.nombre}': its attributes are a "
                    f"subset of those of that one ({', '.join(sorted(comunes))}) "
                    f"and all its operations are accessors. Check whether this "
                    f"wrapper has a separate responsibility. If framework integration "
                    f"requires it, declare and justify it as <<solution>>.")


def check_r3_firmas(mod, avisos) -> None:
    """Rule #3: Complete and precise types, parameters and returns."""
    tag = f"[{mod.path}]"
    for c in mod.clases.values():
        if c.kind == "enum":
            continue
        for a in c.atributos:
            if not a.tipo:
                avisos.append(
                    f"RULE #3 {tag} L{a.linea}: the attribute "
                    f"'{c.nombre}.{a.nombre}' does not declare a type.")
            elif norm(a.tipo) in TIPOS_IMPRECISOS:
                avisos.append(
                    f"RULE #3 {tag} L{a.linea}: '{c.nombre}.{a.nombre}' uses the "
                    f"imprecise type '{a.tipo.strip()}'. A vague type "
                    f"transfers to the code a decision that the design had to "
                    f"cerrar.")
        for o in c.operaciones:
            if not o.tipo:
                avisos.append(
                    f"RULE #3 {tag} L{o.linea}: the operation "
                    f"'{c.nombre}.{o.nombre}()' does not declare a return value.")
            elif norm(o.tipo) in TIPOS_IMPRECISOS:
                avisos.append(
                    f"RULE #3 {tag} L{o.linea}: '{c.nombre}.{o.nombre}()' "
                    f"returns vague type '{o.tipo.strip()}'.")
            if any(not tipo for _nombre, tipo, _defecto in parametros_de(o.params)):
                avisos.append(
                    f"RULE #3 {tag} L{o.linea}: the parameters of "
                    f"'{c.nombre}.{o.nombre}()' is not typed.")
            for t in TIPOS_IMPRECISOS:
                if re.search(rf":\s*{t}\b", norm(o.params or "")):
                    avisos.append(
                        f"RULE #3 {tag} L{o.linea}: "
                        f"'{c.nombre}.{o.nombre}()' receives a parameter of type "
                        f"vague '{t}'.")
                    break
            if norm(o.nombre) in NOMBRES_SIN_INTENCION:
                avisos.append(
                    f"RULE #3 {tag} L{o.linea}: '{c.nombre}.{o.nombre}()' is a "
                    f"unintentional name. The names should express what it does "
                    f"the operation; a generic name usually hides that the "
                    f"responsibility is not clear.")


def check_abstraccion_inestable(mod, avisos) -> None:
    for c in mod.clases.values():
        if c.es_solucion:
            continue
        hit = contiene_termino(c.nombre, TERMINOS_TECNOLOGIA)
        if hit:
            avisos.append(
                f"[{mod.path}] L{c.linea}: '{c.nombre}' names a technology "
                f"('{hit}') and <<solution>> is not marked. Separate domain "
                f"responsibilities from implementation choices; mark and justify "
                f"a technology-specific solution class.")


def check_multiplicidades(mod, avisos) -> None:
    sin = [r for r in mod.relaciones
           if not r["multiplicidad"] and "<|" not in r["conn"]
           and "|>" not in r["conn"] and ".." not in r["conn"]]
    if sin:
        ejemplo = sin[0]
        avisos.append(
            f"[{mod.path}] {len(sin)} relationship(s) without multiplicity, for "
            f"example '{ejemplo['izq']}' - '{ejemplo['der']}' in L{ejemplo['linea']}. "
            f"Declare both association-end bounds so the reviewer can distinguish "
            f"a single reference, optional reference and collection.")
    for relacion in mod.relaciones:
        if any(x in relacion["conn"] for x in ("<|", "|>", "..")):
            continue
        for extremo in ("izq", "der"):
            valor = relacion["multiplicidad_" + extremo]
            if valor and limites_multiplicidad(valor) is None:
                avisos.append(
                    f"[{mod.path}] L{relacion['linea']}: unsupported multiplicity "
                    f"'{valor}' at '{relacion[extremo]}'; its bounds cannot be verified.")


def check_lineas_vida_huerfanas(secuencias, avisos) -> None:
    """Drawn object that no one sends messages to.

    ACTORS are excluded: an actor who only initiates the flow and never receives
    response is normal, not a design gap. Marking actors would convert
    This check in noise in almost all the diagrams.
    """
    for s in secuencias:
        for k, etiqueta in s.lineas_vida.items():
            if s.kinds.get(k) == "actor":
                continue
            if k not in s.con_mensaje:
                avisos.append(
                    f"[{s.path}] lifeline '{etiqueta}' does not receive any "
                    f"message. Add the missing collaboration or explain why "
                    f"this participant belongs in the interaction.")


def check_r5_trazabilidad(mod, req_texto, specs, avisos) -> dict:
    """Rule #5: requirements -> use cases -> classes, BOTH ways."""
    reqs = requisitos_de(req_texto)
    resultado = {"requisitos": len(reqs), "sin_implementar": [], "sin_requisito": []}
    if not reqs:
        return resultado

    voc_clases = set()
    for c in mod.clases.values():
        voc_clases |= palabras(c.nombre)
        for o in c.operaciones:
            voc_clases |= palabras(o.nombre)
        for a in c.atributos:
            voc_clases |= palabras(a.nombre)

    # Requirement -> some class. The text is taken from the requirement line.
    #
    # TWO words in common are required, not one. One term was enough
    # generic shared by chance—“format,” “data,” “state”—for
    # cover a requirement that no one had implemented, and the failure
    # was SILENT: the requirement simply did not appear on the list. Two
    # Matches do not guarantee semantic coverage, but they eliminate the
    # accident of the single word. The threshold is CONVENTION of this skill.
    MIN_COINCIDENCIAS = 2
    for linea in (req_texto or "").split("\n"):
        ids = requisitos_de(linea)
        if not ids:
            continue
        if len(palabras(linea) & voc_clases) >= MIN_COINCIDENCIAS:
            continue
        rid = sorted(ids)[0]
        resultado["sin_implementar"].append(rid)
        avisos.append(
            f"RULE #5: requirement {rid} has no vocabulary in common with "
            f"no model class. Functionality may be missing. "
            f"(The comparison is lexical: it does not recognize synonyms, so "
            f"confirm it before taking it for granted.)")

    # Class -> some requirement or specification.
    voc_fuente = palabras(req_texto or "")
    for t in specs:
        voc_fuente |= palabras(t)
    for c in mod.clases.values():
        if c.es_solucion:
            continue
        if palabras(c.nombre) & voc_fuente:
            continue
        resultado["sin_requisito"].append(c.nombre)
        avisos.append(
            f"RULE #5 [{mod.path}] L{c.linea}: class '{c.nombre}' does not appear "
            f"in the requirements or specifications. Either there is too much design, or "
            f"there is an undocumented implicit requirement — the second case is "
            f"frequent and more informative.")
    return resultado


def check_r1_pruebas(controladores, pruebas_texto, secuencias, specs, avisos) -> None:
    """Rule #1: One test case per robustness controller."""
    cps = pruebas_de(pruebas_texto)
    if not cps:
        avisos.append(
            "RULE #1: The test plan does not declare any CP-XX. Without "
            "identifiers cannot be checked for coverage.")
        return
    voc_pruebas = palabras(pruebas_texto)
    for ctrl in controladores:
        if not (palabras(ctrl) & voc_pruebas):
            avisos.append(
                f"RULE #1: Controller '{ctrl}' does not appear in the plan "
                f"evidence. Link it to test cases that exercise its "
                f"responsibility and relevant failure paths.")
    declarados = set()
    for t in specs:
        declarados |= flujos_de(t)
    sin_prueba = sorted(declarados - flujos_de(pruebas_texto))
    for f in sin_prueba:
        avisos.append(
            f"RULE #1: Flow {f} has no associated test case.")


def check_r6_patrones(mod, secuencias, avisos) -> None:
    """Rule #6: What the model declares must be seen in the sequence."""
    voc = set()
    for s in secuencias:
        voc |= s.vocabulario
        voc |= {clave(v) for v in s.lineas_vida.values()}
        voc |= palabras(" ".join(s.lineas_vida.values()))
    padres = parse_generalizaciones(mod)
    for c in mod.clases.values():
        if not c.es_solucion:
            continue
        if palabras(c.nombre) & voc:
            continue
        # An INTERFACE is a type, not a participant: in the sequence it appears
        # who implements it, not her. Demanding his own life line would be a
        # False positive especially in any design that uses interfaces.
        if c.kind == "interface":
            reales = realizadores_transitivos(clave(c.nombre), padres)
            if any(palabras(mod.clases[h].nombre) & voc
                   for h in reales if h in mod.clases):
                continue
        avisos.append(
            f"RULE #6 [{mod.path}] L{c.linea}: the solution class "
            f"'{c.nombre}' does not appear in any sequence diagram. "
            f"Show the collaboration that uses it or remove it from this review scope.")


def check_comentario_sin_cerrar(paths_y_textos, avisos) -> None:
    """A `/'` without its `'/` causes PlantUML to comment out the rest of the file.

    The parser cannot know where it ends, so it analyzes what is real as real.
    the tool considers commented — and the findings return on
    elements that do not exist in the design. It is not guessed: it is warned.
    """
    for path, texto in paths_y_textos:
        # Quoted strings are ignored, for the same reason as in
        # `sin_comentarios`: a `/'` inside a message tag does not open
        # nothing. Counting it here produced a warning about a correct diagram.
        # The SAME criteria are used for cleaning: only openings to
        # beginning of line Count any `/'` towards that a tag with
        # that text would produce a warning about a correct diagram.
        limpio = ENTRECOMILLADO_RE.sub("", texto or "")
        abre = len(APERTURA_BLOQUE_RE.findall(limpio))
        cierra = len(CIERRE_BLOQUE_RE.findall(limpio))
        if abre > cierra:
            avisos.append(
                f"[{path}] there are {abre - cierra} comment block(s) `/'` without "
                f"close with `'/`. PlantUML will treat as comments everything "
                f"go on; This validator can't, so you can report "
                f"findings about elements that do not exist in the real diagram. "
                f"Close the block before trusting the result.")


def check_no_parseadas(mod, avisos) -> None:
    for c in mod.clases.values():
        for n, texto in c.no_parseadas:
            avisos.append(
                f"[{mod.path}] L{n}: Could not interpret this member "
                f"'{c.nombre}': \"{texto[:60]}\". It has not been counted as an attribute "
                f"nor as an operation; check the syntax before trusting "
                f"counts of this class.")


# --------------------------------------------------------------------------
# Session planning
# --------------------------------------------------------------------------

def lineas_efectivas(text: str) -> int:
    n = 0
    for cruda in (text or "").split("\n"):
        ln = cruda.strip()
        if ln and not ln.startswith("'") and not ln.startswith("@"):
            n += 1
    return n


def presupuesto(mod, secuencias, pruebas_texto):
    lin = lineas_efectivas(mod.text) + sum(lineas_efectivas(s.text)
                                           for s in secuencias)
    pag_diseno = lin / LINEAS_POR_PAGINA
    pag_pruebas = lineas_efectivas(pruebas_texto) / LINEAS_POR_PAGINA
    horas = (pag_diseno / PPH_DISENO_DETALLADO[1],
             pag_diseno / PPH_DISENO_DETALLADO[0])
    if pag_pruebas:
        horas = (horas[0] + pag_pruebas / PPH_PLAN_PRUEBAS[1],
                 horas[1] + pag_pruebas / PPH_PLAN_PRUEBAS[0])
    return {"paginas_diseno": pag_diseno, "paginas_pruebas": pag_pruebas,
            "horas": horas,
            "sesiones": max(1, int(pag_diseno // PAGINAS_RECOMENDADO) +
                            (1 if pag_diseno % PAGINAS_RECOMENDADO else 0))}


def check_presupuesto(pres, avisos) -> None:
    p = pres["paginas_diseno"]
    if p > PAGINAS_INSERVIBLE:
        avisos.append(
            f"BUDGET: the design material is equivalent to {p:.1f} pages, "
            f"above the historical {PAGINAS_INSERVIBLE}-page planning assumption. "
            f"Consider splitting the package into reviewable use-case scopes; "
            f"calibrate session size with the actual team.")
    elif p > PAGINAS_RECOMENDADO:
        avisos.append(
            f"BUDGET: {p:.1f} equivalent pages, above the "
            f"{PAGINAS_RECOMENDADO}-page historical session-size assumption. "
            f"Suggested: {pres['sesiones']} sessions; calibrate with the review team.")


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def validar(mod, secuencias, specs, robustez, dominio, req_texto,
            pruebas_texto, hay):
    errores, avisos, infos = [], [], []
    capas, degradadas = {}, []
    specs = [texto_documento(t) for t in specs]
    req_texto = texto_documento(req_texto)
    pruebas_texto = texto_documento(pruebas_texto)

    # Paths only prove that an input was supplied. Every artifact must expose
    # the evidence used by its dependent checks before those checks are complete.
    suministrados, hay = hay, dict(hay)
    specs_utiles = [t for t in specs if especificacion_util(t)]
    robustez_util = [t for t in robustez if parse_controladores(t)]
    hay.update({
        "spec": bool(specs_utiles) and len(specs_utiles) == len(specs),
        "robustez": bool(robustez_util) and len(robustez_util) == len(robustez),
        "dominio": bool(dominio),
        "requisitos": bool(requisitos_de(req_texto)),
        "pruebas": bool(pruebas_de(pruebas_texto)),
    })
    for entrada in ("spec", "robustez", "dominio", "requisitos", "pruebas"):
        if suministrados[entrada] and not hay[entrada]:
            avisos.append(
                f"EVIDENCE: --{entrada} contains an empty or unrecognized artifact; "
                f"dependent checks are not fully verified.")

    if check_modelo_vacio(mod, errores):
        capas["empty model"] = "executed"
        return errores, avisos, infos, capas, [], None, {}

    detener = check_criterio_entrada(mod, secuencias, specs_utiles, errores, avisos)
    capas["entry criteria"] = "executed"
    if detener:
        return errores, avisos, infos, capas, [], None, {"detenido": True}

    # The blocks are well closed and I empty them `leer()`; what remains is a
    # `/'` orphan, and that is why it is enough to look at the already processed text.
    check_comentario_sin_cerrar(
        [(mod.path, mod.text)] + [(s.path, s.text) for s in secuencias], avisos)
    check_no_parseadas(mod, avisos)
    check_r3_firmas(mod, avisos)
    check_r7_responsabilidades(mod, dominio, hay["dominio"], avisos)
    check_envoltorio(mod, avisos)
    check_abstraccion_inestable(mod, avisos)
    check_multiplicidades(mod, avisos)
    check_lineas_vida_huerfanas(secuencias, avisos)
    capas["rule 3 (types and signatures)"] = "executed"
    capas["rule 7 (responsibilities)"] = "executed"

    huerfanas = check_r8_asignacion(mod, secuencias, errores, avisos)
    check_r6_patrones(mod, secuencias, avisos)
    capas["rule 8 (assignment)"] = "executed"
    capas["rule 6 (real design)"] = "executed"

    faltan9 = check_r9_flujos(secuencias, specs_utiles, errores) if specs_utiles else 0
    if hay["spec"]:
        capas["rule 9 (alternative courses)"] = "executed"
        capas["rule 10 (sequence vs text)"] = "executed (partial: the "\
            "faithful pairing is judged by one person)"
    else:
        for c in ("rule 9 (alternative courses)", "rule 10 (sequence vs text)"):
            capas[c] = ("PARTIAL - some supplied specifications have no usable CU behavior"
                        if specs_utiles else "NOT EXECUTED - use case specification missing or unusable")
            degradadas.append(c)

    if hay["requisitos"]:
        traza = check_r5_trazabilidad(mod, req_texto, specs_utiles, avisos)
        if hay["spec"]:
            capas["rule 5 (traceability)"] = "executed"
        else:
            capas["rule 5 (traceability)"] = "PARTIAL - use case specification missing or unusable"
            degradadas.append("rule 5 (traceability)")
    else:
        traza = {}
        capas["rule 5 (traceability)"] = "NOT EXECUTED - requirements are missing"
        degradadas.append("rule 5 (traceability)")

    if hay["pruebas"]:
        controladores = []
        for t in robustez_util:
            controladores += parse_controladores(t)
        check_r1_pruebas(controladores, pruebas_texto, secuencias, specs_utiles, avisos)
        if hay["robustez"] and hay["spec"]:
            capas["rule 1 (test plan)"] = "executed"
        else:
            capas["rule 1 (test plan)"] = (
                "PARTIAL - robustness diagrams or specifications missing or unusable")
            degradadas.append("rule 1 (test plan)")
    else:
        capas["rule 1 (test plan)"] = "NOT EXECUTED - test plan missing"
        degradadas.append("rule 1 (test plan)")

    if not hay["dominio"]:
        capas["contrast with dominance"] = "NOT EXECUTED - domain model missing"
        degradadas.append("contrast with dominance")

    # Rule #4 is not automatable and #2 is only half automatable. They do not degrade:
    # It is not work that could have been done and was not done, it is work that no one
    # tool can do.
    capas["rule 4 (programmer validation)"] = \
        "NOT AUTOMATABLE - it is determined by a person who is going to build it"
    capas["rule 2 (code headers)"] = \
        "PARTIAL BY NATURE - the generation is automated; the inspection does not"

    pres = presupuesto(mod, secuencias, pruebas_texto)
    check_presupuesto(pres, avisos)

    metricas = {"operaciones_sin_mensaje": huerfanas, "flujos_sin_disenar": faltan9,
                "trazabilidad": traza}
    return errores, avisos, infos, capas, degradadas, pres, metricas


def veredicto_propuesto(errores, avisos, degradadas, detenido):
    """The verdict is DETERMINED by the decision maker (IEEE 1028 §5.2.1).
    This is a proposal with its condition.

    The gradient layers arrive as EXPLICIT PARAMETER. in a skill
    sister, the capes were declared, they were printed, and the verdict came out
    favorable also because the function that calculates it did not receive them.
    """
    if detenido:
        return ("NOT REVIEWED - ENTRY CRITERIA NOT MET",
                "The source requires complete sequences and synchronized model "
                "before convening the CDR.")
    if errores:
        return ("REINSPECTION REQUIRED",
                f"{len(errores)} open error level finding(s).")
    if degradadas:
        return ("NOT FULLY VERIFIED",
                f"{len(degradadas)} rule(s) not executed due to lack of "
                f"supplies: {', '.join(degradadas)}.")
    if avisos:
        return ("ACCEPTED WITH REWORK VERIFICATION",
                f"No errors, but {len(avisos)} warning(s) require your "
                f"judgment and, if appropriate, verified correction.")
    # "ACCEPTED" here means: everything AUTOMATABLE was executed and came out.
    # clean. Rules #4 (programmers say if it is constructible) and the
    # inspection of #2 is not covered by any tool, and that is why it is not
    # enter `degradadas` —it is not work that could have been done and was not done—,
    # but they cannot be assumed satisfied. Say it in your own
    # verdict prevents someone from reading "ACCEPTED" as "fully reviewed."
    return ("ACCEPTED (subject to the two non-automatable rules)",
            "Entry criterion met, all automatable rules "
            "executed, zero errors and zero warnings. SLOPE of the "
            "rule #4—have someone who is going to build it confirm that it is "
            "constructible—and the inspection of the headers (#2). Without those "
            "Two, the “Accepted” disposition is not complete.")


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    p = argparse.ArgumentParser(
        description="Prepare the MKL Critical Design Review (CDR).")
    p.add_argument("--clases", required=True, help="design class model (.puml)")
    p.add_argument("--secuencia", action="append", default=[], required=True,
                   help="sequence diagram (.puml). Repeatable.")
    p.add_argument("--spec", action="append", default=[],
                   help="use case specification (.md). Repeatable.")
    p.add_argument("--robustez", action="append", default=[],
                   help="robustness diagram (.puml). Repeatable.")
    p.add_argument("--dominio", help="domain model (.puml)")
    p.add_argument("--requisitos", help="requirements list (.md)")
    p.add_argument("--pruebas", help="test plan (.md)")
    args = p.parse_args(argv)

    mod = parse_clases(args.clases, leer(args.clases))
    # Repeated paths are counted once: pass the same file twice
    # inflated the session budget without contributing anything.
    rutas_sec = list(dict.fromkeys(args.secuencia))
    secuencias = [parse_secuencia(s, leer(s)) for s in rutas_sec]
    specs = [leer(s) for s in dict.fromkeys(args.spec)]
    robustez = [leer(r) for r in args.robustez]
    dom_text = leer(args.dominio) if args.dominio else ""
    dominio = parse_dominio(dom_text) if args.dominio else {}
    req_texto = leer(args.requisitos) if args.requisitos else ""
    pruebas_texto = leer(args.pruebas) if args.pruebas else ""

    hay = {"spec": bool(args.spec), "robustez": bool(args.robustez),
           "dominio": bool(args.dominio), "requisitos": bool(args.requisitos),
           "pruebas": bool(args.pruebas)}

    errores, avisos, infos, capas, degradadas, pres, metricas = validar(
        mod, secuencias, specs, robustez, dominio, req_texto, pruebas_texto, hay)

    n_ops = sum(len(c.operaciones) for c in mod.clases.values())
    n_recepciones = sum(len(c.recepciones) for c in mod.clases.values())
    n_attrs = sum(len(c.atributos) for c in mod.clases.values())

    print("Critical Design Review (CDR) - automated preparation")
    print("=" * 60)
    print(f"Classes: {len(mod.clases)} | Attributes: {n_attrs} | "
          f"Operations: {n_ops} | Receptions: {n_recepciones} | Relationships: {len(mod.relaciones)}")
    print(f"Sequences: {len(secuencias)} | Specifications: {len(specs)} | "
          f"Robustness: {len(robustez)}")
    print()

    if pres:
        print("SESSION BUDGET")
        print(f"  design material ......... {pres['paginas_diseno']:.1f} equivalent "
              f"pages (convention: {LINEAS_POR_PAGINA} lines/page)")
        if pres["paginas_pruebas"]:
            print(f"  test plan ............ {pres['paginas_pruebas']:.1f} pages")
        print(f"  planning assumption ...... {PPH_DISENO_DETALLADO[0]}-"
              f"{PPH_DISENO_DETALLADO[1]} page/hour (historical upstream rate; "
              f"calibrate locally)")
        print(f"  estimate ................. {pres['horas'][0]:.1f} to "
              f"{pres['horas'][1]:.1f} hours")
        print(f"  suggested sessions ......... {pres['sesiones']}")
        print()

    print("RULES COVERAGE")
    for c in sorted(capas):
        print(f"  {c}: {capas[c]}")
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

    estado, razon = veredicto_propuesto(
        errores, avisos, degradadas, bool(metricas.get("detenido")))
    print(f"PROPOSED VERDICT: {estado}")
    print(f"  {razon}")
    print()
    print("This verdict is a PROPOSAL. It is determined by the decision "
          "maker (IEEE 1028 §5.2.1), who is you: the skill conducts the review "
          "and recommends; the decision is yours. Errors are verifiable "
          "violations; warnings require your judgment. Rule #4 and "
          "the inspection required by #2 are not covered by any tool.")

    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
