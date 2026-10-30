---
name: mkl-cdr-review
description: Review UML detailed-design consistency and scoped SOLID evidence across classes, interactions and tests. Use for CDR preparation or formal MKL handoff; report coverage, findings and disposition.
license: Apache-2.0
metadata:
  author: kingle.zhuang
  email: kinglezhuang@vip.qq.com
  copyright: 2026 kingle.zhuang
  organization: mkl
---
# MKL CDR Review

## Operating contract

- Use **standalone** mode by default: complete the requested artifact from the supplied evidence. Use **MKL workflow** mode when the user requests its cross-artifact handoff or formal gate.
- Treat generate, review, refactor, and validate as operations within either mode. Preserve existing scope and authorization; do not ask again for an already authorized correction.
- Review/refactor/validate requires the target artifact. Generation requires a stated goal and enough behavior to model it; record assumptions and ask only for information that changes the result.
- Report verification coverage as **checked**, **partial**, or **blocked**, with the checks run and missing evidence. Missing upstream artifacts limit cross-artifact checks; they do not block useful standalone work. A partial check cannot establish formal acceptance.
- Preserve supplied identifiers and their mappings across renaming, reordering, splitting, and regeneration. Allocate new identifiers above the existing high-water mark; retain retired identifiers and never reuse them. If the registry is unavailable, mark new IDs provisional. Diagram aliases are separate from traceability IDs.
- Distinguish UML semantics, local MKL conventions, and heuristic findings. Run a scoped verification pass and recheck affected parts after corrections. Do not require a fixed number of clean passes or issue an assurance certificate from a validator result.

## Scope and inputs

Default to a scoped preparation review of the supplied material. Conduct a formal MKL CDR when requested. A scoped review does not require an entire pipeline; it must name the checks its evidence supports.

| Evidence | Enables | If missing |
|---|---|---|
| Design class model | Signatures, cohesion and static design | Block class review |
| Sequence diagrams | Interactions, operation allocation and continuity | Block interaction review and the full gate |
| CU specifications | Text/flow correspondence | Mark behavior coverage unverified |
| Domain, robustness, requirements, test plan | Provenance and downstream coverage | Declare affected checks partial |
| Developer assessment and header inspection when applicable | Feasibility and human review | No unqualified formal acceptance |

## Review workflow

1. Fix scope and artifact versions; preserve CDR/H/RF/CU/DR/DS/MC/CP IDs. Review claims against traceable evidence, not diagram polish or expected finding density.
2. Examine flow correspondence, alternate behavior, receiver responsibilities, cohesive state, explicit solution classes, complete signatures, requirements and tests.
3. Match ordinary operations to operation calls or documented contracts/requirements. Treat replies, signals, creation and destruction according to their message sorts; respect inheritance and aliases.
4. Run the available mechanical checks, then assess non-automatable questions such as feasibility and semantic adequacy. Do not manufacture participation or infer human inspection from generated headers.
5. Present located findings and proportionate recommendations. Fixed four-way menus, deliberation pauses, and quantitative review budgets are optional MKL facilitation choices; do not attribute them as mandatory IEEE/ISO procedures.
6. Generate code headers only when that action is authorized. Existing explicit authorization is sufficient; do not re-ask. Header generation and header inspection are different evidence.
7. If remediation is authorized, apply and verify it while recording what changed. For formal independent rework verification, identify the actual independent reviewer; do not call repeated self-checks independent review.

When SOLID is requested or a material design claim concerns extension, substitution, client contracts or dependency ownership, apply the [scoped SOLID evidence review](references/solid-evidence.md). Record evidence, checks actually performed, coverage, supported conclusions or findings, and missing layers separately from formal acceptance.

## Coverage and disposition

Coverage (`checked` / `partial` / `blocked`) is separate from the proposed formal disposition:

- **Accepted:** all applicable checks have evidence, no unresolved critical/major findings, and the designated decision maker accepts the transition.
- **Accepted with rework verification:** remaining findings have agreed correction and verification conditions.
- **Reinspection required:** material unresolved defects prevent implementation handoff.

Use **Not fully verified** when evidence is missing, and **Not reviewed — entry criteria not met** when required review targets are absent. Non-applicability requires a reason tied to scope; it must not conceal a missing check. A script's provisional acceptance is never the final gate decision.

## Mechanical preparation

From this skill directory, this command is executable; paths are placeholders:

```bash
python scripts/validate_cdr.py --clases path/to/classes.puml --secuencia path/to/sequence.puml
```

Add existing `--spec`, `--dominio`, `--robustez`, `--requisitos` and `--pruebas` inputs only when relevant; inspect `--help` for supported cardinalities. Missing optional CLI files can still be mandatory evidence for the requested formal scope. Declare omitted layers and human checks.

Return a concise scoped review, or a formal record with coverage, located findings, traceability, decisions, disposition and action ownership. No fixed self-audit count or assurance certificate is required.

## Focused references

- For a formal CDR, read [cdr-rules.md](references/cdr-rules.md) and [review-protocol.md](references/review-protocol.md).
- For a decision workshop, read [deliberation-protocol.md](references/deliberation-protocol.md); for a requested session plan, read [session-budget.md](references/session-budget.md).
- For header work and traceability, read [traceability-and-headers.md](references/traceability-and-headers.md).
- For metrics, smells, figure interpretation or examples, consult [metrics-and-triage.md](references/metrics-and-triage.md), [anti-patterns.md](references/anti-patterns.md), [figure-notes.md](references/figure-notes.md), or [regression-examples.md](references/regression-examples.md) as needed.
- For attribution limits, consult [sources-and-methods.md](references/sources-and-methods.md).
