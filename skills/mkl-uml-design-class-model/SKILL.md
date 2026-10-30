---
name: mkl-uml-design-class-model
description: Create, review, refactor, and validate UML design class models in PlantUML. Use to model operations, attributes, types, relationships, and responsibility allocation, including traceability from interactions before CDR.
license: Apache-2.0
metadata:
  author: kingle.zhuang
  email: kinglezhuang@vip.qq.com
  copyright: 2026 kingle.zhuang
  organization: mkl
---
# MKL UML Design Class Model

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
| Generate | Requested responsibilities, constraints and design scope | Domain model, sequences/operation delta, CU specifications |
| Review/refactor/validate | Existing design class model | Sequences, domain, specifications and architecture for provenance |

Complete useful standalone class-design work from supplied evidence. Full MKL provenance requires the domain, interaction and behavioral sources; missing sources make that layer partial, not permission to invent it.

## Modeling decisions

1. Separate domain/problem classes from introduced solution classes. Explain a new repository, service, adapter, interface, or pattern by a concrete responsibility and constraint.
2. Trace operations to operation-invoking messages, explicit requirements, contracts, or documented design decisions. Reply labels, signals and lifecycle messages do not automatically become ordinary receiver operations. Preserve inherited/implemented contracts and resolve PlantUML aliases before judging provenance.
3. Give operations appropriate visibility, parameter types, return type, and cohesive receiver. Asynchronous calls require an explicit operation mapping when their sort is ambiguous.
4. Trace attributes to required state and behavior. A derived property `/name` describes derivability; it makes no storage or indexing decision. Keep persistence decisions explicit in their own design context.
5. Use association, dependency, inheritance and composition with their actual semantics. Composition permits at most one composite owner at a time; it does not require permanent attachment or exactly one owner at every instant.
6. Preserve MC/class trace IDs across refactoring. Keep aliases distinct from class names and trace IDs; update their references consistently. Record compatibility implications of public signature changes.
7. When SOLID or an extension/replacement contract is in scope, name the responsibility/change reason, protected variation, common behavior, actual client capabilities and contract ownership. Collect model/source/test evidence alongside member provenance and carry open verification actions to CDR. Model-only evidence leaves source-import and runtime claims partial; record the missing challenge instead of inferring success from interface arrows.

## Output and verification

Return readable PlantUML at the requested abstraction level. For MKL handoff, include an operation/attribute/source map, introduced solution classes, unresolved design decisions, and any domain delta. Do not require code generation or a certificate for a class-diagram request.

This executable command runs the local MKL cross-artifact profile from this skill directory; paths are placeholders:

```bash
python scripts/validate_design_class_puml.py --clases path/to/classes.puml --secuencia path/to/sequence.puml
```

Add existing `--dominio` and `--spec` inputs when relevant; inspect `--help` for the supported CLI. Only `--clases` is mandatory for this tool; omitting a sequence leaves interaction provenance unverified. For class-only work, report that limitation and inspect notation with an available renderer. Lexical matches are evidence candidates, not proof of responsibility correctness.

## Focused references

- For operation/attribute provenance, read [provenance-rules.md](references/provenance-rules.md).
- For signature and relationship syntax, read [notation-rules.md](references/notation-rules.md).
- For full model cleanup before CDR, read [static-model-guidelines.md](references/static-model-guidelines.md).
- For a demonstrated smell or comparative example, consult [anti-patterns.md](references/anti-patterns.md) or [regression-examples.md](references/regression-examples.md); consult [sources-and-methods.md](references/sources-and-methods.md) for attribution.
