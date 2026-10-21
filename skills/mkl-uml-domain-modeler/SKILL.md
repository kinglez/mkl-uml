---
name: mkl-uml-domain-modeler
description: Create, review, refactor, and validate conceptual UML domain models in PlantUML from business descriptions, requirements, or user stories. Use for domain vocabulary and conceptual relationships before implementation design.
license: Apache-2.0
metadata:
  author: kingle.zhuang
  email: kinglezhuang@vip.qq.com
  copyright: 2026 kingle.zhuang
  organization: mkl
---
# MKL UML Domain Modeler

## Operating contract

- Use **standalone** mode by default: complete the requested artifact from the supplied evidence. Use **MKL workflow** mode when the user requests its cross-artifact handoff or formal gate.
- Treat generate, review, refactor, and validate as operations within either mode. Preserve existing scope and authorization; do not ask again for an already authorized correction.
- Review/refactor/validate requires the target artifact. Generation requires a stated goal and enough behavior to model it; record assumptions and ask only for information that changes the result.
- Report verification coverage as **checked**, **partial**, or **blocked**, with the checks run and missing evidence. Missing upstream artifacts limit cross-artifact checks; they do not block useful standalone work. A partial check cannot establish formal acceptance.
- Preserve supplied identifiers and their mappings across renaming, reordering, splitting, and regeneration. Allocate new identifiers above the existing high-water mark; retain retired identifiers and never reuse them. If the registry is unavailable, mark new IDs provisional. Diagram aliases are separate from traceability IDs.
- Distinguish UML semantics, local MKL conventions, and heuristic findings. Run a scoped verification pass and recheck affected parts after corrections. Do not require a fixed number of clean passes or issue an assurance certificate from a validator result.

## Inputs and result

| Operation | Minimum input | Result |
|---|---|---|
| Generate | Business scope and relevant concepts or behavior | Conceptual `.puml` model and assumptions |
| Review/refactor/validate | Existing domain model; requirements when available | Located findings or a revised model; verification limits |
| MKL handoff | Domain model plus supplied requirements/specifications | Vocabulary map and justified domain delta |

## Modeling decisions

1. Identify domain concepts from business meaning and identity; noun extraction is a candidate-finding aid. Separate attributes, values, actors, interfaces, and implementation classes.
2. Model only relationships supported by the evidence. Assign role names and multiplicities from business constraints; leave an uncertainty explicit rather than guessing.
3. Prefer a plain association. Use generalization for substitutable domain specializations. Use composition only for justified exclusive composite ownership: a part has at most one composite at a time and may be detached before composite deletion.
4. A derived property `/name` is computable from other information. UML does not prescribe whether its value is stored, cached, indexed, or recomputed.
5. Keep conceptual operations and infrastructure out of the default model. Put repositories, controllers, database tables, and frameworks in an explicitly requested design view.
6. Classify vocabulary origins. Domain entities must resolve to the domain model; named screens, external actors, API boundaries, and solution classes belong to their own sources. Propose missing domain concepts as a delta, without inventing their approval.

## Output and verification

Return valid `@startuml` / `@enduml` PlantUML. Keep readable names and stable aliases, show only useful details, and preserve the user's requested notation and language. For a code-only request, return the artifact without a compulsory report bundle.

The bundled validator checks the repository's **strict conceptual profile**, which is narrower than UML. In particular, enriched notation can be valid UML while violating that profile. Report profile findings separately from semantic defects.

From this skill directory, this is an executable command; `path/to/model.puml` is an input placeholder:

```bash
python scripts/validate_domain_puml.py path/to/model.puml
```

State whether it actually ran. Exit 0 means no detected errors under that profile, 1 means findings, and 2 means invocation/input failure. Check syntax with an available PlantUML renderer separately.

## Focused reference

Read [domain-model-rubric.md](references/domain-model-rubric.md) for selection tradeoffs, relationship notation, enriched models, or a detailed review. Do not load it for a trivial local edit unless that decision needs it.
