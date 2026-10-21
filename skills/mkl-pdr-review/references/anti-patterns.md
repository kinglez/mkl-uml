<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Anti-patterns that the PDR hunts

Catalog for review. Each brings **symptom → why it matters → correction → recipient**, where the recipient is the sibling skill that owns the defective artifact.

These anti-patterns are different from those in robustness analysis: those live **within** a diagram; almost all of these live **among** artifacts, which is where no one else looks.

---

## Defects between artifacts

### 1. Floating entities

**Symptom.** A domain entity in robustness has neither a corresponding domain class nor a disclosed discovery delta. Domain classes unused by the selected package are informational; they may serve other use cases.

**Why it matters.** It's non-compliance with guideline #9, and its usual cause is benign but expensive: robustness analysis **discovered** an object—which is exactly what it was supposed to do—and no one returned it to the model. The gap is paid in the detailed design, where two artifacts disagree about which classes exist.

**Frequent causes:** the discovery occurred and the record was forgotten; names differ between artifacts (see #2); The artifacts were made by different teams without synchronization.

**Correction.** Validate whether this is a domain concept, a synonym, or an interface/actor role. Add a supported new domain concept when domain updates are authorized; otherwise record its discovery delta. Only domain entities require domain closure. **Prevention:** retain a single domain vocabulary with stable identities.

**Recipient:** `/mkl-uml-domain-modeler`.

### 2. Vocabulary drift

**Symptom.** Same concept with different names in different artifacts: `Order` in the domain model and `Purchase` in robustness; "matching titles" in the text where the domain says `Book`.

**Why it matters.** It breaks traceability and reintroduces precisely the ambiguity that guideline #3 wants to eliminate. It also **masks** anti-pattern #1: a floating entity may actually be the same class with another name, and counting it as missing leads to duplicating it in the model.

**Correction.** Set the domain model term as canonical and align the other artifacts. If the two names designate genuinely different concepts, then the defect is the opposite: a class is missing.

**Caution when detecting it automatically:** name similarity is a **candidate match**, never a certainty. Present it as a question—"are `Order` and `Purchase` the same concept?"—and let the analyst decide.

**Recipient:** depends on what the correct name is; by default `/mkl-uml-domain-modeler`.

### 3. Data that goes nowhere

**Symptom.** Required interface input/output data has no explained destination/source in the model. This is a candidate gap, not proof that every interface field must persist or every attribute must be exposed.

**Why it matters.** Guideline #8 seeks explained data movement. Data may be transient, derived, machine-supplied, or intentionally internal. Check those origins before claiming data loss, an unused attribute, or a missing interface.

**Correction.** The guideline itself says it: during the review, **populate the class model with the missing attributes**. The PDR not only detects this defect; It's time to fix it.

**Recipient:** `/mkl-uml-domain-modeler` for attributes; `/mkl-use-case-specifier` if what is missing is the step that collects the data.

### 4. Out of place actor

**Symptom.** Actor participation differs between artifacts covering the same use-case scope without explanation. An actor absent from a particular diagram may legitimately participate in another use case.

**Why it matters.** The use case diagram, when available, is cross-artifact evidence for external roles. A newly discovered actor needs requirements/interaction evidence; absence from an optional diagram alone does not prove unauthorized behavior.

**Frequent and serious variant:** treating as an actor something that is not an actor — a database, an internal module, a table. An actor models an **external role interacting with the subject by exchanging data or signals**. Supporting actors need not initiate a goal.

**Correction.** Reconcile with the use case diagram, or justify the new actor and add it there first.

**Recipient:** `/mkl-uml-use-case-diagram`.

### 5. Inconsistency between use case and interface

**Symptom.** The data requested by the specification does not match the fields shown in the wireframe or mockup.

**Why it matters.** It is the concrete reverse of "in the context of the GUI" (guideline #3). Boundary objects derive from named human or machine interfaces; entity concepts derive from domain vocabulary. If the supplied interface and specification evidence disagree, resolve the real mismatch within scope.

**Correction.** Report it as a traceability finding. **Don't figure it out on your own**: which of the two sources is in charge is a decision of the analyst, and often the client — who is in the room for precisely that reason.

**Recipient:** `/mkl-use-case-specifier`, or the owner of the prototype.

---

## Use case text defects

### 6. One-sided use case

**Symptom.** The text describes only what the user does, without a response from the system: *"the user opens the application, navigates to the catalog, selects a book, presses buy"*.

**Why it matters.** It violates guideline #6. A use case is a **dialog**; if the system does not respond in the text, its behavior is not specified anywhere, and what is not specified is not implemented.

**Correction.** Intersperse the system response in each step where appropriate: what it validates, what it shows, where it leads.

**Recipient:** `/mkl-use-case-specifier`.

### 7. Empty alternate course

**Symptom.** The text states the alternate —*"if the user is not authenticated, show error"*— but does not say which screen shows it, if it can be redirected to the login, what happens to the current state, or how to recover it.

**Why it matters.** It is the most common anti-pattern and the most expensive, because the alternate courses account for more than half of the complexity. Listing is not specifying: the source says it unambiguously — identifying what can happen is necessary but not sufficient.

**Correction.** Detail the exact user and system behavior for that alternate. The questions that uncover it: what can go wrong here? · Is there a special condition that changes the flow? · Can the user abandon at this point?

**Recipient:** `/mkl-use-case-specifier`.

### 8. Alternate course without a triggering validation

**Symptom.** The text declares an alternate course, but the base flow does not have the validation step from which it could branch.

**Why it matters.** This is different from the orphan alternate drawn without text: here the defect is in the **specification**, which declares an outcome without specifying the check that produces it. It appears when reviewing because the branch has no triggering step.

**Correction.** Add the validation step to the basic flow, or remove the alternate one if not applicable.

**Recipient:** `/mkl-use-case-specifier`.

### 9. Language that breaks the mini-contract

**Symptom.** Text or element names are only understood by a programmer. Or, at the opposite extreme, they are so vague that they do not commit anything: "the system processes the information."

**Why it matters.** After the PDR, the use cases are mini-contracts between the client and programmers, and for that they must reach the right level of abstraction: neither vague nor technical jargon. If the non-technicians in the room disengage, the contract does not exist — and the source gives that disengagement as a **diagnostic sign** that the material entered detailed design.

**Correction.** Rename in domain vocabulary; Replace vague nouns with the domain model term.

**Recipient:** `/mkl-use-case-specifier`, and `/mkl-uml-robustness-diagram` for diagram element names.

---

## Abstraction-level defects: entering detailed design too early

### 10. Robustness disguised as sequence

**Symptom.** The "robustness diagram" has repeated lifelines above and below, combined fragments (`alt`, `opt`, `loop`, `par`), numbered leading arrows, and messages with method and parameter signatures: `addToCart(isbn, quantity)`. Concepts such as session, transaction or cache appear.

**Why it matters.** It violates guideline #2 and step 6. The robustness diagram is an **idealized conceptual design**; The mapping of behavior between classes belongs to the sequence diagram. Advancement freezes decisions without the necessary information and, worse, makes people believe that the analysis is more advanced than it is.

**How to distinguish it mechanically.** A sequence diagram states each participant **twice** (top and bottom box); robustness one declares each object once. That single clue, together with the `alt` fragments and the signatures with parentheses, is enough to reliably separate them.

**Correction.** Redo the diagram in robustness notation: objects declared once, associations without direction, Controllers with semantic name. Save the detail for the next stage.

**Recipient:** `/mkl-uml-robustness-diagram`.

### 11. Design-pattern-itis

**Symptom.** Controllers named `CartObserverFactory`, `AuthStrategyHandler`, `FindBookRepositoryProxy`; `Factory`, `Singleton`, `DAO`, architecture layers appear.

**Why it matters.** Step 5 calls it out by name. It is a solution space within a conceptual artifact, and brings up the problem of guideline #4: if a non-technical participant does not understand the name of a Controller, it is a sign that it is being designed too early.

**Correction.** Semantic name that describes the intent: `Register order`, not `OrderDAOImpl`.

**Note of origin.** The source uses the term "design-pattern-itis" without defining it. This operational reading—pattern names in Controllers—is **our interpretation**, consistent with step 6 and guideline #2, and is stated as such.

**Recipient:** `/mkl-uml-robustness-diagram`.

### 12. Operations assigned ahead of time

**Symptom.** Notes with `save() : void` hanging on entities; methods assigned to classes in the domain model.

**Why it matters.** Assigning behavior is the **second pass**; Doing it here is skipping the first one. The source is explicit that these decisions are deferred to sequence diagrams.

**Correction.** Remove them. The discovered attributes do go to the domain model—in fact guideline #8 requires it—; operations, no.

**Recipient:** `/mkl-uml-domain-modeler` or `/mkl-uml-robustness-diagram`, depending on where they are.

---

## Defects of the review itself

These are not in the artifacts: they are in how the PDR is conducted. They are verified against the record.

### 13. Review without a client

**Symptom.** There are only technical participants in the room.

**Why it matters.** It violates guideline #4 and defeats the purpose of the milestone: the PDR is the customer's last direct entry point. Without someone validating that the language is understood, it cannot be said that use cases are contracts.

**Correction.** Summon a product representative if the customer cannot. If there is still no one, **declare it in the minutes** and mark guideline #4 as not executed.

### 14. Review above the pace

**Symptom.** The package is much larger than 3-4 pages/hour allows viewing in the scheduled session.

**Why it matters.** Detection ability plummets with pace. A review that is too quick does not find proportionally fewer defects: it finds almost none — and issues the same verdict, which is what is dangerous.

**Correction.** Split the package into several sessions. It is in the minutes as a session budget precisely so that this decision is made with a number in front of it.

### 15. Verdict downgraded due to fatigue

**Symptom.** A package with open major findings returns as `Accepted with rework verification` because time has run out or it is the third round.

**Why it matters.** It destroys the value of the gate. A fake `Accepted` authorizes the detailed design with a guarantee that does not exist, and the defect reappears later and at a higher cost.

**Correction.** The verdict comes from thresholds, not mood. If it is the third round and it still does not pass, the answer is not to approve it: it is to **split the use case**, as indicated by the review-count metric.

### 16. Finding without an owner

**Symptom.** The report lists defects without a person responsible or a date.

**Why it matters.** The reference material asks to record each finding as a pending task with the owner and date, and IEEE 1028 makes the classification of anomalies mandatory. A finding without an owner is not closed: it is forgotten, and reinspection finds it again.

**Correction.** For a formal action record include severity, recipient, and agreed owner/date. Do not invent an owner or date: mark them unresolved if no decision exists. For a scoped check a verifiable finding and concrete correction are sufficient; preserve the existing `H-XX` identity.
