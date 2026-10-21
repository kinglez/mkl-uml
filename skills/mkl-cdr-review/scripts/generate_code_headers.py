#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Generate code headers from the class model (CDR rule #2).

    "Generate the code headers for your classes, and inspect them closely."
    "See, we told you that you were about to generate code. Once you've done
     so, inspect the code headers carefully."

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
import re
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from validate_cdr import (  # Noqa: E402
    parse_clases, parse_generalizaciones, leer, clave, norm, TIPOS_IMPRECISOS,
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
    for p in crudo.split(","):
        p = p.strip()
        if not p:
            continue
        if ":" in p:
            nombre, tipo = p.split(":", 1)
            partes.append(f"{tipo_o_hueco(tipo)} {nombre.strip()}")
        else:
            partes.append(f"{HUECO} {p}")
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
            pares = [(r["izq"], r["der"])]
        elif "-o" in conn or "-*" in conn:        # the rhombus is on the right
            pares = [(r["der"], r["izq"])]
        elif ">" in conn and "<" not in conn:     # A --> B, navigable A->B
            pares = [(r["izq"], r["der"])]
        elif "<" in conn and ">" not in conn:     # A <-- B, navigable B->A
            pares = [(r["der"], r["izq"])]
        else:                                     # directionless association
            pares = [(r["izq"], r["der"]), (r["der"], r["izq"])]
        etiqueta = re.sub(r"[^\w]+", "", (r.get("etiqueta") or "").strip())
        for origen, destino in pares:
            k = clave(origen)
            c = mod.clases.get(k)
            if not c or c.kind == "enum":
                continue
            previo = out.setdefault(k, {})
            ident = (destino, etiqueta)
            anterior = previo.get(ident)
            # The one that provides multiplicity remains: it is the only one that resolves
            # whether the field is a reference or a collection.
            if anterior is None or (r["multiplicidad"] and not anterior[0]):
                previo[ident] = (r["multiplicidad"], r["linea"])
    return {k: [(d, et, m, ln) for (d, et), (m, ln) in sorted(v.items())]
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


def generar(mod, identificador: str) -> tuple:
    padres = parse_generalizaciones(mod)
    campos = campos_de_relaciones(mod)
    huecos = []
    L = []
    L.append(f"/* HEADERS GENERATED FOR INSPECTION - {identificador}")
    L.append(" * Review instrument, NOT production code.")
    L.append(f" * Generated from: {mod.path}")
    L.append(" * Do not edit: if something is wrong, it is wrong in the model.")
    L.append(f" * Gaps are marked with {HUECO}; they are findings, not")
    L.append(" * generator oversights. */")
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
            v = visibilidad(a.visibilidad)
            est = "static " if a.estatico else ""
            L.append(f"    {v + ' ' if v else ''}{est}{t} {a.nombre};")

        ocupados = {a.nombre for a in c.atributos}
        for destino, etiqueta, tiene_mult, ln in campos.get(k, []):
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
            if not tiene_mult:
                huecos.append(
                    f"{c.nombre} -> {destino}: relationship without multiplicity, not known "
                    f"Do you know if it is a reference or a collection (L{ln})")
                L.append(f"    private {destino}{HUECO} {campo};")
            else:
                L.append(f"    private {destino} {campo};")

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

    mod = parse_clases(args.clases, leer(args.clases))
    if not mod.clases:
        print("The model declares no class: nothing to generate.",
              file=sys.stderr)
        return 2

    texto, huecos = generar(mod, args.id)

    if args.salida:
        with open(args.salida, "w", encoding="utf-8") as fh:
            fh.write(texto + "\n")
        print(f"Headers written to {args.salida}")
    else:
        print(texto)

    print()
    print("WHAT THE TRANSLATION TO CODE REVEALS")
    if huecos:
        print(f"  {len(huecos)} gap(s) that the diagram concealed:")
        for h in huecos:
            print(f"  - {h}")
    else:
        print("  No typing gaps found. Human inspection must still check for")
        print("  duplicate operations, unnecessary dependencies,")
        print("  and redundant parameters.")
    print()
    print(f"Applicable inspection rate: {100} pages/hour or 200 lines/hour "
          f"(IEEE 1028 §6.5.2, row 'Source code'). It is much faster than "
          f"review design, so this check takes little time.")
    print("Remember: this is NOT production code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
