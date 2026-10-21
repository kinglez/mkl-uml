---
name: mkl-uml-robustness-diagram
description: Create, review, refactor, and validate boundary/control/entity robustness diagrams in PlantUML. Use to analyze a use case before detailed design, check behavior coverage, and discover missing domain concepts.
license: Apache-2.0
metadata:
  author: kingle.zhuang
  email: kinglezhuang@vip.qq.com
  copyright: 2026 kingle.zhuang
  organization: mkl
---
# MKL UML Robustness Diagram

## Operating contract

- Use **standalone** mode by default: complete the requested artifact from the supplied evidence. Use **MKL workflow** mode when the user requests its cross-artifact handoff or formal gate.
- Treat generate, review, refactor, and validate as operations within either mode. Preserve existing scope and authorization; do not ask again for an already authorized correction.
- Review/refactor/validate requires the target artifact. Generation requires a stated goal and enough behavior to model it; record assumptions and ask only for information that changes the result.
- Report verification coverage as **checked**, **partial**, or **blocked**, with the checks run and missing evidence. Missing upstream artifacts limit cross-artifact checks; they do not block useful standalone work. A partial check cannot establish formal acceptance.
- Preserve supplied identifiers and their mappings across renaming, reordering, splitting, and regeneration. Allocate new identifiers above the existing high-water mark; retain retired identifiers and never reuse them. If the registry is unavailable, mark new IDs provisional. Diagram aliases are separate from traceability IDs.
- Distinguish UML semantics, local MKL conventions, and heuristic findings. Run a scoped verification pass and recheck affected parts after corrections. Do not require a fixed number of clean passes or issue an assurance certificate from a validator result.

## Inputs and result

| Operation | Minimum input | Additional MKL evidence |
|---|---|---|
| Generate | Target goal and sufficiently specified flows | CU specification/ID, domain model, actor view, rules |
| Review/refactor/validate | Existing robustness diagram | Flow text and domain model for correspondence/closure |

Generate a scoped preliminary design from supplied behavior. Without a domain model, mark entity closure unverified; without flow text, do not claim textual completeness. Full MKL PDR handoff requires the specification and domain model.

## Modeling decisions

1. Identify actors and system interfaces. A **boundary** represents interaction with a human or external system: screen, API, webhook endpoint, device port, or adapter. Do not invent a GUI for a machine interface.
2. Use **entities** for domain concepts holding state. Resolve them to the supplied domain model when available; propose missing concepts as a domain delta.
3. Use **controls** for use case behavior coordinating boundaries and entities. A control is an analysis responsibility, not an automatic implementation controller class.
4. Apply the local BCE connection profile: actors interact with boundaries; boundaries and entities interact through controls; controls may coordinate controls. Distinguish these method conventions from UML's general relationship rules.
5. Map every relevant basic/alternative/exception behavior to responsibilities and links. Do not treat a noun as an entity or every verb as a separate control mechanically.
6. Trace boundary data to domain attributes where justified. An interface-only field or protocol identifier need not become a domain property.

## Output and verification

Return one readable PlantUML robustness view per requested use case, preserving CU/DR IDs. Add a behavior correspondence map and domain delta for an MKL handoff. Keep sequence timing, operation signatures, and infrastructure details for detailed design unless explicitly requested.

This executable command, run from this skill directory, checks local BCE syntax; the path is a placeholder:

```bash
python scripts/validate_robustness_puml.py path/to/robustness.puml
```

Report actual execution and detected errors separately from manual correspondence checks. Missing evidence makes those checks partial; no script proves complete analysis coverage.

## Focused references

- For BCE notation and allowed links, read [robustness-rules.md](references/robustness-rules.md).
- For a formal PDR handoff, read [audit-gate.md](references/audit-gate.md).
- For a concrete smell, consult [anti-patterns.md](references/anti-patterns.md).
- For source/example interpretation, consult [sources-and-methods.md](references/sources-and-methods.md), [figure-notes.md](references/figure-notes.md), or [regression-examples.md](references/regression-examples.md) as needed.
