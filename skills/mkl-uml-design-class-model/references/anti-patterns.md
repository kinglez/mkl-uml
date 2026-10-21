<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Design class model anti-patterns

Catalog organized as **symptom → why it matters → correction → recipient**. The first six are named by the source itself; the others derive from explicit rules of the method, and their wording is our own.

`[automated]` means the validator detects it; `[judgment]` means it requires inspection.

---

## Broken provenance

### 1. Element without provenance `[automated]`

**Symptom.** A significant operation has no originating Operation-call or declared contract/design-delta evidence within scope; an attribute has no requirements/domain/interface origin; a relationship lacks domain or design justification. Replies, Signals, and lifecycle arrows do not imply ordinary receiver operations.

**Why it matters.** This violates the governing rule. This is the last artifact before code: unsupported elements become classes, fields, or methods someone must write and maintain without knowing why they exist. A sound model *"contains purely the detail we've uncovered during domain modeling, robustness analysis, and sequence diagramming, and nothing more"*.

**Correction.** Report the provenance gap and revisit the relevant artifact; apply supported corrections within the user-authorized scope. Record actual rationale/evidence rather than manufacturing provenance. The source says: *"use it as an indication that you need to revisit your previous diagrams, not that you need to second-guess yourself and add detail arbitrarily"*.

**Recipient:** `/mkl-uml-sequence-diagram`, `/mkl-use-case-specifier`, or `/mkl-uml-domain-modeler`, depending on what is missing.

### 2. Undeclared solution class `[automated]`

**Symptom.** A class is absent from the domain model and lacks `<<solution>>`.

**Why it matters.** Problem and solution spaces become silently mixed. When the framework changes, nobody knows which classes survive. The source explains: *"base the key abstractions in the code on true statements about the problem domain, because the problem domain winds up being the most stable"*.

**Correction.** Declare it, applying this test: if removing the stereotype would make you put it in the domain model without hesitation, it is **not** a solution class; it is a missing domain class.

### 3. Vocabulary drift `[automated, partial]`

**Symptom.** The same class has different names in domain and design: `Order` versus `Purchase`.

**Why it matters.** It breaks traceability and **conceals anti-pattern #2**: a “new” class may simply be an old one renamed; counting it as new duplicates it.

**Correction.** The domain name governs unless the change is declared. If the design name is better, route the correction **back** to `/mkl-uml-domain-modeler`.

**Check limitation:** detects spelling variation (`VaccinationRecord` / `VaccineRecord`), **not** synonyms (`Order` / `Purchase`). Lexical measures do not identify synonyms; human judgment must.

---

## Responsibility allocation

### 4. Anemic domain model `[automated]`

**Symptom.** Domain classes contain only data; all logic resides in controllers and services.

**Why it matters.** The source names *"a design where the domain classes are all data and no behavior"* and quotes Fowler: *"The fundamental horror of this anti-pattern is that it's so contrary to the basic idea of object-oriented design."* Fowler also says: *"You should be very afraid of classes that are nothing but a collection of fields and their accessors."*

**Correction.** Revisit the sequence diagram. If every operation ended up in an `XService`, the defect is in behavior allocation. The sequence skill calls this **centralized control**.

**Recipient:** `/mkl-uml-sequence-diagram`.

### 5. Class with a “schizophrenic personality” `[judgment]`

**Symptom.** Unrelated sets of operations share one class. The CDR source says: *"Look for classes without attributes and for classes with 'schizophrenic personalities' (i.e., unrelated sets of operations)."*

**Why it matters.** The class has multiple responsibilities. This corresponds to the **discordant attributes test** used in behavior allocation.

**Correction.** Split it: *"a class has gained too many responsibilities and needs to be split in two using aggregation"*.

**Not automated.** Assessing cohesion requires understanding each operation; the validator only counts them (#9). This test requires human judgment.

### 6. Class without responsibilities `[automated]`

**Symptom.** A class has attributes and **no** operations—*"rather impoverished, with no responsibilities"*.

**Why it matters.** This is the individual case of #4. It may be legitimate—a pure value class—but warrants justification.

**Correction.** Check whether an operation on another class belongs here. Behavior belongs where the knowledge resides.

### 7. Entity without attributes `[automated]`

**Symptom.** An entity class declares no attributes.

**Why it matters.** User-entered data has nowhere to go. The source emphasizes the timing: *"If you know that a class needs an attribute, add it to the class diagram! It's your last chance to do so before coding."*

**Correction.** Recover attributes from the specification and prototypes: *"Fields on screens often imply attributes on entity classes"*.

**Recipient:** `/mkl-use-case-specifier` if the text also omits them.

---

## Granularity

### 8. Swarm of tiny classes `[automated, heuristic]`

**Symptom.** Dozens of classes with one or two operations each.

**Why it matters.** *"it's possible to 'overnormalize' the design and end up with hundreds of tiny classes flying around."* Balance is needed *"between monolithic, thousand-line classes … and swarms of tiny classes"*.

**Correction.** Find classes that always collaborate and consider whether they are two aspects of one class.

### 9. God class `[automated]`

**Symptom.** One class has far more operations and attributes than its neighbors.

**Why it matters.** The opposite extreme of #8, and the same failure as centralized sequence control: behavior accumulated instead of being allocated.

**Correction.** Apply the discordant attributes test and split the class.

**Threshold note:** the numbers are **skill conventions, not evidence**; no corpus source specifies them. God class: more than **12** operations or **12** attributes. Swarm: at least **8** classes, with more than **half** having at most one operation. Vocabulary drift suggestion: similarity **0.72**. These generate warnings, never errors.

---

## Implementation intrusion

### 10. Premature pattern adoption `[automated, partial]`

**Symptom.** A pattern appears because it sounds attractive: a `SessionFactory` with no demonstrated need.

**Why it matters.** *"A SessionFactory is clearly part of the solution space, not the problem space, as are most design patterns."* The source also locates the timing: *"Design patterns usually begin to emerge during robustness analysis (preliminary design)."*

**Important distinction from robustness's *design-pattern-itis*:** patterns **are welcome here**. Pre-CDR cleanup explicitly includes *"identifying useful design patterns that can be factored in to improve the design"*. The finding concerns using a pattern **without any sequence message requiring it**. Provenance is the test, not its name.

**Correction.** Justify it from the sequence or remove it.

### 11. *Getters* and *setters* in the model `[automated]`

**Symptom.** `getName()`, `setName()`, and similar methods fill the operation compartment.

**Why it matters.** *"Our advice is to avoid adding them to your model."* They can be generated from attributes and produce *"a busy-looking class diagram"* that hides important operations.

**Correction.** Remove them, retain private attributes, and rely on encapsulation.

### 12. Low-level private methods `[judgment]`

**Symptom.** Internal helpers appear on the diagram.

**Why it matters.** Agile Development (2005) omits them because *"they may be a bit too low level to warrant showing on the class diagram"*. They couple model and code *"too tightly"*: each internal refactor requires redrawing.

**Correction.** Remove them; retain the public operation that uses them.

### 13. Excessive detail `[judgment]`

**Symptom.** Every operation, dependency, and multiplicity is shown.

**Why it matters.** Fowler: *"comprehensiveness is the enemy of comprehensibility"*. Showing every dependency is *"an exercise in futility"*. The diagram *"acts as a graphical table of contents"*, not as source code.

**Correction.** Show *"only the important features"*.

---

## Process defects

### 14. Model omits assigned operations `[automated]`

**Symptom.** The sequence assigns operations absent from the class model.

**Why it matters.** This is the literal **CDR entry criterion**: *"You should also have updated the class diagrams so that all of the operations that you assigned during sequence diagramming are reflected in the static model."* A model failing this should not pass the gate.

**Check level:** warning, not error. Comparison uses vocabulary rather than an operation list, so gaps may arise because message labels are phrases rather than method names. The analyst decides whether anything is truly missing; the CDR is the gate, not this script.

**Correction.** Apply the complete operation delta.

### 15. Operation on the wrong class `[judgment]`

**Symptom.** The class owning an operation disagrees with its demonstrated originating call receiver. Asymmetric operations (adds without removes, opens without closes) are only clues to inspect, not defects by themselves.

**Why it matters.** This is the CDR's reverse technique: *"You can find most sequence diagram errors by looking at the class diagram."* The source describes *"a Queue class that had only an Add method. Nobody was removing anything from the queue, ever!"* because arrows had been drawn backward.

**Correction.** Check call classification, receiver, scope, and responsibility. Correct a proven misdirected call and dependent model; do not infer or add inverse operations merely from asymmetry.

**Recipient:** `/mkl-uml-sequence-diagram`.

### 16. Layout substitutes for content `[judgment]`

**Symptom.** Hours of visual adjustment while provenance gaps remain.

**Why it matters.** *"try not to spend hours tinkering with the layout"*; these diagrams are *"about showing a structural overview of the code you're about to write"*.

**Correction.** Resolve findings first.
