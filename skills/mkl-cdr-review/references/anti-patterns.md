<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CDR anti-patterns

Catalog with **symptom → why it matters → correction → recipient**. Flags `[automated]` when detected by the validator; `[judgment]` when it requires reading.

Each entry also carries its **anomaly category** from IEEE 1028 §6.8.2, because the distinction between a demonstrated error and a `Risk-prone` changes how the finding is presented.

**Those that the source names are cited.** Where the formulation is ours, it is said.

---

## Broken correspondence — the axis of the CDR

### 1. The sequence does not say what the text says `[automated, partial]` · *Inconsistent*

**Symptom.** A use case behavior phrase with no messages that perform it, or messages that no phrase explains.

**Why it matters.** It's rule #10, the first on the list and — depending on the course — *"probably the most important validation of the entire review"*. If the design and the text disagree, one of the two is wrong and no one knows which; the code will inherit the discrepancy.

**Correction.** Apply the Highlighter Technique phrase by phrase. If design is missing, it goes to the sequence; If there is excess design, either the text is incomplete or the design invented behavior.

**Check limit:** The validator compares vocabulary and detects flows without messages. **The validator cannot judge whether the match is faithful** — just because the words match does not prove that the design does what the phrase asks for.

**Recipient:** `/mkl-uml-sequence-diagram` or `/mkl-use-case-specifier`, depending on which side the hole is on.

### 2. Undesigned alternative course `[automated]` · *Missing*

**Symptom.** A specified `FA-XX` or `FE-XX` that has no fragment or diagram in the sequence.

**Why it matters.** Rosenberg puts it bluntly (4590): *"Don't make the mistake of saying YAGNI about those pesky rainy-day scenarios."* And the course proves it right: *"Alternative scenarios often contain much of the system's complexity."* What was not designed will be improvised when coding.

**Correction.** Add the fragment. If the flow turned out not to apply, remove it from the specification — don't leave it orphaned.

**Recipient:** `/mkl-uml-sequence-diagram`.

### 3. Operation on the wrong class `[automated]` · *Incorrect*

**Symptom.** A demonstrated originating Operation-call receiver differs from the class owning the operation. Asymmetry (adds without removes, opens without closes) is only a review clue, not a proven defect.

**Why it matters.** It is the defect that the source illustrates with its most cited case (4646): *"Doug found a **Queue class that had only an Add method**. Nobody was removing anything from the queue, ever!… the message arrows were drawn backward."* And the technique that finds it (4648): *"**You can find most sequence diagram errors by looking at the class diagram.**"*

**Correction.** Check the actual call sort, signature, receiver, and responsibility before changing either artifact. Where evidence confirms a wrong arrow, correct it and its dependent model within the authorized scope. Do not invent inverse operations from asymmetry, replies, Signals, or lifecycle messages.

**Recipient:** `/mkl-uml-sequence-diagram`.

### 4. Operation without origin `[automated]` · *Extra (superfluous)*

**Symptom.** A significant model operation in the selected scope has no originating Operation-call or declared contract/design-delta evidence. Other message sorts are not operation evidence.

**Why it matters.** The CDR entry criteria requires that the model reflect what is assigned in the sequence — no more. One operation too many is code that someone will write without knowing why.

**Correction.** Check scope, other scenarios, and declared contracts first. Report a missing call or unsupported operation only when that check establishes the gap; unknown message kinds stay unresolved.

**Recipient:** `/mkl-uml-sequence-diagram` or `/mkl-uml-design-class-model`.

### 5. Requirement without implementation, class without requirement `[automated]` · *Missing* / *Extra*

**Symptom.** A requirement that does not reach any class, or a class that no requirement explains.

**Why it matters.** It's rule #5. The course formulates it precisely: *"Without traceability it is difficult to know if functionality is missing, there are unnecessary components, or a change in requirements affects the design."*

**The two directions are different defects** and are reported separately: lack of functionality versus excess design.

**Recipient:** `/mkl-use-case-specifier` or `/mkl-uml-design-class-model`.

---

## Distribution of responsibilities

### 6. Anemic domain model `[automated]` · *Risk-prone*

**Symptom.** Entities are all data and no behavior; logic lives in controllers, services and *helpers*.

**Why it matters.** It is the worked case of the chapter itself (4658, *"Book Is Devoid of All Responsibilities"*): *"But it has no behavior. It will end up with lots of getters and setters, but no actual responsibilities."* And the underlying reason (4686): *"**Centralization of responsibility for books in the Book class means that if something changes about books… you ought to be able to find it pretty quickly by looking at the Book class**, instead of searching through dozens of itty-bitty one-method classes."*

The course explains it with a useful analogy: *"Imagine a company where employees only store information and never do work. All activity ends up concentrated in the managers."*

**Correction.** Move behavior to the entity that has the knowledge. In the case of the book: `load()` was moved to `Book`.

**Recipient:** `/mkl-uml-sequence-diagram` — because anemia is decided by assigning behavior, not by drawing classes.

### 7. Multiple personality class `[judgment]` · *Risk-prone*

**Symptom.** Unrelated operations in the same class. The course exemplifies with `BookManager`: `saveBook()`, `deleteBook()`, `generateInvoice()`, `sendEmail()`, `calculateTaxes()`.

**Why it matters.** Tip literal from 4600: *"Look for classes without attributes and for classes with **'schizophrenic personalities'** (i.e., unrelated sets of operations)."* Signals more than one responsibility in a class.

**Correction.** Split the class by responsibility.

**Not automated, and that's honest to say.** Measuring cohesion requires understanding what each operation does. The validator counts operations and flags candidates by volume (anti-pattern #12); **the reviewer decides whether those operations represent unrelated responsibilities**.

### 8. Class without responsibilities `[automated]` · *Risk-prone*

**Symptom.** A class with attributes and no operations.

**Why it matters.** The source describes it as *"rather impoverished, with no responsibilities"* (4602). It may be legitimate—a pure value class—but it is rare and deserves justification.

**Correction.** Check if any operation that is in another class should be here.

### 9. Entity without attributes `[automated]` · *Missing*

**Symptom.** An entity without any declared attributes.

**Why it matters.** The data that the system manages has nowhere to live. Tip from 4912: *"You should identify attributes and add them to their classes during robustness analysis. **You then put the functions where the data lives.**"*

**Recipient:** `/mkl-uml-domain-modeler` if the domain does not have them either.

---

## Leftover elements

### 10. Wrapper class `[automated]` · *Extra (superfluous)*

**Symptom.** A class that aggregates another class, whose attributes are a subset of those of that one, and whose operations are all delegating accessors.

**Why it matters.** It is the second worked case of the chapter (4848, *"WriteCustomerReviewCommand Seems Redundant"*): *"it seems like WriteCustomerReviewCommand is just a **wrapper class** around the CustomerReview entity. **Is the Command class really needed?**"* The figure in the book finishes it off with a note: *"getRating(), getTitle() and getReview() are **wrapper methods around the CustomerReview properties**."*

The course gives the analogy: *"Imagine a box that contains another identical box. If they both store exactly the same information: do we really need both?"* And the cost argument: *"Each additional class implies more code, more maintenance, more testing, more documentation."*

**The automatable criterion**, derived from the figure: **X aggregates Y · the attributes of X are a subset of those of Y · the operations of X are all accessors**. When all three are met, it is a candidate.

**Correction.** Delete it and use the entity directly. In the case of the book, the model went from five classes to four.

**Caution.** *"It doesn't mean it should always be removed. But it does deserve careful review."* A wrapper may be justified by the framework; then `<<solucion>>` is declared and explained.

**Recipient:** `/mkl-uml-design-class-model`.

### 11. Object without messages `[automated]` · *Missing*

**Symptom.** A lifeline drawn in the sequence to which no one sends any messages.

**Why it matters.** Verbatim quote from 4820-4846: *"If you find an object sitting all on its own on the sequence diagram, **without any messages being passed to it**, it's likely that you've discovered a part of the design that hasn't been thought through in sufficient detail."*

**Correction.** Either the object participates and its messages are missing, or it does not participate and is left over.

**Recipient:** `/mkl-uml-sequence-diagram`.

### 12. God Class `[automated, heuristic]` · *Risk-prone*

**Symptom.** A class with many more operations and attributes than its neighbors.

**Why it matters.** It concentrates responsibilities that should be shared. The course illustrates it with a `BookController` that validates, saves, searches, calculates prices, generates reports and sends emails: *"The class does too many things."*

**Threshold note, and it is important.** The corpus **does not set any numerical threshold** for this — neither of operations, nor of cyclomatic complexity. The numbers used by the validator are **convention of this skill**, they feed warnings and never errors. What there is is an empirical distribution rule, the 5/20/80 triage of `metrics-and-triage.md`, which orders by criticality instead of cutting by an invented number.

---

## Implementation details intruding into the model

### 13. Magic functionality `[judgment]` · *Ambiguous*

**Symptom.** Behavior that occurs without any message producing it.

**Why it matters.** Verbatim quote from 4610: *"the sequence diagram should show the 'real design' as you intend to code it. **Magic is not permissible on sequence diagrams.**"* What is not in the diagram, someone will improvise.

**Correction.** Draw what is actually going to happen, including the infrastructure: if there is a DAO, you can see it.

**Recipient:** `/mkl-uml-sequence-diagram`.

### 14. Undeclared unstable abstraction `[automated, partial]` · *Risk-prone*

**Symptom.** Technology-named classes—`JdbcBookDao`, `HibernateSession`, `SpringBookController`—without a solution-space stereotype.

**Why it matters.** Box from 4874-4886: *"**base the key abstractions in the code on true statements about the problem domain, because the problem domain winds up being the most stable**"*. The course develops it as *stable abstractions* (`Book`, `Customer`, `Order`, which survive the framework change) versus *unstable* (`Hibernate`, `Spring MVC`, `JDBC`, which do not).

**It's not that there are leftovers:** it's that if they are mixed with the domain without marking them, when the framework changes no one will know which classes survive.

**Correction.** Mark them `<<solucion>>` and justify them.

**Check limit:** detects known technology names; It does not recognize a framework that is not in its list.

**Recipient:** `/mkl-uml-design-class-model`.

### 15. Imprecise types `[automated]` · *Ambiguous*

**Symptom.** `Object`, `var` or equivalents as parameter or return type. The course example: `public Object process(Object data)` vs. `public Book load(int id)`.

**Why it matters.** Rule #3. *"It lacks precision. It makes maintenance difficult. It generates ambiguity."* An imprecise type transfers to the code a decision that the design should close.

**Recipient:** `/mkl-uml-design-class-model`.

### 16. Names that do not express intent `[automated]` · *Editorial*

**Symptom.** `doStuff()`, `process()`, `handle()`, `manage()`.

**Why it matters.** *"Names should clearly express the intent."* A generic name hides that the operation does not have a clear responsibility — it is often the visible symptom of anti-pattern #7.

**Note:** is the *Editorial* category of §6.8.2, the least severe. It reports, it doesn't block.

**Known limit of accessor detection, and why it is left like this.** The accessors (`getX`, `setX`, `isX`, `hasX`) are **exempt** from rule #8: they are generated from the attributes and do not need their own message. The validator recognizes them in `camelCase` and `PascalCase`, **not in ALL CAPS** — `GETNOMBRE()` is treated as a normal operation and origin is required.

An independent audit reported it, and **the decision was not to correct it**. Any pattern that captures `GETNOMBRE` also captures `HASTA` (HAS+TA), `SETENTA` (SET+ENTA), and `ISLA` (IS+LA) written in uppercase — and that reintroduces the **silent** exemption that this pattern came to remove. Between a noisy failure - a reported operation that you discard at a glance - and a silent one - an exempt operation that no one sees - this skill always prefers the noisy one.

Additionally, the pipeline notation is `camelCase` in all its rules and in all its test sets: an uppercase method does not belong in this contract. If your project uses them, the operation will appear as a finding of rule #8 and it is enough to declare it false positive.

### 17. Missing multiplicities `[automated]` · *Missing*

**Symptom.** Relationships without multiplicity in the design model.

**Why it matters.** Quote from 4864: *"At this stage of the design process, **we really should have identified the multiplicity for all these kinds of relationships** and added them onto the diagram."*

**The nuance that avoids contradicting the sister skill:** in the **domain** model, multiplicities are optional, and `/mkl-uml-domain-modeler` treats it that way. **Not in the CDR anymore**, because the design is about to become code and the multiplicity decides if a field is a reference or a collection.

---

## Defects of the review itself

### 18. Polish the diagram instead of closing findings `[judgment]`

**Symptom.** Time spent on aesthetics with open traceability gaps.

**Why it matters.** Caution literal 4944: *"try not to spend hours tinkering with the layout until it's so tidy and symmetrical it could be **mistaken for a map of midtown Manhattan**."*

### 19. Review above sustainable rate `[automated]`

**Symptom.** A package that exceeds what fits in one session, reviewed in one sitting.

**Why it matters.** It's `session-budget.md`'s empirical finding: effectiveness plummets with length because **reviewers skim**. Reviewing 60 pages at a time produces a report that looks like a review and is not.

**Correction.** Split the package. §5.1 authorizes it: *"may require more than one meeting."*

### 20. Review without findings on a large package `[automated]`

**Symptom.** Zero or almost zero findings on extensive material.

**Why it matters.** Contradicts the measured base rate of **0.4 failures/page** in design documents. Most likely, it's not that the design was impeccable: it's that the review was superficial.

**Correction.** Review the rules that came out clean before signing the minutes.

**Our formulation**, derived from real data. IEEE 1028 §6.9 supports it by requiring analysis of *"connections between preparation (checking) rate, meeting rate, and number and severity of anomalies found"*.

### 21. Reviewer fatigue `[judgment]`

**Symptom.** Third or fourth round on the same material.

**Why it matters.** Wiegers: *"Don't ask anyone to review the same material more than three times. He will be tired of looking at it and won't spot major issues after a third cycle because of **'reviewer fatigue.'**"*

**Correction.** If it doesn't pass the third time, the problem is not the review: it is the artifact or its scope. **That is also a finding**, and an important one.

---

## Origin

The anti-patterns **1-14 and 17-18** are named or illustrated by the source: Rosenberg chap. 9 (lines 4590, 4600, 4602, 4610, 4646, 4658, 4686, 4820-4846, 4848-4864, 4874-4886, 4912, 4944). **15-16** come from the course material, *Session 09*. **19-21** are our formulation on evidence from GQM/RITME, IEEE 1028 §6.9 and Wiegers chap. 17, and it is declared. Anomaly categories are from IEEE 1028 §6.8.2 — transcribed in `review-protocol.md`.
