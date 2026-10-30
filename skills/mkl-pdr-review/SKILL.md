---
name: mkl-pdr-review
description: Review preliminary-design consistency across robustness diagrams, use case specifications, and domain models. Use for a scoped PDR preparation check or a formal MKL gate before detailed design; report coverage, findings and a justified disposition.
license: Apache-2.0
metadata:
  author: kingle.zhuang
  email: kinglezhuang@vip.qq.com
  copyright: 2026 kingle.zhuang
  organization: mkl
---
# MKL PDR Review

## Operating contract

- Use **standalone** mode by default: complete the requested artifact from the supplied evidence. Use **MKL workflow** mode when the user requests its cross-artifact handoff or formal gate.
- Treat generate, review, refactor, and validate as operations within either mode. Preserve existing scope and authorization; do not ask again for an already authorized correction.
- Review/refactor/validate requires the target artifact. Generation requires a stated goal and enough behavior to model it; record assumptions and ask only for information that changes the result.
- Report verification coverage as **checked**, **partial**, or **blocked**, with the checks run and missing evidence. Missing upstream artifacts limit cross-artifact checks; they do not block useful standalone work. A partial check cannot establish formal acceptance.
- Preserve supplied identifiers and their mappings across renaming, reordering, splitting, and regeneration. Allocate new identifiers above the existing high-water mark; retain retired identifiers and never reuse them. If the registry is unavailable, mark new IDs provisional. Diagram aliases are separate from traceability IDs.
- Distinguish UML semantics, local MKL conventions, and heuristic findings. Run a scoped verification pass and recheck affected parts after corrections. Do not require a fixed number of clean passes or issue an assurance certificate from a validator result.

## Scope and inputs

Default to a scoped preparation review of the supplied material. Conduct a formal MKL PDR when requested; do not silently turn a small consistency check into a release gate.

| Evidence | Enables | If missing |
|---|---|---|
| Robustness diagram | BCE/profile and responsibility review | Block the diagram review; other supplied-artifact checks may proceed |
| CU specification | Basic/alternate/exception correspondence | Mark behavior coverage unverified |
| Domain model | Domain-entity and attribute closure | Mark closure unverified |
| Actor/use case view, requirements, interface contracts | Scope and source traceability | Declare the affected checks partial |
| Architecture, review participants, prior record | Applicable formal review layers | Record missing evidence or agreed non-applicability |

## Review workflow

1. Fix the artifact versions and review scope. Preserve PDR/H/CU/DR IDs and distinguish requirements, source evidence, assumptions, and local MKL criteria.
2. Check BCE notation, entity closure, flow correspondence, data flow, alternate behavior, and absence of premature implementation detail. Boundary interfaces can be human or machine interfaces.
3. Use the validator for mechanical preparation and inspect semantic correspondence manually. A noun match or actor/system alternation heuristic does not establish completeness.
4. Report actionable findings with source location, impact, severity, proposed correction and owning artifact. For a formal session, record disposition, owner, due date and verification evidence for agreed actions; do not invent participants or acceptance.
5. Recommend correction, deferral, upstream revision or dismissal only when relevant. A fixed menu and a compulsory pause are local facilitation choices, not universal requirements of IEEE/ISO standards.
6. Apply corrections when the user has authorized remediation; keep the review evidence and correction record distinct. Reuse existing authorization and verify the affected scope afterward.
7. For a handoff to detailed design, end the existing review record with the reviewed scope/baseline, findings and closure evidence, remaining constraints, and technical transition recommendation. Keep formal acceptance separate. Use the compact handoff in [review-protocol.md](references/review-protocol.md) so another chat can continue from the actual reviewed state.

## Coverage and disposition

Coverage (`checked` / `partial` / `blocked`) is separate from the proposed gate disposition:

- **Accepted:** all applicable formal checks have evidence, no unresolved critical/major findings, and the designated decision maker accepts the result.
- **Accepted with rework verification:** remaining findings have agreed remediation and verification conditions.
- **Reinspection required:** material unresolved defects prevent the transition.

With missing applicable evidence, withhold final acceptance and label the record **Not fully verified**. If the review target is absent, label it **Not reviewed — entry criteria not met**. A validator pass alone cannot authorize detailed design.

## Mechanical preparation

From this skill directory, the following is executable; paths are placeholders:

```bash
python scripts/validate_pdr.py --robustez path/to/robustness.puml --spec path/to/spec.md --dominio path/to/domain.puml
```

Use only available inputs accepted by `--help`. State execution, findings and omitted layers. Return a concise review for scoped work; a formal gate adds coverage, traceability, decisions and action tracking. No fixed self-audit count or assurance certificate is required.

## Focused references

- For a formal PDR or a handoff to detailed design, read [pdr-guidelines.md](references/pdr-guidelines.md) and [review-protocol.md](references/review-protocol.md).
- For cross-artifact evidence, read [cross-artifact-checks.md](references/cross-artifact-checks.md).
- For metrics or a specific smell, consult [pdr-metrics.md](references/pdr-metrics.md) or [anti-patterns.md](references/anti-patterns.md).
- For source limits and worked examples, consult [sources-and-methods.md](references/sources-and-methods.md) or [regression-examples.md](references/regression-examples.md).
