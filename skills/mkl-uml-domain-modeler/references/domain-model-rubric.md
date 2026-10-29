<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Domain Model Rubric

Use this reference when reviewing or refining UML domain models for any project domain.

## Purpose

A domain model is a conceptual glossary. It captures important terms of the problem domain and the relationships between them. It should reduce ambiguity and support later use case diagrams and use case specifications.

The goal is not to make the smallest diagram, nor the largest. The goal is to produce a clean, stable, traceable vocabulary for the project — **minimal yet sufficient**.

## Modeling Philosophy (source-backed)

Three convergent principles set the tone for every review and every audit pass:

- **Minimal yet sufficient / low ceremony.** Produce just enough to remove ambiguity and proceed; a concept earns its place only if it adds clarity (Rosenberg, Stephens & Collins-Cope, 2005).
- **Timeboxed first pass.** A couple of hours of focused work typically surfaces ~80% of the domain classes; resist gold-plating and premature detail (Rosenberg & Stephens, 2007).
- **Living artifact.** The initial model is expected to be incomplete and is refined and updated throughout the project and across increments (Rosenberg & Stephens, 2007; Rosenberg et al., 2005).

## Source-Backed Quality Dimensions

Use these dimensions when the user asks for review, comparison, justification, or academic documentation:

| Dimension | Meaning for UML domain models | Typical finding |
|---|---|---|
| Syntactic quality | The model follows the chosen notation and the assignment constraints. | Missing required notation, using methods in conceptual classes, or using multiplicities when the rubric forbids them. |
| Semantic quality | The model represents the domain described by the verbal model without false, missing, or overloaded concepts. | Important domain terms are absent, process actions become classes, or a class has the wrong relationships. |
| Pragmatic quality | The intended audience can understand and use the model. | Too many crossings, ambiguous labels, inconsistent names, or overly dense packages. |
| Visual effectiveness | Symbols, labels, layout, and grouping reduce cognitive load and support accurate interpretation. | Long procedural labels, visually similar concepts with different meanings, unnecessary line crossings, or decorative packages. |
| Traceability | Terms remain consistent from verbal model to domain model and later use case specifications. | The diagram uses synonyms or removes a term needed in normal and alternative flows. |
| Analysis-model value | As a requirements analysis model, it augments (not replaces) the written spec and reveals missing, inconsistent, duplicated, or superfluous vocabulary. | The model adds no clarity over prose, or hides a duplicated/omitted term that multiple views would expose. |

Apply the dimensions as review criteria, not as rigid scoring unless the user requests a grade. When the user's academic prompt forbids attributes or multiplicities, treat that as the controlling syntactic constraint even if richer UML notation could be useful in professional class diagrams.

## Dynamic Domain Expertise

Before evaluating or generating a domain model, infer the problem domain and apply the most relevant senior domain-expert perspective with more than 30 years of experience. Use this domain perspective to judge which concepts are stable, which terms are ambiguous, which exceptions or events deserve first-class modeling, and which relationships are meaningful in that specific domain.

Do not overfit to examples. A concept that is only an alternative flow in one domain may be a tracked business record in another domain, such as finance, insurance, healthcare, safety, audit, security, or logistics.

Keep the detailed analysis private. When asked to explain decisions, provide a concise rationale, checklist, or review summary rather than step-by-step hidden reasoning.

## Core Rules

- Model problem-domain vocabulary, not software design (the conceptual perspective: a vocabulary to talk about the domain, with software kept out of the discussion).
- Use conceptual classes, plain associations, `has-a` (aggregation), and justified `is-a` (generalization). These three relationship kinds carry the large majority of a domain model.
- Validate every generalization with the substitution test: *every instance of the subtype is, by definition, an instance of the supertype*. Distrust a bare verbal "is-a" — the phrase is ambiguous.
- Treat aggregation (`o--`) as a light "has-a"; it has no precise, agreed UML semantics. Do not split hairs between aggregation and composition on a first pass. Reserve composition (`*--`) for evidenced composite ownership: at most one whole at a time, with deletion of object parts still attached when the whole is deleted. Parts may detach first where allowed; precise lifecycle details require model evidence ([OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) §9.5.3).
- Do not include operations, methods, algorithms, persistence details, infrastructure, or design-pattern machinery.
- Do not include multiplicities in initial academic domain models unless the assignment explicitly asks for cardinalities; a missing multiplicity means "deliberately deferred", not "1". In review mode, mark multiplicities as optional/forbidden according to the prompt, not as universally required.
- Prefer a clear first approximation over exhaustive coverage.
- Do not over-prune concepts that will be needed in later use case specifications.
- Use one term per concept; refine iteratively as project understanding improves.

## Candidate Classification

For each noun phrase from the verbal model, classify it before drawing:

| Candidate type | Keep as class? | Guidance |
|---|---:|---|
| Stable real-world thing | Usually | `Customer`, `Course`, `Reservation`, `Product`, `Patient` |
| Role in the domain | Often | Keep if it interacts with or classifies domain objects; it may later be a use case actor |
| Simple property | No | Convert to attribute only if attributes are allowed |
| UI element | No | `Screen`, `Form`, `Button`, `Interface` |
| Technical element | No | `Database`, `API`, `Controller`, `TechnicalService` |
| Design-pattern machinery | No | `Factory`, `Singleton`, `Strategy`, `Manager` — solution space, not problem space |
| Use case/action | No | `CreateUser`, `ReserveRoom`, `ValidatePayment` |
| Error/alternative flow | Sometimes | Keep only if it is a business record, incident, alert, state, or domain event with identity, lifecycle, traceability, or relationships |
| Policy/rule/restriction | Sometimes | Keep if it governs several concepts or has domain meaning |
| State or lifecycle category | Sometimes | Keep when approval, rejection, confirmation, cancellation, blocking, expiration, or pending correction is meaningful for traceability |
| Term needed for use case wording | Often | Keep if it avoids ambiguity in normal or alternative flows |

## Traceability to Use Cases

When the domain model will feed use cases:

- Preserve names that will be referenced in use case specifications.
- Reuse domain-class names for **domain concepts** in the use case text ("reference domain classes by name"). Actor-role and boundary/interface names have separate participation/interface origins and need not be domain classes.
- Keep actors or roles as conceptual classes when they belong to the domain vocabulary. Real domain models routinely include the actors (e.g., `Customer`, `Seller`) connected by association.
- Do not convert use cases into classes. Use cases are goals/behaviors; domain classes are nouns.
- Do not convert every class into a use case. Only actor goals become use cases.
- Alternative-flow concepts may remain outside the domain model unless the domain tracks them as records, incidents, alerts, states, or events.
- Use one consistent term for one concept across verbal model, domain model, use case diagram, and use case specifications ("Duplicate Name Police": pick one term and stick with it).

## The Four Most Common Domain-Modeling Mistakes (source-backed)

Rosenberg & Stephens (2007) present domain modeling by walking through the mistakes people make and correcting them. Check every model for these:

1. **Multiplicity too early.** Cardinalities on a first-pass conceptual model. Correction: remove them; defer multiplicity to later modeling.
2. **Mapping database tables to domain classes.** Classes copied from a relational schema, full of IDs/foreign keys, or with attributes placed on the wrong class (e.g., customer fields sitting on `Order`). Correction: establish each class from business meaning rather than copying database structure.
3. **Operations / abstract classes too early.** Assigning behavior or introducing abstract machinery is a design activity. Correction: keep the model structural and conceptual.
4. **Premature patternization.** Design-pattern machinery (e.g., a `SessionFactory`) appearing as domain classes. Correction: remove it — it is solution space, not problem space.

## Common Anti-Patterns

### Multiplicities too early

Problem: `Customer "1" -- "*" Reservation`.
Correction: `Customer -- Reservation : undertakes`.

### Operations in conceptual classes

Problem: `Reservation { confirm(); calculateTotal(); }`.
Correction: remove operations; those belong to design or behavior models.

### Data-model thinking

Problem: classes full of IDs, foreign keys, table-like joins, or technical fields; or attributes placed on the wrong class.
Correction: model business concepts and vocabulary; move each attribute to its owning concept, or omit attributes in strict mode.

### Premature patternization

Problem: `SessionFactory`, `ReservationBuilder`, `PaymentStrategy`, `UserManager` appearing as domain classes.
Correction: remove them; design patterns are solution-space and do not belong in a problem-domain model.

### Attribute misplacement

Problem: attributes of `Customer` placed in `Order`.
Correction: move each attribute to its owning concept, or omit attributes in strict mode.

### Flow-as-domain

Problem: classes named `RejectedPayment`, `InvalidData`, `SuccessfulValidation` for every scenario.
Correction: omit them, keep them in use case alternative flows, or consolidate into `Incident`, `Event`, `Alert`, `State`, or `Notification` only if the domain tracks them.

### Disconnected general concept

Problem: a general class and its specializations appear, but the inheritance relationship is missing, for example `Service`, `IncludedService`, and `AdditionalService` without generalization.
Correction: connect the specializations with `--|>` when the relation passes the substitution test, or remove the general class if it adds no conceptual value.

### Overworked aggregation / misused composition

Problem: composition (`*--`) used for relationships that are not lifecycle-dependent, or long debates over whether something is aggregation vs composition on a first pass.
Correction: prefer plain association or a declared application-specific `has-a`; use composition only when exclusive ownership at a time and deletion semantics are justified. A part may be detached before deletion where otherwise allowed.

### Procedural relationship labels

Problem: association labels read like system behavior, for example `generates`, `communicates`, `validates`, `calculates`, `updates`, `verifies`, `approves`, `rejects`, `prevents`, or `affects`.
Correction: rewrite them as stable domain relations, such as `has`, `owns`, `corresponds to`, `is documented by`, `is reported through`, `is supported by`, `occupies`, `applies to`, or `depends on`.

### Missing state concept when lifecycle matters

Problem: the verbal model discusses approval, rejection, confirmation, cancellation, expiration, blocking, or pending correction, but the domain model cannot name the lifecycle condition.
Correction: consider a conceptual state such as `ReservationState`, `PaymentState`, or `RequestState` only when it improves use-case traceability. Do not model every transition as a class.

### Technical classes

Problem: `System`, `Application`, `Database`, `PaymentService`, `ReservationController`.
Correction: remove them from the domain model.

### Artificial hub overload

Problem: one class is connected to nearly every other class because the modeler attached all details directly to it.
Correction: review the hub. Preserve it if it is truly central in the domain; otherwise introduce intermediate domain concepts or remove redundant relationships.

## Hub Review Rule

A hub-like class is not automatically wrong. It may be correct when it is a central business concept, such as `Reservation`, `Contract`, `Order`, `Patient`, `Case`, `Course`, `Account`, or `Project`. A domain model can legitimately have more than one hub (for example, an online bookstore centered on both `Order` and `Book`).

Refactor only when the hub:

- accumulates details that belong to another concept;
- duplicates relationships already expressed through intermediate classes;
- mixes behavior or workflow with structure;
- causes ambiguity rather than reducing it;
- exists only because of database or implementation thinking.

## Worked Exemplar (what a good first-pass domain model looks like)

A canonical teaching example — an online bookstore — illustrates the target shape of a first-pass model (Rosenberg & Stephens, 2007):

- Two legitimate hubs: `Order` and `Book`, each aggregating its related concepts (`Line Item`, `Shopping Cart`, `Credit Card`; `Author`, `Category`, `Review`, `Wish List`).
- `has-a` (aggregation) is the dominant relationship; generalization is used where it truly applies (e.g., `Purchase Order` and `Credit Card` are kinds of `Payment Type`, an abstract supertype).
- Actors are present as domain classes: `Customer` and `Seller`, connected by plain associations.
- No attributes and no multiplicities in the first pass.
- Some candidate nouns are deliberately left unconnected or later pruned — including technical ones (`Database`) that do not belong in the domain model at all.

The lesson: a good first pass is aggregation-heavy, allows more than one hub, includes actors, omits attributes/multiplicities, and is openly incomplete. It is then tightened over successive passes (see the Iterative Audit Loop).

## Optional Iterative Audit Loop Checklist

Default to one scoped check of the requested artifact and affected links; correct concrete findings and recheck what changed. Use the fuller loop below only for an explicitly requested formal MKL review or audit. Repeated clean passes do not prove completeness or correctness; stop when the requested scope is checked and residuals are disclosed.

- Refine → Audit → Correct → Check convergence.
- Audit against: the Review Checklist below, the four common mistakes, the anti-pattern list, the quality dimensions, and (if a `.puml` exists) `validate_domain_puml.py`.
- Each remaining trade-off that is a genuine judgment call (class vs attribute; concept in this domain vs an adjacent one) is surfaced as a short review note, not resolved by endless looping.
- In review/teaching mode, a concise "what changed across passes" summary is a good way to show convergence.

## Packaging Guidance

Use packages when the diagram is medium or large. Good package names come from the domain itself. Examples:

- Users and roles
- Core domain
- Transactions or requests
- Resources or assets
- Costs, payments, and billing
- Policies and rules
- Records, history, evidence, incidents, and notifications

Do not force these packages when the project domain suggests better groupings. Do not use packages in small diagrams if they make the model harder to read.

## Review Checklist

- Are all classes stable domain concepts?
- Are any classes really actions, UI, database, design patterns, or implementation?
- Are attributes allowed by the user's prompt?
- Are multiplicities absent (unless explicitly required)?
- Are operations absent?
- Are relationships short, conceptual, and non-redundant?
- Were procedural labels rewritten into conceptual relationship labels?
- Is every class connected or otherwise justified as a superclass or traceable vocabulary?
- Is generalization used when a general concept and true specializations both appear, and only when the substitution test holds?
- Is composition reserved for genuine lifecycle-dependent whole-part, with aggregation not overworked?
- Were state concepts considered when lifecycle conditions are central to the verbal model?
- Are events, states, exceptions, alerts, or incidents justified by the domain?
- Are hub-like classes reviewed rather than automatically removed?
- Is one term used per concept, with synonyms removed?
- Are packages helpful rather than decorative?
- Are terms traceable into later use case diagrams and specifications, and reused as the nouns of use case text?
- Was the model reviewed from the most relevant domain-expert perspective?
- Are syntactic, semantic, pragmatic, visual, and traceability concerns distinguished clearly?
- Were scoped checks completed and remaining trade-offs surfaced as notes (or the optional formal loop recorded when requested)?
- Is the result readable when rendered?

## Key References for Justification

Use these sources as conceptual support when the user requests documentation or academic justification. Keep citations concise in the answer; do not overload normal modeling output with references.

**Domain-modeling and UML practice:**

- Fowler, M. (2004). *UML Distilled: A Brief Guide to the Standard Object Modeling Language* (3rd ed.). Addison-Wesley. Use for the conceptual perspective, class-diagram notation, the substitution test for generalization, the semantics of composition and the (deliberate) lack of semantics of aggregation, and advanced constructs (association classes, enumerations, derived and qualified associations).
- Rosenberg, D., & Stephens, M. (2007). *Use Case Driven Object Modeling with UML: Theory and Practice*. Apress. Use for domain-model-first as a project glossary, prioritizing generalization and aggregation, referencing domain classes by name in use case text, the timeboxed first pass, and the common-mistake catalog.
- Rosenberg, D., Stephens, M., & Collins-Cope, M. (2005). *Agile Development [abbreviated title]*. Apress. Use for minimal-yet-sufficient / low-ceremony modeling, iterating the domain model across increments, and the one-term-per-concept discipline.
- Wiegers, K., & Beatty, J. (2013). *Software Requirements* (3rd ed.). Microsoft Press. Use for analysis models that augment (not replace) written requirements, requirement-quality characteristics (unambiguous, consistent, complete, verifiable, traceable), the glossary/data dictionary distinction, and traceability.

**Conceptual-modeling and notation quality:**

- Krogstie, J., Lindland, O. I., & Sindre, G. (1995). Defining quality aspects for conceptual models. Use for syntactic, semantic, and pragmatic quality dimensions.
- Moody, D. L. (2009). The physics of notations: Toward a scientific basis for constructing visual notations in software engineering. Use for visual effectiveness, cognitive load, discriminability, and diagram readability.
- Object Management Group. (2017). OMG Unified Modeling Language Version 2.5.1. Use for UML notation, class relationships, generalization, and modeling constraints.
- Wand, Y., & Weber, R. (2002). Research commentary: Information systems and conceptual modeling: A research agenda. Use for conceptual modeling as representation of domain phenomena and for discussing conceptual-modeling rigor.
