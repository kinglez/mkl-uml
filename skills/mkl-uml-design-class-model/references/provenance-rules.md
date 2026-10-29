<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Provenance of design-model elements

A significant element needs a supported reason to exist. Use scenario behavior, domain knowledge and explicit technical decisions as different evidence sources. When evidence is absent, report the gap and investigate the originating artifact; do not manufacture business behavior to justify a technical field.

This independently worded guidance adapts Rosenberg & Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice* (2007), chapter 8, together with the detailed-design context in Rosenberg, Stephens & Collins-Cope (2005). Historical extraction locators include 4363–4365 and 4284–4286; they identify upstream research rather than a publicly bundled source.

## Provenance table

| Element | Accepted origin | What to record |
|---|---|---|
| Operation | A classified Operation call, interface/framework contract, architecture constraint or justified design delta. | Origin ID, actual receiving classifier and required responsibility. |
| Problem-space class | Domain evidence and a reconciled domain model/discovery delta. | Stable concept name and any declared alias/change. |
| Solution-space class | Required architecture, infrastructure, framework or collaboration decision. | `<<solution>>`, purpose and the actual decision/contract source; the stereotype alone is insufficient. |
| Relationship | Domain relationship or a justified collaboration/navigation/ownership decision. | Origin, direction/role and evidenced multiplicities where modeled. |
| Business attribute | Domain evidence, scenario data, prototype or interface contract. | Concept/data origin and why that class holds it. |
| Technical/internal attribute | Architecture/design decision, configuration, framework/interface contract or required behavior. | Decision/source ID, purpose and constraint; literal mention in business use case text is unnecessary. |
| Constraint | Business rule, interface/framework contract, quality requirement or explicit design decision. | Applicable rule/decision ID and its scope. |

For example, `Order.version` may trace to an optimistic-concurrency design decision, and `RetryPolicy.maximumAttempts` to an integration/configuration contract. Preserve that rationale in the provenance matrix; adding those technical names to business use case steps would obscure their actual origin.

## Resolve gaps at their source

| Situation | Investigation |
|---|---|
| Operation lacks a selected call | Check other in-scope scenarios, contracts and documented deltas before concluding it is unused. |
| Attribute has no literal business-text match | Inspect domain, interface, architecture and configuration evidence. Route only a genuinely missing business concept/step to the specification. |
| Class is absent from the domain | Determine whether it is a supported solution class, late domain discovery or undeclared synonym. |
| Entity discovery was never reconciled | Record the domain delta and affected robustness/PDR links. |
| Relationship has no justified purpose | Establish actual ownership, navigation or domain meaning; correct it only with supported evidence. |

A provenance report names the element, available rationale, missing evidence and affected artifact. Apply supported corrections within the user's authorization. A declaration without substantive rationale cannot resolve a provenance gap.

## Vocabulary and scope

Preserve domain names or document intentional changes with aliases and affected links. Lexical similarity can suggest drift but cannot establish that `Order` and `Purchase` are the same concept. Solution classes may be newly introduced during detailed design; new problem-domain concepts still need domain reconciliation.

## Message semantics

Follow [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF), §17.4.3 and §17.12.18, when deriving operations:

| Message sort | Provenance consequence |
|---|---|
| `synchCall` / `asynchCall` with an Operation signature | Allocate/check the invoked Operation on the receiving classifier; inputs map to `in`/`inout` parameters. |
| `reply` | Trace outputs of the original synchronous call back to its caller; no reverse operation is implied. |
| `asynchSignal` with a Signal signature | Trace the Signal and applicable reception/handling contract. |
| `createMessage` / `deleteMessage` | Trace instance lifecycle behavior. |
| Ambiguous sort/signature/receiver | Record an unresolved allocation rather than guessing an operation. |

A self-call follows the same rule. Labels naming returned information are not callable operations. `MessageKind` concerns known message ends and differs from `MessageSort`. An unresolved receiver remains unresolved.

This skill's provenance requirement concerns significant operations within the selected behavioral scope; UML does not require every classifier operation to appear in one selected interaction. Matching words locates candidates and cannot establish semantic equivalence.
