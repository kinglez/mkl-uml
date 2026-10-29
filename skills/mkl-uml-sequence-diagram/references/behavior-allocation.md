<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Allocating behavior to collaborators

For each required behavior, determine what information and authority it needs, which object has that knowledge, and which collaborators should contribute. This original guidance is informed by Rosenberg & Stephens (2007), chapter 8; Fowler, *UML Distilled* (3rd ed.), chapter 4; and Wirfs-Brock's *A Brief Tour of RDD in 2004*. Historical source confidence is recorded in [sources-and-methods.md](sources-and-methods.md).

## Choose a responsibility

Start from the selected scenario and supplied robustness Controllers when available. Prefer keeping a state-dependent decision near the state and invariants it needs. Delegate a coherent subtask when one class would otherwise need unrelated data or know a collaborator's internals.

Inspect proposed attributes and operations together. Unrelated state groups or several independent reasons to change suggest a responsibility split, but confirm the design context before moving behavior. A stateless service, coordinator or framework adapter can be justified by its contract.

## Useful role vocabulary

| Role | Review question |
|---|---|
| Information holder | What state or facts does this object maintain? |
| Structurer | Which domain objects and relationships does it organize? |
| Service provider | Which coherent calculation or transformation does it offer? |
| Controller | Which decisions and progression rules does it own? |
| Coordinator | Which tasks does it delegate and in what order? |
| Interfacer | Which external interaction or technology detail does it encapsulate? |

The role names are attributed to Wirfs-Brock; the questions are local wording. Roles may combine. Identify the concrete responsibility rather than forcing every object into a single category.

GRASP terminology from Larman's *Applying UML and Patterns* is supplementary vocabulary known through secondary sources: Information Expert, Creator, Controller, Low Coupling, High Cohesion, Polymorphism, Pure Fabrication, Indirection and Protected Variations. Use it to explain a decision; it is not a substitute for the actual behavior and contract evidence.

## Inspect the resulting collaboration

- Determine whether a dominant participant is coordinating legitimate work or performing others' responsibilities.
- Check whether state-dependent behavior can be localized without violating transaction, framework or interface contracts.
- Explain a non-domain collaborator through architecture/design evidence and mark it accordingly.
- Prefer precise action names that reveal the intended responsibility.
- Record meaningful allocation rationale and affected class-model changes.

A fully centralized or data-only design is a review candidate, not automatically an error. Consider the chosen architectural style and actual requirements before calling it an anemic model.

## Limits of automated checks

Counts and lexical matching cannot establish the correct owner of business behavior. A message chain also needs semantic evidence: receiving a reference from one collaborator and then navigating it may reveal structural coupling, while ordinary delegation `A → B → C` may be exactly the intended design. The Law of Demeter source (Lieberherr & Holland, 1989) is inherited secondary context, not a proven graph-only rule.

Consecutive self-calls, high message concentration and apparently uncovered Controllers are candidates for inspection. Confirm the required behavior, receiver, message sort and scope before reporting a defect. No fixed proportion of Controllers needs to become software controller classes.
