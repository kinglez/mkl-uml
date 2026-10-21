<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Behavior allocation: which class receives each operation

Step 4 is the non-automatable step that gives the diagram value. These decision criteria also state **where automation is unavailable**. Source verification records retain the historical upstream research status.

---

## Two questions

The source reduces step 4 to (4187):

> - *"What are the classes?"*
> - *"Which classes are **responsible** for which operations?"*

Domain and robustness already answer the first. **The second is the work.**

## What is a responsibility?

The source (4192), tracing the idea to Rebecca Wirfs-Brock's *Responsibility-Driven Design*:

> *"A **responsibility** is a combination of things: knowledge or data (the attributes), behavior (the operations), and the major decisions made at runtime that affect others."*

**Behavior belongs where knowledge resides.** An operation reading three attributes of another class to decide usually belongs to that class.

Easy example (4194): *"it should be obvious that a BookReview will be responsible for validating its own data"*. **A class validates its own data.** Apply obvious decisions without prolonged debate.

## When responsibility is too large

The difficult-case test (4210), drawing on Wirfs-Brock:

> *"A class with a split personality—or multiple personalities—is a class that has more than one responsibility. A clear sign of such a troubled class is if it contains **discordant** attributes"*

**Discordant attributes test:** inspect attributes; one that does not belong with the others signals multiple responsibilities. Use **aggregation** to move such attributes to more appropriate collaborating classes.

Conversely, if an operation requires adding a discordant attribute, **it does not belong there**.

## Four criteria of a good class

“Four Criteria of a Good Class” (4212), taken from Booch, who cites **Halbert and O'Brien**:

| Criterion | Question |
|---|---|
| **Reusability** | Is this a reusable component corresponding to a problem-domain abstraction? |
| **Applicability** | Do behaviors belong together, or are they unrelated responsibilities? |
| **Complexity** | Does any class have more than it can comfortably manage? |
| **Implementation knowledge** | Does the class depend on another's internals? |

The source's compact criterion (4222):

> *"maximize cohesion, minimize coupling"*

## Six role stereotypes (Wirfs-Brock)

External supplement, recorded upstream as **verified** in the author's presentation *A Brief Tour of RDD in 2004* (Wirfs-Brock Associates). Simplified views of roles: each object fits at least one, and combinations are normal.

| Stereotype | Characterized by | Example |
|---|---|---|
| **Information holder** | What it **knows** | `TransactionRecord`, `Account` |
| **Structurer** | Whom it knows and what it knows about them | `Order` |
| **Service provider** | What it **does**: calculation, transformation | `CreditChecker` |
| **Controller** | **Decisions** it makes | `TransactionController` |
| **Coordinator** | Actions it **delegates** | `ViewCoordinator` |
| **Interfacer** | Communication and hidden details | UI objects, wrappers |

**Allocation use:** identify the candidate's role first. An information holder making decisions is becoming a controller without an explicit decision; a coordinator doing delegated work has stopped coordinating.

**Two allocation guidelines**, verbatim: *"Keep behavior with related information"*, *"Keep information about one thing in one place"*. Fulfill responsibility directly or **delegate part to helpers**: *"Delegate control if possible. Let collaborators be responsible"*.

**Message naming:** prefer **strong verbs**—delete, merge, calculate, credit, activate—to weaker verbs—organize, register, process, maintain, accept. The validator applies the same idea to generic messages.

## GRASP as complementary vocabulary

Nine responsibility-allocation patterns (Larman, *Applying UML and Patterns*). **Secondary confidence:** two restatements were read, not the original book, absent from the corpus. They name decisions that otherwise risk arbitrary rationale:

- **Information Expert:** responsibility goes to the class with the required information; matches the primary rule.
- **Creator:** instantiate `A` in a class that contains, records, closely uses it, or has initialization data.
- **Controller:** a non-UI object receives/coordin­ates a system operation; facade or per-use-case controller. *"The keyword is delegation"*: coordinate without doing everything.
- **Low Coupling** and **High Cohesion:** **evaluative** criteria for comparing alternatives, not placement rules. Excessively low coupling can signal low cohesion.
- **Polymorphism:** assign type-varying behavior to varying types instead of branching by type.
- **Pure Fabrication:** if Information Expert harms cohesion/coupling, use an artificial non-domain class; legitimate justification for a service.
- **Indirection** and **Protected Variations:** mediate to reduce coupling and isolate predictable change points.

**Combination:** Information Expert restates behavior-with-knowledge; Pure Fabrication justifies the remaining 20% of Controllers becoming classes; High Cohesion/Low Coupling matches *"maximize cohesion, minimize coupling"*.

## Distributed versus centralized control

Fowler's visual quality test (1526-1556): **centralized** means one participant processes while others *"to supply data"*; **distributed** means participants each perform part of the algorithm.

Two substantive reasons for distributed control:

> *"One of the main goals of good design is to localize the effects of change"*

> *"by distributing control, you create more opportunities for using polymorphism rather than using conditional logic"*

## The anemic domain model

The accumulated failure: Entities only receive `get`/`set`, while controllers/services contain all logic.

**Early source warning** (3865): *"sometimes a framework might tempt you to litter your design with dozens of tiny 'controller classes'"*. An `XController` and `XService` per entity is disguised functional decomposition and contradicts Fowler's principle.

**Correction:** return self-validation, derived calculations, and invariant decisions to Entities whose state they use.

## Procedure for step 4

1. **Inspect every `DR-XX` Controller**: guideline #7 makes them the behavior worklist.
2. Ask **which class has the required knowledge**.
3. Apply obvious answers directly.
4. Otherwise use the discordant attributes test.
5. **Split** responsibilities too complex for one class across collaborators.
6. **Record rationale** so allocation is auditable rather than opinion.
7. Check distribution: does one participant send nearly all messages? Is any Entity left without behavior?

## What scripts cannot check

State judgment limits explicitly; false claims of coverage create false positives that teach people to ignore validators.

- **Correct receiving class.** The script checks Controller completeness, not whether `calculate amount` belongs on `Ticket` or `Rate`; use the criteria above.
- **Message chains/Law of Demeter.** UML has **no Demeter-specific construct**. The observable clue is: *`A` sends to `B`; `B` returns a reference to `C`; `A` then sends directly to `C`*, without immediate-neighbor status. A **returned reference becomes the original sender's subsequent message receiver**. Reliable detection requires knowing which returns carry object references; labels do not establish that.

  **This check is deliberately not automated.** A naive `A→B→C→D` chain check flags **distributed delegation**, exactly what Fowler recommends. An earlier attempt did this to a sound design; penalizing sound design undermines the validator.

  The script instead checks the automatable relative: **consecutive self-calls**, suggesting an algorithm hidden in one object. Chains remain **human review** using the precise pattern above.

  *(Provenance: Lieberherr & Holland, “Assuring Good Style for Object-Oriented Programs,” IEEE Software 6(5), 1989. Known through restatements: **located originals are scanned images without text layers**, so exact class/object formulations were not read.)*
- **Justified controller class.** Managers/dispatchers among the remaining 20% require domain knowledge to assess.

---

## Provenance note

Wirfs-Brock & McKean's *Object Design: Roles, Responsibilities and Collaborations* **is absent from the corpus**, known through citations in available books. Sources disagree slightly on year: course material says 2002; Rosenberg & Stephens footnote says 2003 (Addison-Wesley, p. 132). **Omit the year until checked against the original.** Responsibility and split-personality definitions here come from the read Rosenberg & Stephens text, not the original work.
