---
name: mkl-use-case-specifier
description: Write, complete, review, and refactor textual software use case specifications in Markdown. Use for actor/system behavior, basic, alternative, and exception flows, acceptance criteria, and traceability to diagrams and tests.
license: Apache-2.0
metadata:
  author: kingle.zhuang
  email: kinglezhuang@vip.qq.com
  copyright: 2026 kingle.zhuang
  organization: mkl
---
# MKL Use Case Specifier

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
| Generate/complete | Goal, actors, and known behavior or draft | CU diagram, domain vocabulary, requirements and business rules |
| Review/refactor/validate | Existing specification | Related diagrams and acceptance/test evidence |

Write a lean specification for a bounded goal; expand only when complexity or the requested formal handoff warrants it. Do not demand a complete upstream pipeline for a single specification.

## Specification workflow

1. Preserve the CU ID, goal, actors, trigger, and boundary. Describe preconditions as existing states, not hidden flow steps.
2. Write a numbered basic flow as observable actor/system interaction. A machine-to-machine exchange is a valid interaction; do not invent a human screen.
3. Anchor each alternative/exception to its triggering step, condition, behavior, and resumption or termination. Give success and failure postconditions that can be checked.
4. Separate business rules from implementation decisions. Label assumptions, unresolved decisions, and source evidence rather than silently filling gaps.
5. Classify terms by origin: domain entity/value, actor, boundary/interface, or design concept. Only domain concepts require domain-model closure. Record genuine discoveries in a proposed domain delta.
6. Preserve existing CU/FA/FE/RN/CP IDs and links. Do not allocate IDs from the current display order; identify any supplied collisions before changing them.

## Output and verification

Return the requested Markdown specification and, when useful, a short unresolved-question or delta list. A formal MKL handoff adds explicit links to requirements, actors, relevant domain concepts, flow coverage, and downstream robustness/test work. Do not attach a mandatory audit certificate to a simple request.

From this skill directory, this command is executable; the specification path is a placeholder:

```bash
python scripts/validate_use_case_spec.py path/to/specification.md
```

The validator checks a supported Markdown/legacy vocabulary profile. Inspect semantic completeness and verify flow references separately; passing syntax or lexical checks does not prove behavior completeness. State which checks actually ran.

## Focused references

- For required fields or a full formal handoff, read [use-case-specification-template.md](references/use-case-specification-template.md).
- For ambiguous flows and review findings, read [review-rubric.md](references/review-rubric.md).
- For short worked forms, read [minimal-examples.md](references/minimal-examples.md).
- For source attribution and limits, consult [sources-and-methods.md](references/sources-and-methods.md).
