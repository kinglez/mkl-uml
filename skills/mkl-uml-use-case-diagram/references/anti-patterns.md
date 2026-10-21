<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# UML Use Case Diagram Anti-Patterns

Use this file for review, refactoring, and validation.

## Semantic anti-patterns

1. **Workflow diagram disguised as use case diagram**
   - Symptom: many use cases are ordered steps of one process.
   - Fix: keep the dominant use case and move detailed flow to textual specification or activity diagram.
   - Academic exception: a richer diagram may include grouped, externally observable subgoals if they improve traceability; avoid low-level temporal steps.

2. **Internal validation as use case**
   - Symptom: use cases named `Validate rule`, `Validate availability`, `Validate rate`.
   - Fix: keep as business rules or steps unless an external service/actor interaction is involved.
   - Acceptable alternative: use one aggregated service such as `Evaluate conditions`, `Evaluate eligibility`, `Evaluate compliance` or another domain-specific aggregate when the grouped result is visible/testable and avoids exposing each internal rule.

3. **Calculation as use case**
   - Symptom: `Calculate total`, `Calculate risk`, `Calculate average` without actor goal evidence.
   - Fix: model only if actor explicitly requests the calculation as a service; otherwise put in main flow.

4. **Persistence as use case**
   - Symptom: `Save`, `Record internally`, `Update database`, `Persist entity`.
   - Fix: model as postcondition or design detail.

5. **Actor connected to every substep**
   - Symptom: primary actor has many direct links to subfunctions already included by a main use case.
   - Fix: retain associations justified by actual external participation; remove mechanical links to internal substeps. Supporting actors may associate without initiating an independent goal.

6. **Include used as temporal sequence**
   - Symptom: includes read like `do A, then B, then C`.
   - Fix: move sequence to textual flow, activity, or sequence diagram.

7. **Extend used for every error**
   - Symptom: each validation failure is an extending use case.
   - Fix: keep minor failures in alternate flows/exceptions.

8. **Domain model copied into use cases**
   - Symptom: every class becomes a use case or actor.
   - Fix: use Domain Model only as vocabulary.

9. **Access/login without authentication requirement**
   - Symptom: `Access system` appears only because the story starts with “the user accesses”.
   - Fix: treat as precondition unless authentication/session behavior is explicit.

10. **Automatic output treated as actor-initiated**
    - Symptom: an automatic output is claimed to be actor-initiated merely because the actor receives it, or every output is mechanically promoted to a use case.
    - Fix: choose a postcondition, included behavior, extension, or justified system service according to the scenario. Keep an association for an external actor actually exchanging data/signals, including a supporting delivery provider; association alone does not claim initiation.

## Notation anti-patterns

- actors inside the system boundary;
- use cases outside the system boundary;
- classes, attributes, methods, multiplicities, components, databases, or UI elements in a use case diagram;
- missing system rectangle;
- aliases with accents/spaces/special characters;
- excessive packages that increase crossings.

## Review actions

Classify findings as:

- Critical: invalid UML or boundary violation;
- Major: actor goal vs internal step confusion;
- Moderate: excessive include/extend or visual density;
- Minor: naming/layout problem;
- Suggestion: optional refinement.

## Practitioner-grounded anti-patterns

11. **Relationship soup (include/extend/generalization overuse)**
    - Symptom: many `<<include>>`/`<<extend>>` and use case generalizations; the diagram reads like a functional decomposition tree.
    - Fix: default to none; keep simple actor–use-case associations. Practitioner guidance calls this a leading cause of analysis paralysis — the content belongs in the use case text, not in relationships.

12. **Too many use cases**
    - Symptom: a single scenario explodes into 15+ use cases, many of them steps of one goal.
    - Fix: collapse steps into their parent goal; keep use cases at user-goal (sea) level. (Wiegers lists "too many use cases" and flows over ~10–15 steps as traps.)

13. **Subfunction ("fish level") as use case**
    - Symptom: use cases like `Check field`, `Calculate subtotal`, `Update record`.
    - Fix: these are steps/postconditions inside a goal, not use cases; move them to the textual flow or, rarely, a justified `<<include>>`.

14. **Use case generalization for minor variants**
    - Symptom: a general use case with specialized children for small differences.
    - Fix: prefer separate use cases or textual alternate flows; use case generalization is rarely worth its cost.

## Sources

These anti-patterns are grounded in Fowler (*UML Distilled*), Rosenberg & Stephens (*Use Case Driven Object Modeling*), Rosenberg, Stephens & Collins-Cope (*Agile Development [abbreviated title]*), Wiegers & Beatty (*Software Requirements*), and Cockburn's goal levels — see `standards-alignment.md`.
