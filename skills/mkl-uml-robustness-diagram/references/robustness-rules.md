<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Robustness diagram rules

Detailed rules applied by the skill and mechanically checked by `scripts/validate_robustness_puml.py`. Primary source: Rosenberg and Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice* (Apress, 2007), chapters 5–6; supplemented by Rosenberg, Stephens, and Collins-Cope, *Agile Development [abbreviated title]* (Apress, 2005). The formulations below are operational paraphrases unless explicitly identified as quotations.

## Terminology

Use **boundary**, **entity**, and **control** objects, following the Jacobson terminology in the English sources. Recognize the course's Spanish equivalents *Borde*, *Entidad*, *Controlador*, *frontera*, and *pantalla* when interpreting inputs. Write deliverables in the user's requested language, English by default in this edition.

PlantUML keywords (`boundary`, `control`, `entity`) and alias prefixes (`B_`, `C_`, `E_`) remain stable as syntax and validation contracts.

## The principle behind the rules

Boundaries and entities are **nouns**; controls are **verbs**. Nouns communicate with verbs, verbs communicate with nouns or other verbs, and nouns do not communicate directly with other nouns.

Within this MKL robustness notation, a noun-to-noun edge is a candidate **missing control**, hence potentially unaccounted behavior. It is a method constraint, not a UML-wide prohibition on object communication; check the actual text before asserting a missing function. Discover and name that function; deleting the edge alone leaves the gap unresolved.

## Permitted relationships

1. Actor ↔ boundary object.
2. Boundary ↔ control: noun ↔ verb.
3. Control ↔ control: verb ↔ verb.
4. Control ↔ entity: verb ↔ noun.

## Prohibited relationships

5. Actor ↔ control or entity: communicate through a boundary.
6. Boundary ↔ entity: insert a control.
7. Entity ↔ entity: insert a control.
8. Boundary ↔ boundary: insert a control.
9. **Actor ↔ actor:** the course material's **4×4 YES/NO matrix**, covering actor, boundary noun, entity noun, and control verb, explicitly disallows actor-to-actor communication. A robustness diagram describes interaction with the system. The validator treats this fifth prohibition as an error.

PDR guidance reinforces that actors connect **only** to boundaries and that noun-to-noun communication requires an intervening control. Missing controls are particularly serious because **controls represent system behavior**.

## Alternative-course color convention

The course recommends coloring objects involved exclusively in alternatives to make flows visually distinguishable. Worked examples show error-message controls in red.

- Color objects **exclusive** to alternative or exception courses: `control "Show 'Blank fields' message" as C_BlankFields #LightCoral`.
- Leave objects shared with the basic course uncolored, including the screen to which an alternative returns.
- Label relevant relationships with the flow ID (`FA-01`, `FE-02`) so the script can check coverage.

The source treats coloring as good practice; the validator reports a **warning**, not an error, when absent.

## Two valid user-action conventions

The course accepts both:

1. An action originates **at a boundary**, connecting one screen to another through a control. Example: “Click Create Course” from Main Page to Show Course Creation Window.
2. An action originates **at the actor**, directed toward the boundary.

Choose a consistent convention within each diagram.

The sources illustrate valid and invalid relationships with different figure numbering across works and editions. Do not transfer figure numbers between editions without checking the image.

## Style and granularity

The upstream review records the following as checked against the source:

| Rule | Operational formulation |
|---|---|
| **Actual interface names** | Resolve a generic boundary to its actual screen/page or machine interface name |
| **Page names are nouns** | Avoid expressions mixing action and object, such as “view book details page” |
| **Interface-level boundaries** | For a GUI use whole screens/pages rather than widgets; for machine interaction use named APIs, webhooks, message ingress, or device adapters |
| **Conceptual terminology** | Use domain names for entities, interface-origin names for boundaries, and external-role names for actors; avoid premature implementation detail |
| **Boundary-to-control labels** | Label this edge to avoid ambiguity when multiple actions enter one boundary |
| **Whole use case in one diagram** | Include the basic course and every alternative |
| **Behavioral controls** | Include a control only when it represents behavior |
| **Direction is immaterial** | Edges are communication associations, not temporal ordering |
| **Invoked use cases** | A use case invoked by the parent may be brought into the diagram |
| **Approximate ten-minute budget** | Longer work often reflects needed use case text revisions; account for that explicitly |
| **Split oversized use cases** | Split when the diagram becomes too large or alternatives gain subordinate alternatives |

## Fixed, checkable notation convention

The source states that arrow direction adds no semantics to robustness communication associations; sequence diagrams convey time order. To give an operational convention, this skill uses **undirected `--` connections**.

The validator warns about directed arrows for **notational consistency**, rather than treating `-->` as a methodological error. Mixed notation encourages readers to infer temporal order that the artifact does not establish.

## Controls: a common source of errors

- Controls are usually **logical software functions**, only occasionally actual control objects. Treat them as function placeholders rather than classes.
- **Overuse leads back to functional decomposition** if every function becomes a controller class.
- A legitimate later design outcome is a **cluster of interacting controls** becoming a manager class, particularly for nontrivial state behavior.
- Presentation controls such as “Show X” are useful when initialization is nontrivial. Give each a specific name rather than calling all of them “Show.”

## Correspondence with use case text

- Place text **beside the diagram** so readers can trace both views of the same behavior.
- Maintain **one-to-one correspondence** between textual steps and represented flow.
- Walk text **one sentence at a time**.
- Expect to **disambiguate and propose rewrites** during drawing; early drafts often contain vagueness, omissions, or errors. Finding them is part of the purpose.
- Maintain the chain: text agrees with robustness diagram, robustness agrees with class model, class model agrees with code.

## Object discovery

- Take entities from the domain model and report missing entities for incorporation.
- Assume the initial domain model is incomplete and use robustness analysis to complete it.
- Incrementally identify new classes and **attributes** while drawing. **Operations wait** for detailed design.
- Completion criterion: all entities in all robustness diagrams appear in the updated domain model or a disclosed pending delta.
- **Boundary/interface names have interface evidence as their origin; actor-role names have external participation evidence as their origin.** Neither is required in the domain model. A role may also be a conceptual domain class when the domain independently requires it (for example `Customer`); keep those two modeling roles distinct.

## Forward mapping

- Boundaries and entities generally become **object instances** in sequence diagrams; controls become **messages**.
- Controls later allocate behavior through calls, Signals, or lifecycle interactions as appropriate. Only Operation-signed calls imply receiving-class operations; replies map outputs of original calls.
- Use the diagram as a sequence-design checklist: walk controls, draw their messages, and mark them.
- Derive **one test case per control**.
- Behavior left implicit in both text and diagram risks being omitted from implementation.

## Scope of these rules

The connection matrix and entity/boundary/control roles are MKL analysis conventions. UML does not require these stereotypes or forbid the same connections in an ordinary interaction/class model. Domain closure applies only to `entity` domain concepts. Boundary names trace to human or machine interfaces and actor names to external roles; do not add APIs or external-service actors to the domain merely to satisfy a vocabulary comparison.
