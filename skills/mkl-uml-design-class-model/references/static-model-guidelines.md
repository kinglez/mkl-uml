<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Maintaining the static design model

Keep the conceptual domain model and the detailed design model separate. Detailed design adds justified technical classes, signatures, visibility and relationships without rewriting business meaning. This original guidance is informed by Rosenberg & Stephens (2007), chapters 8–9 and 11, and Rosenberg, Stephens & Collins-Cope (2005), model-refactoring and implementation discussions. See [sources-and-methods.md](sources-and-methods.md) for historical evidence limits.

## Synchronize while allocating behavior

When adding an Operation call, inspect its receiving class and update the significant operation signature and required state. Apply the message-sort rules in [provenance-rules.md](provenance-rules.md); replies, Signals and lifecycle messages have different consequences. Record contracts and design decisions that justify members beyond one interaction.

Review the resulting responsibility distribution. A potential superclass, a useful adapter or a class split needs a concrete purpose and preserves the selected behavior. Generalization and pattern names alone do not justify new structure.

## Prepare for CDR

Resolve the following where they affect the selected design:

- Required framework/infrastructure collaboration and its contracts.
- Operation parameters, directions, return values and attribute types.
- Evidence for important relationships, multiplicities and ownership.
- Requirement/design-decision provenance and scenario/test links.
- Unresolved assumptions that affect implementability.

Use layout to make these responsibilities readable; visual polish cannot close evidence gaps. A standalone model assessment may proceed with disclosed supporting limits. A formal package review requires applicable evidence before acceptance.

## Refactor the model deliberately

Compare alternative responsibility allocations before code makes them expensive to change. Preserve required behavior and traceability while moving operations, extracting collaborators or simplifying dependencies. Technical/internal state may originate in documented architecture and contracts; business use cases need not name implementation fields.

Check both directions between static and dynamic models. A suspiciously one-sided API is a prompt to inspect its scope and call origin, not a requirement to add an inverse operation. Confirm a demonstrated mismatch before changing the interaction or class.

## Downstream handoff

CDR checks scenario realization, operation allocation, class coherence, explicit collaboration, requirements, implementer assessment, signatures, headers and test design. The owning CDR reference defines those checks; this file does not duplicate its countdown wording.

Generate requested/authorized headers as inspection aids and compare their output with the modeled members and relationships. Report unsupported translation rather than silently dropping information. Once implementation exists, reconcile the maintained class model with actual code under the requested code-review/model-update scope. Do not assume that an old interaction remains current without examining affected behavior.
