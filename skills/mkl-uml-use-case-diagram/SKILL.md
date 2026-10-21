---
name: mkl-uml-use-case-diagram
description: Create, review, refactor, and validate UML use case diagrams in PlantUML. Use to identify system boundaries, participating actors, user goals, and justified include, extend, or generalization relationships.
license: Apache-2.0
metadata:
  author: kingle.zhuang
  email: kinglezhuang@vip.qq.com
  copyright: 2026 kingle.zhuang
  organization: mkl
---
# MKL UML Use Case Diagram

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
| Generate | System scope and actor goals | Requirements, domain model, existing CU registry |
| Review/refactor/validate | Existing use case diagram | Specifications and requirements for coverage checks |

A domain model is useful context, not a prerequisite for drawing an independently requested use case view. The diagram summarizes goals; textual specifications carry the behavior.

## Modeling decisions

1. Establish the subject boundary and external actor roles. Actors may be people, organizations, devices, or external systems.
2. Identify actor-valued goals at a consistent level. Do not add CRUD, authentication, reporting, or a dominant use case merely to satisfy a fixed template.
3. Associate every participating actor with the use case, including supporting actors that exchange messages or data. Initiation is a separate role; an association need not imply initiation. Prefer an undirected actor association unless direction has a defined project meaning.
4. Use `include` for required reused behavior, directed from the including case to the included case. Use `extend` for conditional extension, directed from the extension to the base; name its condition/extension point when relevant.
5. Use actor/use case generalization only with substitutable behavior. Avoid relationship proliferation when plain associations explain the scope.
6. Preserve CU identifiers independently of display order or goal prominence. Reordering or choosing a different dominant goal must not renumber existing cases.

## Output and verification

Return a readable PlantUML view with explicit subject boundary, actors outside it, stable aliases, and meaningful goal names. Include a compact actor/goal/source map when traceability is requested. For code-only output, omit compulsory audit attachments.

From this skill directory, this executable command runs the bundled MKL diagram profile; `path/to/diagram.puml` is an input placeholder:

```bash
python scripts/validate_use_case_puml.py path/to/diagram.puml
```

Report actual execution, exit status, and relevant findings. Lexical/diagram heuristics do not prove goal quality or UML conformance; inspect those decisions and rendering separately.

## Focused references

- For actor participation and UML relationship semantics, read [standards-alignment.md](references/standards-alignment.md).
- For goal selection or detailed review, read [use-case-diagram-rubric.md](references/use-case-diagram-rubric.md).
- For a demonstrated modeling smell, consult [anti-patterns.md](references/anti-patterns.md).
- For comparative domain examples, consult [regression-examples.md](references/regression-examples.md).
