<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# The ten PDR guidelines and the six steps

Main source: Rosenberg & Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice*, chapter "Preliminary Design Review". The quotes are verbatim and short; the locators are lines from the corpus file, so anyone can check them.

It's a **deliberate countdown**: Guideline #1 is the most important. That order is preserved because it is that of the source.

---

## #10 — The Highlighter Test

> *"make sure the use case text matches the robustness diagram, using the highlighter test"* (line 3179)

**Procedure, as stated in the source:** *"Simply highlight a sentence of your use case, highlight the corresponding section of your robustness diagram, and continue until all the text is highlighted"* (3200). And the other side of the check, on the same line: *"You should also see the entire robustness diagram highlighted"*. The complete explanation of the guide occupies 3192-3202.

**What each mismatch means:**

| Direction | Diagnosis |
|---|---|
| Unmarked text | Missing logic in the model: specified behavior that no one designed |
| Unmarked diagram | Undocumented behavior: design no one asked for |

The source assumes that mismatches will appear: *"If you find a mismatch between the text and the diagram (and trust us, you will), then you have more work to do"* (3202).

**Associated practices:** one color for the basic flow and another for each alternate; the entire use case in **a single diagram**; If the diagram grows too much, **split the use case**.

**Scope Note.** The same technique reappears later in the book applied to sequence diagrams (4586) and as an explanation for a late-found defect (4828) — it is not unique to PDR, it is a general review technique.

---

## #9 — All entities, in the domain model

> *"Make sure that all the entities on all robustness diagrams appear within the updated domain model."* (line 3180)

**Why.** Object discovery is a central purpose of robustness analysis. An entity appearing in robustness and not domain means that the discovery **occurred and no one returned it**.

**Recommended way:** add the new class to the domain model, stereotype it as an entity, and only then drag it to the robustness diagram. Order matters: prevent the diagram from being the only source of the class.

**Automatable, deterministic.** It is the highest-performance check of the validator and the one that feeds the *# non-domain entities* metric, whose goal is zero.

---

## #8 — Data flow traceability

> *"Make sure that you can trace data flow between entity classes and screens."* (line 3181)

The two senses: *"This data needs to find its way into the entity classes, which hold the values entered as attributes"* (3212), and conversely, the values of the entities are shown on the screen.

**The often overlooked operational statement** (3214): *"as you're tracing data flow between screens and entity classes, populate the class model with any missing attributes that are needed."* That is: the PDR **not only detects** missing attributes; It is time to populate them.

The GUI recipe uses `Screen | Field | Entity::attribute`; generalize it to `Interface | Input/output | Destination/source` for APIs, webhooks, message ingress, or device adapters. Trace domain data to appropriate attributes where relevant; transient inputs, derived values, and outputs need an explained source/destination, not an invented persistent domain attribute.

---

## #7 — Alternate courses, with their behavior

> *"Don't forget the alternate courses, and don't forget to write behavior for each of them when you find them."* (line 3182)

**The data that justifies the priority** (3224): the alternate courses *"generally account for more than half the complexity of a piece of software."*

**Enumeration is not enough** (3222): *"Identifying that an alternate course can happen is necessary, but not sufficient to complete your use case."* The exact behavior of the user and the system must be detailed.

**What counts as alternate** (3220): *"Alternate courses are not necessarily error paths but can include infrequent/atypical usage paths."* It's not just the error path.

**Consequence if omitted:** the classes will be born without the operations that manage those flows.

**Useful questions to find the missing ones:** What can go wrong in this step? · Are there any special conditions that change the flow? · Can the user leave here? Common categories: invalid data, connection timeout or loss, insufficient permissions, resource not found, user cancellation.

---

## #6 — Both sides of the dialogue

> *"Make sure each use case covers both sides of the dialogue between user and system."* (line 3183)

Rookie mistake: writing only what the user does and calling the use case done. A use case is a **dialog**; If the system doesn't respond in text, no one has specified what it does.

Automatable with heuristics: bursts of steps whose subject is only the actor, and flows without any response from the system.

---

## #5 — Correct robustness syntax

> *"Make sure you haven't violated the syntax rules for robustness analysis."* (line 3184; the same statement is repeated as a section header in 3234, with a different capitalization)

What to check: Actors connect **only** to Boundary objects; there is no noun-noun communication (Boundary-Entity, Boundary-Boundary, Entity-Entity) without a Controller in between.

**Why Controllers are not optional** (3239): *"The controllers represent the system behavior,"* so omitting them is, in the source's words, *"a very bad thing"*.

**Side advantage of syntax:** If a diagram cannot be expressed with these rules, the use case has an ambiguity or incompleteness problem. The syntax works as an early detector.

The detail of the nine connection rules lives in the sister skill `/mkl-uml-robustness-diagram`; here they are consumed, not redefined.

---

## #4 — Technical and nontechnical participants, in the same room

> *"Make sure that this review includes both nontechnical (customer, marketing team, etc.) and technical folks (programmers)."* (line 3185)

**What are the use cases after the PDR** (3251): *"Your use cases after robustness analysis should be treated as 'mini-contracts' between the clients and the programmers."* And the moment: *"It's during PDR that you finalize those contracts."*

**The right level of abstraction** (3253): each use case must reach *"the magic abstraction level—not vague and ambiguous, but not geek-speak—where everybody understands what the use case means…"* (the sentence continues in the original; it is cut here).

**In-session red flag:** If non-technical participants tune out, the material has probably entered detailed design territory.

Not automatable: it is verified in the session script and in the list of participants in the minutes.

---

## #3 — In the context of the object model and the GUI

> *"Make sure your use cases are in the context of the object model and in the context of the GUI."* (line 3186)

What "in context" means: human or machine interfaces have their own names, domain classes have a unique name, and actor roles have external participation evidence; there is no ambiguity about the referenced role, concept, or interface. These names have separate origins and are not all required in the domain model. From *"the search screen"* to a specific name; from *"the book object"* to `Book::isbn`, `Book::title`.

It is the practical mechanism by which the abstraction level of #4 is achieved.

The source adds (3259) that use cases should also be kept in the context of the evolving technical architecture, **without crossing over** into detailed design.

Partially automatable: generic screen names and vocabulary drift between artifacts.

---

## #2 — Do not drift towards detailed design

> *"Make sure your robustness diagrams (and the corresponding use case text) don't attempt to show the same level of detail that will be shown on the sequence diagrams"* (line 3187)

**The nature of the artifact** (3263): the robustness diagram *"represents an idealized, conceptual design, not the 'real software design.'"* And therefore: *"decisions related to allocating behavior among classes should not be made on robustness diagrams"* — *"These decisions are best deferred until you draw the sequence diagrams"* (3263).

**The two passes** (3265): *"[MKL] Process takes a two-pass approach to get to detailed design."* In the first, *"you intentionally ignore 'who's doing what' and focus on identifying objects, naming screens, and unambiguously describing behavior"*. In the second comes the problem of assigning behavior, *"how the methods are distributed among the classes"*.

Automatable in its two most visible symptoms: design pattern names in Controllers, and robustness diagrams that are actually sequence diagrams.

---

## #1 — The six steps

> *"Follow our 'six easy steps' to a better preliminary design (see Chapter 6)."* (line 3188)

For **each** robustness diagram under review (3267-3278), cited verbatim:

1. *"Make sure the diagram matches the use case text."*
2. *"Make sure the diagram follows the rules of robustness analysis."*
3. *"Check that the diagram focuses on the logical flow of the use case."*
4. *"Make sure the diagram shows all alternate courses of action for the use case."*
5. *"Watch out for 'design-pattern-itis' in the diagram."*
6. *"Check that the diagram isn't trying to be a detailed design."*

All six **add** the preceding guidelines to the individual diagram level: step 1 is #10, step 2 is #5, step 4 is #7, steps 5 and 6 are #2. Step 3—logical flow, not implementation—is the only one that does not have its own guide in the countdown.

**About "design-pattern-itis"** (3275): The source uses the term without defining it beyond this line. The operational reading we apply—Controllers named as GoF patterns, DAOs, repositories, or services instead of semantically named—is **our interpretation**, consistent with step 6 and guideline #2, and is marked as such in `anti-patterns.md`.

**Provenance of the six steps.** The footnote of the chapter itself (3280) attributes them to a previous book by Rosenberg & Scott that is **not in the corpus**. The quotes above are taken from the book that is there, where they are reproduced; The original work, which has not been read, is not cited.

---

## Position in the process and participants

**Where it fits** (826): the PDR *"is the 'gateway' between the preliminary design and detailed design stages, for each package of use cases."* It is the **Milestone 2 of 4**: Requirements Review → **PDR** → Detailed/Critical Design Review → Delivery.

**Why it exists** (822): *"In theory you should now be ready to start the detailed design, but in practice, it really helps to perform a quick Preliminary Design Review (PDR) first."*

**Who attends** (3153): *"The same group of people you had at the requirements review: customer representatives, the development team, and any managers"* closely involved. The question that introduces the answer is in 3151.

**Customer input ends here** (3153): *"this review is the last stage in the process where the customer has direct input."* Afterwards, the detailed design is up to the senior developers. The source clarifies (3155) that the client will be able to continue commenting on screens and work in progress; what ceases is its intervention on the design.

**If the client requests new requirements** (3157-3163): *"Then you're back to step 1 of the process (modifying use cases and the domain model, as needed)"* — and only for those requirements.

**Duration:** **NOT FOUND** in the corpus. The book does not give a figure for the PDR session. The time budgets this skill uses come from IEEE 1028 §6.5.2 and Wiegers, and are marked as such in `review-protocol.md`; they are not attributed to Rosenberg.

**After the PDR** (3416): *"Once the PDR is complete, you're ready to move on to the detailed design"*, and the technical architecture *"should also be reviewed during this session"* (3171-3173) to ensure that the design will work with the chosen architecture.

## Scope and interpretation

The quoted practitioner recipe is the full MKL preliminary-design review. Ordinary standalone checks use only the applicable evidence; the formal checklist is opt-in. “Two passes” here distinguishes preliminary object discovery from detailed behavior allocation, not two mandatory self-audits or a correctness guarantee. The actor/boundary/control connection matrix is an MKL convention, not a UML-wide prohibition. Entity closure concerns domain concepts only; boundary/interface and actor-role names trace to separate evidence.
