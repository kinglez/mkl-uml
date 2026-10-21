<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# UML Use Case Diagram Rubric

Use this rubric to review or refine UML use case diagrams generated from a verbal model and optional PlantUML Domain Model.

## Core principle

- Verbal model decides functionality.
- Domain Model controls **domain-concept** terminology. Actor-role names come from external participation evidence; boundary/interface names come from interaction/interface evidence. Neither category must be forced into the domain model.
- Use case diagram shows external actor goals and externally observable system services.
- Do not convert domain classes into actors or use cases mechanically.
- Do not convert workflow steps, validations, calculations, state updates, or persistence effects into use cases mechanically.

## Standards-informed quality gate

A valid use case must:

1. represent an externally observable actor goal or system service;
2. be traceable to the verbal model;
3. use domain model terminology when it preserves meaning;
4. stay inside the system boundary;
5. avoid implementation, UI, persistence, algorithmic, and architectural details;
6. avoid internal validations, calculations, generated identifiers, and state updates unless they involve an external actor/service and are meaningful at the system boundary;
7. be named with an infinitive verb plus a domain complement;
8. be suitable for later textual specification and acceptance testing.

Reject or relocate a candidate if it is better represented as:

- precondition;
- postcondition;
- business rule;
- validation step;
- workflow step;
- activity diagram element;
- sequence diagram interaction;
- domain model concept;
- architecture component;
- UI or database detail.

## Actor checklist

Valid actors:

- external human roles;
- external organizational roles;
- external systems;
- external devices or sensors;
- external black-box services;
- external roles participating in the use case by exchanging data/signals, whether initiating or supporting it.

Invalid actors by default:

- database;
- screen/form/button/page;
- controller/repository/service module;
- internal component;
- passive entity with no interaction;
- class from the Domain Model without external-role evidence;
- the system itself.

## Actor association checklist

Associate an external actor when it **participates by exchanging data or signals with the subject during the use case**. This includes initiating actors and supporting actors such as payment gateways, notification providers, identity systems, and devices. An association does not assert initiation, sequence, or control direction. Mere benefit or mention without interaction is insufficient. See [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) §18.1.3–18.1.4.

Warning signs:

- the primary actor is connected to almost every use case;
- actor links point to calculations, validations, notifications, postconditions, or persistence effects;
- a subfunction is both included by the dominant use case and directly associated with the same actor without independent-goal evidence.

## Dominant use case checklist

If the prompt says `Use case: X`, or narrates one end-to-end process:

- treat X as the dominant use case;
- connect the primary actor mainly to X;
- include only important, externally meaningful subgoals;
- move validation, calculation, persistence, identifiers, and state updates to textual specification;
- avoid turning the scenario into a dense process map.

## Academic enrichment checklist

Use this when the user says the diagram is too simple, asks for scientific/methodological validation, or needs a stronger academic artifact.

A richer version is acceptable when:

- each added use case is traceable to the verbal model;
- supporting use cases remain externally observable or actor-visible;
- business rules are grouped into aggregated services instead of many low-level validations;
- packages group business concerns rather than technical layers;
- external service actors are justified by payment, notification, identity, registry, device, or integration evidence;
- postconditions such as generated identifiers, availability updates, and persistence remain outside the use case diagram.

For a single dominant scenario, about 6-10 use cases can be acceptable if the model is rich enough. A compact diagram is not wrong merely because it has fewer use cases; it may be under-expressive for classroom deliverables.

## Include rules

Use `<<include>>` only when all are true:

- the included behavior is mandatory;
- it is meaningful or testable as a separate subgoal/service;
- extraction improves clarity;
- it is not being used merely for sequence;
- it is not an internal validation, calculation, state update, persistence effect, or UI step.

## Extend rules

Use `<<extend>>` only when all are true:

- the behavior is optional, conditional, exceptional, or role-dependent;
- the base case can complete without it;
- the extension is externally observable;
- it improves clarity;
- it is not a minor internal validation failure.

## Access/authentication rule

Do not model `Access system` simply because the narrative says a user accesses the system. Model access/authentication only when the requirements mention authentication, credentials, identity verification, registration, role-based access, or session handling. Otherwise, treat access as a precondition.

## System-output rule

For confirmations, receipts, certificates, alerts, and notifications:

- direct actor association when the actor participates in exchanging the output/data/signals, including a supporting delivery service; this does not make the actor the initiator;
- `<<include>>` only when automatic, mandatory, externally meaningful, and clarity improves;
- `<<extend>>` only when conditional/exceptional and externally observable;
- otherwise, represent as postcondition in textual specification.

## Traceability questions

1. Which phrase in the verbal model supports each actor?
2. Which phrase supports each use case?
3. Is the candidate an external goal, external system service, or internal step?
4. Does the Domain Model term improve the name without adding functionality?
5. Are include/extend relations justified by semantics, not sequence?
6. Would the diagram help write later textual use case specifications?
7. Are excluded candidates better placed in another artifact?

## Visual quality

Prefer:

- simple associations over dense dependency webs;
- packages only for clear functional groups;
- actor generalization only when it reduces duplication;
- readable left-to-right layout;
- short use case names;
- controlled number of relationships.

Do not optimize visual simplicity by deleting required actor goals.

## The diagram is a summary; the text carries the weight

Recognized practitioner guidance (Fowler; Rosenberg & Stephens; Wiegers — see `standards-alignment.md`) converges: the use case *diagram* is a lightweight table of contents of actor goals, and the real analysis lives in the textual use case specifications. Review accordingly — reward a clean summary of goals; treat a diagram that tries to encode flow, sequence, or many relationships as a smell, not as richness.

## Goal levels (granularity compass)

Aim use cases at the **user-goal ("sea") level**. Flag candidates that are subfunctions ("fish": validate, compute, save, update a record) as steps/postconditions or `<<include>>` candidates, and candidates that are whole business processes ("kite": manage operations) as context, not a single use case. Keep the diagram at sea level; record a use case's level in its text if useful, not in the diagram.

## Include/extend restraint

Default to **none**. Practitioner guidance is emphatic that overusing `<<include>>`/`<<extend>>` (and use case generalization) is a leading cause of analysis paralysis and adds little real value. Accept one only when its gate is fully met and it clearly improves clarity — the classic legitimate case being a subgoal genuinely shared by two or more base use cases.

## Worked exemplar (what a clean use case diagram looks like)

A canonical example — a trading system — shows the target shape: a system boundary rectangle with a handful of use cases inside (`Set Limits`, `Analyze Risk`, `Price Deal`, `Capture Deal`, `Value Deal`, `Update Accounts`); four actors **outside** the boundary, including an external *system* actor (`Accounting System`) alongside human roles (`Trader`, `Trading Manager`, `Salesperson`); simple actor–use-case associations as the backbone; and only two `<<include>>` relations, both pointing to a genuinely shared subgoal (`Value Deal`).

The lessons: actors (human *and* external systems) sit outside the boundary; actor goals sit inside; associations are the backbone; and include/extend stay scarce and are used only for real, shared subgoals — never to encode sequence or internal steps.
