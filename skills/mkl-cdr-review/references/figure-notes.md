<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Lessons from historical source figures

The upstream research inspected book/course figures that are not distributed here. Those historical observations are evidence about the method's teaching examples, not new visual verification or permission to reproduce the figures. This revision retains concise original review lessons rather than transcribing diagram Notes or reconstructing source artwork.

Rosenberg & Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice* (2007), chapter 9, informs these lessons:

- A wrapper that merely repeats another object's state/accessors merits a purpose check. Framework or boundary contracts may still justify it.
- A refactored example can improve one responsibility while retaining unrelated visibility, state or operation problems. Verify each finding independently.
- Read static and dynamic views together and trace required outcomes to test design.
- An alternative is designed when actual guarded behavior realizes it, not when a Note merely names it.
- Inspect suspicious class responsibilities to find the interaction that allocated them; confirm actual call direction before changing either model.

Historical extraction filenames sometimes used nearby text instead of the correct figure caption. They are unreliable bibliographic figure numbers. Verify an original figure before citing its exact number or content.

RITME charts in van Solingen & Berghout, *The Goal Question Metric Method*, Case B, supplied historical context about review size, pace and varying defect yield. They are not measurements of this tool or universal defect-density expectations. See [session-budget.md](session-budget.md).

The fixture set demonstrates the specific contracts described in [regression-examples.md](regression-examples.md); it does not reproduce every source figure or prove the sources' designs correct. Source provenance and remaining uncertainty are in [sources-and-methods.md](sources-and-methods.md) and the repository's third-party inventory.
