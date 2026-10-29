#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Generate code headers from the class model (CDR rule #2).

Translate modeled members into review skeletons and report conversion gaps.
Compare the output with the source model before making implementation decisions.

Why it works: A diagram tolerates ambiguity and a signature does not.
`process(data)` looks plausible in a diagram box but exposes unanswered questions in
`??? process(??? data)`. This does not find new defects: it makes visible
those that the diagram hid.

IMPORTANT - this is NOT production code. It is a review instrument.
Gaps are MARKED with `???`, never filled: inventing a missing type
would destroy the very finding that rule #3 seeks.

Usage:
    python generate_code_headers.py --clases model_design_classes.puml \\
        [--id CDR-01] [--salida headers.txt]

Exit codes:
    0 generated
    2 usage error or file not found
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import tempfile

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from validate_cdr import (  # Noqa: E402
    parse_clases, parse_generalizaciones, leer, clave, norm, parametros_de,
    limites_multiplicidad, TIPOS_IMPRECISOS,
)

HUECO = "???"


def tipo_o_hueco(t: str) -> str:
    """An absent type is output as ???, not as Object.

    Filling with a generic type would convert a rule #3 finding into
    apparently valid code, which is exactly the opposite of what
    that the headers are generated.
    """
    t = (t or "").strip()
    return t if t else HUECO


def params_de(crudo: str) -> str:
    """Normalizes the list of parameters, marking those that do not have a type."""
    crudo = (crudo or "").strip()
    if not crudo:
        return ""
    partes = []
    for nombre, tipo, defecto in parametros_de(crudo):
        valor = f" = {defecto}" if defecto else ""
        partes.append(f"{tipo_o_hueco(tipo)} {nombre}{valor}")
    return ", ".join(partes)


VIS = {"+": "public", "-": "private", "#": "protected", "~": ""}


def visibilidad(v: str) -> str:
    return VIS.get(v, "public") or ""


def campos_de_relaciones(mod):
    """The relationships are output as fields, because that is where the
    absent multiplicity becomes visible: without it one does not know if a field
    It is a reference or a collection.

    Three rules that a previous version did not respect and produced Java
    invalid:

    1. **Address.** `A --> B` is navigable from A to B: only A receives the field.
       Broadcasting it also in B invented a reverse reference that no one
       drawing. The same with aggregation and composition: the field goes from
       side of the rhombus, which is who owns it.
    2. **Deduplication by (destination, label), not just by destination.** Two
       relations between the same pair of classes produced two fields with the
       same name, one with `???` in the type. But deduplicate only by
       destiny was to go overboard: two different LABELED associations
       —`Persona --> Direccion : facturacion` and `: envio`— are two fields
       legitimate, and one disappeared in silence. The label enters the
       key and also gives name to the field.
    3. **enums do not receive fields.** An enum is a set of constants;
       injecting a reference to the user is an artifact of the generator,
       not the model.
    """
    out = {}
    for r in mod.relaciones:
        conn = r["conn"]
        if "<|" in conn or "|>" in conn or ".." in conn:
            continue          # inheritance, realization and dependency are not fields
        pares = []
        if "o-" in conn or "*-" in conn:          # the rhombus is on the left
            pares = [(r["izq"], r["der"], r["multiplicidad_der"], r["multiplicidad_izq"])]
        elif "-o" in conn or "-*" in conn:        # the rhombus is on the right
            pares = [(r["der"], r["izq"], r["multiplicidad_izq"], r["multiplicidad_der"])]
        elif ">" in conn and "<" not in conn:     # A --> B, navigable A->B
            pares = [(r["izq"], r["der"], r["multiplicidad_der"], r["multiplicidad_izq"])]
        elif "<" in conn and ">" not in conn:     # A <-- B, navigable B->A
            pares = [(r["der"], r["izq"], r["multiplicidad_izq"], r["multiplicidad_der"])]
        else:                                     # directionless association
            pares = [(r["izq"], r["der"], r["multiplicidad_der"], r["multiplicidad_izq"]),
                     (r["der"], r["izq"], r["multiplicidad_izq"], r["multiplicidad_der"])]
        etiqueta = re.sub(r"[^\w]+", "", (r.get("etiqueta") or "").strip())
        for origen, destino, multiplicidad, mult_origen in pares:
            k = clave(origen)
            c = mod.clases.get(k)
            if not c or c.kind == "enum":
                continue
            previo = out.setdefault(k, {})
            ident = (destino, etiqueta)
            anterior = previo.get(ident)
            # The one that provides multiplicity remains: it is the only one that resolves
            # whether the field is a reference or a collection.
            if anterior is None or (multiplicidad and not anterior[0]):
                previo[ident] = (multiplicidad, mult_origen, r["linea"])
    return {k: [(d, et, m, mo, ln) for (d, et), (m, mo, ln) in sorted(v.items())]
            for k, v in out.items()}


def nombre_campo(destino: str, etiqueta: str, ocupados=()) -> str:
    """VALID field name and no collisions.

    Three things that a previous version did not do and produced Java that it did not
    compiles:
      - A label like "1 to many" gave `1amuchosProducto`, which begins
        by digit: invalid identifier.
      - An attribute `direccion` and an untagged relationship to `Direccion`
        They gave two fields `direccion`.
      - Neither of them was notified.
    """
    base = destino[:1].lower() + destino[1:]
    if etiqueta:
        base = etiqueta[:1].lower() + etiqueta[1:] + destino[:1].upper() + destino[1:]
    if base and base[0].isdigit():          # invalid identifier in java
        base = "_" + base
    nombre, n = base, 2
    while nombre in ocupados:               # collision with an attribute or with
        nombre = f"{base}{n}"               # another field already issued
        n += 1
    return nombre


def tipo_relacion(destino: str, multiplicidad: str) -> str:
    """Preserve the relevant association end, including its optionality."""
    limites = limites_multiplicidad(multiplicidad)
    if limites is None:
        return destino + HUECO
    minimo, maximo = limites
    if maximo == 0:
        return destino + HUECO
    if maximo is None or maximo > 1:
        return f"List<{destino}>"
    return f"Optional<{destino}>" if minimo == 0 else destino


def generar(mod, identificador: str) -> tuple:
    padres = parse_generalizaciones(mod)
    campos = campos_de_relaciones(mod)
    huecos = []
    L = []
    L.append(f"/* HEADERS GENERATED FOR INSPECTION - {identificador}")
    L.append(" * Review instrument, NOT production code.")
    L.append(f" * Generated from: {mod.path}")
    L.append(" * Review the model and conversion diagnostics before correcting the source.")
    L.append(f" * Gaps are marked with {HUECO}; review all unresolved or unsupported syntax.")
    L.append(" * List/Optional preserve multiplicity; exact bounds remain in comments. */")
    L.append("")

    for k, c in mod.clases.items():
        decl = "interface" if c.kind == "interface" else (
            "enum" if c.kind == "enum" else "class")
        abst = "abstract " if c.es_abstracta and decl == "class" else ""
        # `padres` saves SETS: a class can extend a base and
        # implement various interfaces. They are separated by what each one is.
        extiende_l, implementa_l = [], []
        for p in sorted(padres.get(k, ())):
            pc = mod.clases.get(p)
            if not pc:
                continue
            (implementa_l if pc.kind == "interface" else extiende_l).append(pc.nombre)
        extiende = ""
        if extiende_l:
            extiende += " extends " + ", ".join(extiende_l)
        if implementa_l:
            extiende += " implements " + ", ".join(implementa_l)
        marca = "  // <<solucion>>" if c.es_solucion else ""
        L.append(f"public {abst}{decl} {c.nombre}{extiende} {{{marca}")
        for ln, texto in c.no_parseadas:
            huecos.append(
                f"{c.nombre}: unsupported modeled member '{texto}' (L{ln}); "
                f"it could not be translated faithfully")
        for recepcion in c.recepciones:
            # A UML reception is a separate behavioral declaration. Do not
            # invent an ordinary operation or silently omit its contract.
            L.append(f"    // Signal reception (not an Operation): "
                     f"{recepcion.visibilidad}<<signal>> {recepcion.nombre}({recepcion.params})")
            huecos.append(
                f"{c.nombre}.{recepcion.nombre}: Signal reception requires a "
                f"language-specific mapping (L{recepcion.linea}); review the preserved signature")

        if c.kind == "enum":
            # The constants of an enum have no type or visibility: they are not
            # attributes. `validate_cdr.py` already excludes them from rule #3; he
            # generator should be consistent with that or both scripts
            # brothers contradict the same model.
            L.append("    " + ", ".join(a.nombre for a in c.atributos) + ";")
            L.append("}")
            L.append("")
            continue

        for a in c.atributos:
            t = tipo_o_hueco(a.tipo)
            if t == HUECO:
                huecos.append(f"{c.nombre}.{a.nombre}: untyped attribute (L{a.linea})")
            elif norm(t) in TIPOS_IMPRECISOS:
                huecos.append(f"{c.nombre}.{a.nombre}: imprecise type '{t}' (L{a.linea})")
            marcas = [f"derived property /{a.nombre}"] if a.derivado else []
            if a.multiplicidad:
                limites = limites_multiplicidad(a.multiplicidad)
                t = tipo_relacion(t, a.multiplicidad)
                marcas.append(f"multiplicity {a.multiplicidad}")
                if limites is None or limites[1] == 0:
                    huecos.append(
                        f"{c.nombre}.{a.nombre}: unsupported property multiplicity "
                        f"'{a.multiplicidad}' (L{a.linea}); cannot select a faithful field type")
            v = visibilidad(a.visibilidad)
            est = "static " if a.estatico else ""
            anotacion = "  // " + "; ".join(marcas) if marcas else ""
            L.append(f"    {v + ' ' if v else ''}{est}{t} {a.nombre};{anotacion}")

        ocupados = {a.nombre for a in c.atributos}
        for destino, etiqueta, multiplicidad, mult_origen, ln in campos.get(k, []):
            campo = nombre_campo(destino, etiqueta, ocupados)
            if campo != nombre_campo(destino, etiqueta):
                huecos.append(
                    f"{c.nombre}: the relationship field towards '{destino}' "
                    f"It clashed with a name already used; was issued as '{campo}' "
                    f"(L{ln}). Rename in the model, not here.")
            ocupados.add(campo)
            # A relationship to a class that the model does not declare: the
            # generator cannot invent the type, and keeping it quiet would produce a
            # header that does not compile without saying why.
            if clave(destino) not in mod.clases:
                huecos.append(
                    f"{c.nombre} -> {destino}: the relationship points to a class "
                    f"that the model does NOT declare (L{ln}). Either the class is missing, or "
                    f"over the relationship.")
            tipo = tipo_relacion(destino, multiplicidad)
            if not multiplicidad:
                huecos.append(
                    f"{c.nombre} -> {destino}: relationship without multiplicity, not known "
                    f"Do you know if it is a reference or a collection (L{ln})")
            elif HUECO in tipo:
                huecos.append(
                    f"{c.nombre} -> {destino}: unsupported multiplicity "
                    f"'{multiplicidad}' (L{ln}); cannot select a faithful field type")
            if not mult_origen:
                huecos.append(
                    f"{c.nombre} -> {destino}: source multiplicity missing (L{ln})")
            elif limites_multiplicidad(mult_origen) is None:
                huecos.append(
                    f"{c.nombre} -> {destino}: unsupported source multiplicity "
                    f"'{mult_origen}' (L{ln}); its bounds cannot be verified")
            marca_mult = (f"  // multiplicity {multiplicidad or HUECO}; "
                          f"source multiplicity {mult_origen or HUECO}")
            L.append(f"    private {tipo} {campo};{marca_mult}")

        if c.atributos or campos.get(k):
            L.append("")

        for o in c.operaciones:
            ret = tipo_o_hueco(o.tipo)
            if ret == HUECO:
                huecos.append(f"{c.nombre}.{o.nombre}(): no return value (L{o.linea})")
            elif norm(ret) in TIPOS_IMPRECISOS:
                huecos.append(f"{c.nombre}.{o.nombre}(): imprecise return '{ret}' (L{o.linea})")
            ps = params_de(o.params)
            if HUECO in ps:
                huecos.append(f"{c.nombre}.{o.nombre}(): untyped parameters (L{o.linea})")
            v = visibilidad(o.visibilidad)
            # The body depends on the MEMBER, not just the class: within
            # In an abstract class, abstract and concrete methods coexist, and
            # emit them all without a body towards the LEAST faithful generated signature
            # than the source diagram — the opposite of the purpose.
            es_abstracto = o.abstracto or c.kind == "interface"
            mods = ("static " if o.estatico else "") + ("abstract " if o.abstracto else "")
            cuerpo = ";" if es_abstracto else " { }"
            L.append(f"    {v + ' ' if v else ''}{mods}{ret} {o.nombre}({ps}){cuerpo}")

        L.append("}")
        L.append("")

    return "\n".join(L), huecos


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    p = argparse.ArgumentParser(
        description="Generates code headers for inspection (CDR rule #2).")
    p.add_argument("--clases", required=True)
    p.add_argument("--id", default="CDR-XX", help="record identifier")
    p.add_argument("--salida", help="destination file; default stdout")
    args = p.parse_args(argv)

    if args.salida:
        origen, destino = Path(args.clases), Path(args.salida)
        try:
            mismo = origen.resolve() == destino.resolve()
            if origen.exists() and destino.exists():
                mismo = mismo or os.path.samefile(origen, destino)
            if mismo:
                print("Input and output must be different files; the source model was not changed.",
                      file=sys.stderr)
                return 2
        except OSError as exc:
            print(f"Cannot inspect output destination: {args.salida}: {exc}", file=sys.stderr)
            return 2

    mod = parse_clases(args.clases, leer(args.clases))
    if not mod.clases:
        print("The model declares no class: nothing to generate.",
              file=sys.stderr)
        return 2

    texto, huecos = generar(mod, args.id)

    if args.salida:
        temporal = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False,
                                             dir=str(Path(args.salida).parent)) as fh:
                temporal = fh.name
                fh.write(texto + "\n")
            os.replace(temporal, args.salida)
        except OSError as exc:
            print(f"Cannot write headers: {args.salida}: {exc}", file=sys.stderr)
            return 2
        finally:
            if temporal and os.path.exists(temporal):
                os.unlink(temporal)
        print(f"Headers written to {args.salida}")
    else:
        print(texto)

    print()
    print("WHAT THE TRANSLATION TO CODE REVEALS")
    if huecos:
        print(f"  {len(huecos)} gap(s) requiring model or conversion review:")
        for h in huecos:
            print(f"  - {h}")
    else:
        print("  No typing gaps found. Human inspection must still check for")
        print("  duplicate operations, unnecessary dependencies,")
        print("  and redundant parameters.")
    print()
    print("Historical planning assumption: 100 pages/hour or 200 lines/hour. "
          "Calibrate this estimate to the actual review team; it is not an acceptance threshold.")
    print("Remember: this is NOT production code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
