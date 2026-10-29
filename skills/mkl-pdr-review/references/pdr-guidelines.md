<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Preliminary-design review checks

This independently worded checklist adapts the PDR method in Rosenberg & Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice* (2007), chapters 6–7. The historical countdown numbers are retained for cross-reference; wording from the book and private course materials is not reproduced.

Use applicable checks for standalone work. Apply the full checklist and formal participation requirements only for a requested formal package review. Supporting evidence outside the selected scope remains a disclosed limit.

| Guideline | Review action | Sufficient evidence and limits |
|---|---|---|
| **10 — Text and diagram correspond** | Trace each scenario step to robustness elements/links, then inspect each element for a scenario origin. | A reviewer confirms semantic correspondence; lexical overlap merely locates candidates. |
| **9 — Domain concepts are reconciled** | Compare robustness Entities with the domain model and declared discovery delta. | Every problem-space Entity is accounted for. Actors and human/machine boundaries trace to separate participation/interface evidence. |
| **8 — Data has a path** | Follow user/interface inputs through behavior to responsible domain concepts and follow required output back to the boundary. | Identify where each significant input is used and output obtained. A graph connection alone does not prove a correct transformation. |
| **7 — Alternatives have behavior** | For each local `(CU-ID, FA/FE-ID)`, inspect the trigger, condition, actions and continuation/termination in text and diagram. | A condition or label without actual handling is incomplete. Coverage cannot be borrowed from another use case. |
| **6 — Both sides of the interaction are specified** | Check actor stimuli and observable system responses. | Include successful and rejected outcomes. Avoid a list of actor actions that never defines what the system does. |
| **5 — Robustness profile is followed** | Check the Boundary/Control/Entity connection matrix and recognizable participants. | Apply the owning robustness skill's rules. These are method/profile constraints rather than UML-wide prohibitions. |
| **4 — Shared understanding is demonstrated** | Include relevant technical and product/customer perspectives in a formal review. | Record actual participants and interpretation issues. An automated check cannot supply missing stakeholder evidence. |
| **3 — Names have context** | Resolve domain nouns, actor roles and interface names to their appropriate sources. | Prefer specific interfaces and stable vocabulary. Architecture context can constrain the scenario without importing implementation details into business steps. |
| **2 — Preliminary scope is preserved** | Keep behavior logical; leave method allocation, framework mechanics and detailed object collaboration to detailed design. | Pattern-like names are investigation clues, not defects without context. |
| **1 — Per-diagram synthesis** | Reconcile text, profile connections, logical behavior, alternatives and abstraction level for every selected diagram. | Record missing and contradictory evidence rather than repairing the report through terminology alone. |

## Practical sweep

For each robustness diagram, read its specification beside it, check allowed connections, follow every logical behavior and alternative, and reconcile newly discovered domain concepts. Record each observation once under the relevant guideline. A second presentation pass does not create an independent review or a correctness guarantee.

## Process boundary

PDR prepares selected preliminary designs for detailed behavior allocation. A new business requirement returns to the affected requirements/domain artifacts and their links; it need not restart unrelated use cases. Where a formal review needs shared technical and business understanding, record it explicitly. A clean script result is preparation evidence, not proof that people agreed or that the full package is accepted.

The book's chapter/page references and inherited research status are recorded in [sources-and-methods.md](sources-and-methods.md). Corpus line numbers in historical records locate a private extraction; they are not publicly reproducible bibliographic locators. No universal PDR duration was established from this source.
