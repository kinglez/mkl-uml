# Located required-control checks

Use this optional PDR record when a known behavior requires a specific control and
the review needs to check that control's connection to its interaction entry. A
diagram-only review remains useful without it; the checker warns on an isolated
control rather than guessing whether that control is mandatory.

```bash
python3 scripts/validate_pdr.py --robustez diagram.puml --behavior-map behavior-map.json
```

Suppose `behavior.md` contains this actual second source line:

```text
3. The System evaluates the constraint before handling the request.
```

Place this record alongside that source and the reviewed diagram:

```json
{
  "schema_version": 1,
  "required_controls": [{
    "diagram": "diagram.puml",
    "entry": "B_Input",
    "control": "C_Evaluate",
    "step": "3",
    "source": "behavior.md",
    "line": 2,
    "quote": "3. The System evaluates the constraint before handling the request."
  }]
}
```

`entry` is the exact boundary alias for the mapped step's interaction, not necessarily
the first screen in the entire use case. `control` is its exact required-control alias.
`step` retains the supplied step/requirement identifier for traceability and diagnostics;
the checker does not infer step semantics from its spelling or translate the source.
`source` and `diagram` are local paths relative to the record and contained in its
directory tree. Symlink escapes are rejected. The diagram must be an actual supplied
`--robustez` target. `line` is a positive one-based source line and `quote` must match
that entire line, ignoring surrounding whitespace. Multiple entries can cover different
steps or diagrams. Unknown fields, duplicate keys/entries and an empty list are rejected.

The author declares that the located source requires this responsibility; the checker
verifies the source location and aliases, not the source's authority or the semantic
adequacy of that interpretation. Preserve the actual source. A fabricated requirement
or a convenient unrelated excerpt cannot justify a mapped control.

## Structural interpretation

- An isolated control in a complete graph produces a warning and preserves exit 0.
- A mapped required control must exist and be reachable from its specified boundary
  through boundary-to-control and control-to-control coordination links. An absent
  alias or unreachable control in a complete diagram is a finding, exit 1.
- Shared entities, actors and other boundaries are not coordination shortcuts for this
  local step. Map a later interaction to its own entry boundary when appropriate.
- Hidden layout edges, note links and commented examples do not connect controls.
- Unresolved endpoints or unsupported BCE syntax make connectivity partial. The checker
  does not convert an absence in that incomplete graph into an error.
- A stale source excerpt, wrong alias role, unmapped diagram, invalid JSON or missing
  record/source file is an input failure, exit 2.

This is a local MKL review convention, not a UML requirement or a temporal proof.
Reachability cannot prove that every execution traverses the control, that a check
precedes a content return, or that another path cannot bypass it. Inspect those
semantic obligations manually against the behavior and later interactions. A
checked map does not replace missing specifications, domain evidence or formal PDR
acceptance, and unlisted controls remain ordinary structural/semantic review subjects.
