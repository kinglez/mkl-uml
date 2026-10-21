<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sequence diagram anti-patterns

A catalog for review, refactoring, and audit: **symptom → why it matters → correction → recipient**. The recipient is the skill owning the defective artifact, or this skill for design defects.

Three entries are **named by the source** (solved exercises 8-1, 8-2, 8-3); the others derive from explicit method or notation rules.

---

## Purpose failures: three source-named patterns

### 1. Disguised flowchart (*Flowcharting*)

**Symptom.** Decisions, loops, and algorithm steps dominate, but most messages begin and end on the same participant. Little collaboration; the actor often disappears after the first message.

**Why it matters.** *"the sequence diagram is being used as a flowchart, instead of for its primary purpose in life"*. Flowcharts do not allocate behavior to classes, the purpose of this artifact. Fowler: *"Treat sequence diagrams as a visualization of how objects interact rather than as a way of modeling control logic."*

**Correction.** Ask **which class should be responsible** for each step and redraw collaboration. If nearly everything belongs to one class, consider #3.

**Recipient:** this skill (redesign).

### 2. Non-OO Behavior Allocation

**Symptom.** Messages target objects lacking the data needed by the operation. Typically, a controller retrieves all entity data and processes it itself.

**Why it matters.** Behavior becomes distant from knowledge; each entity-structure change forces controller changes.

**Correction.** Move behavior to the class with the information. An operation needing three attributes from another class usually belongs there.

**Recipient:** this skill.

### 3. Missing *Plumbing*

**Symptom.** Unexplained results and missing persistence, external-service, or session participants create *"leaps of logic"*.

**Why it matters.** *"it's probable that a part of the design has been missed"*. Undesigned, unestimated work emerges during implementation.

**Correction.** Add missing infrastructure. Detailed design **does** allow architecture/storage objects; omission conceals rather than simplifies.

**Opposite risk:** adding plumbing before domain behavior is allocated produces #6.

**Recipient:** this skill.

---

## Behavior-allocation failures

### 4. Centralized control

**Symptom.** One lifeline sends nearly all messages while others only return data.

**Why it matters.** Fowler favors distributed processing: *"One of the main goals of good design is to localize the effects of change"*; *"by distributing control, you create more opportunities for using polymorphism rather than using conditional logic"*.

**Correction.** For each dominant-participant message, ask whether the target can own that work; move what can move.

**Caveat.** Centralized coordination can be legitimate or framework-required. The validator uses a **threshold warning**, not an error.

**Recipient:** this skill.

### 5. Anemic domain model

**Symptom.** Entities receive only `get`/`set`; controllers/services own all logic. Domain classes are named data structures.

**Why it matters.** Accumulated #4/#2 defects separate data from behavior and turn object-oriented design into functional decomposition.

**Early source warning:** a framework *"might tempt you to litter your design with dozens of tiny 'controller classes'"*. An `XController` and `XService` per entity follows that path.

**Correction.** Return state-dependent operations to each Entity: self-validation, derived-value calculation, invariant decisions.

**Recipient:** this skill and the class-model operation delta.

### 6. Premature implementation detail

**Symptom.** Full signatures, concrete types, framework method names, sessions, transactions, or caches appear before domain behavior is allocated.

**Why it matters.** Detailed design is not code. Infrastructure introduced **before** problem-behavior decisions buries them under plumbing.

**Correction.** Allocate domain behavior first; then add the required infrastructure.

**Recipient:** this skill.

### 7. Message chain

**Symptom.** A participant requests an object, asks it for another, then operates on that third object.

**Why it matters.** The sender depends on others' internal object structure, violating “talk only to immediate neighbors.”

**Correction.** Request a service rather than an object; let the neighbor perform or delegate it.

**Recipient:** this skill.

### 8. Diagram never progressed beyond robustness

**Symptom.** Participants match `DR-XX`, and messages reproduce Controllers one to one without new decisions.

**Why it matters.** Mechanical steps 1–3 ran; **step 4 did not**. Changing notation alone does not allocate behavior.

**Distinguishing real design:** some Controllers split into operations, some gain receiver-specific names, a few become classes. Perfect one-to-one correspondence is the warning.

**Correction.** Decide **which class** receives each Controller's operation and why.

**Recipient:** this skill.

---

## Traceability failures

### 9. Uncovered Controller

**Symptom.** A `DR-XX` Controller appears neither as message nor participant in `DS-XX`.

**Why it matters.** Design lost behavior identified during analysis. Guideline #7 equates use case behavior with robustness Controllers.

**Correction.** Allocate it, or justify removal, for example an analysis duplicate.

**Recipient:** this skill; `/mkl-uml-robustness-diagram` for an unnecessary Controller.

### 10. Alternate flow without fragment

**Symptom.** A specification `FA-XX`/`FE-XX` has no diagram fragment.

**Why it matters.** Guideline #9 requires basic **and all alternate courses together**. Undesigned alternatives risk omission from implementation.

**Correction.** Add a fragment labeled with its identifier.

**Detection caveat:** normalize `FA-01`, `FA1`, `FA 1`; exact-spelling checks silently miss valid variants.

**Recipient:** this skill; `/mkl-use-case-specifier` if the alternative is invalid.

### 11. Orphan participant

**Symptom.** A declared lifeline sends/receives no messages.

**Why it matters.** Either it is unnecessary or its behavior is missing. A sequence participant exists **because it participates**.

**Correction.** Connect or remove it.

**Recipient:** this skill.

### 12. Actor bypasses boundaries

**Symptom.** Actor messages a Controller, Entity, or infrastructure.

**Why it matters.** In the MKL layered recipe actors interact through Boundary roles. A bypass may reveal a missing human or machine interface (API, webhook, message ingress, device adapter); it does not prove a screen is missing. This is an architectural modeling convention, not a UML-wide ban on such messages.

**Correction.** Insert the appropriate Boundary.

**Recipient:** this skill; `/mkl-uml-robustness-diagram` if `DR-XX` also lacks it.

### 13. Infrastructure declared as Entity

**Symptom.** `entity "ORM"`, `entity "Database"`, `entity "HTTPClient"`.

**Why it matters.** `entity` means **domain-model** class. Mislabeling corrupts vocabulary and makes the domain check search for nonexistent `ORM` concepts.

**Correction.** Use `participant`, `database`, or `queue` and an infrastructure prefix.

**Recipient:** this skill.

### 14. Silent renaming between artifacts

**Symptom.** A `DR-XX` participant appears under a different name.

**Why it matters.** Traceability breaks and identity versus novelty becomes unclear.

**Correction.** Preserve the upstream name, or declare a finding so the change propagates backward.

**Recipient:** `/mkl-uml-robustness-diagram` or `/mkl-uml-domain-modeler`, whichever owns the vocabulary.

---

## Notation failures and noise

### 15. Excessive returns (*returnitis*)

**Symptom.** Every synchronous call has a dashed return even when its value is unused.

**Why it matters.** All sources omit unnecessary returns. Rosenberg notes values can pass as arguments; Fowler: *"otherwise, they simply clutter things"*. Twice the arrows does not mean twice the information.

**Correction.** Keep returns for later-used values, asynchronous results, and error branches.

**Recipient:** this skill.

### 16. Unnecessary activation bars

**Symptom.** Unrequested `activate`/`deactivate` commands.

**Why it matters.** Course material requires omission; Rosenberg prefers it. **Presence is not an error**, merely *"a matter of personal taste"*. Warn only when unrequested.

**Correction.** Remove or explicitly declare the choice.

**Serious variant: activation leak.** Unmatched activation **on any execution path** is a structural defect. Enumerate paths because each `alt` branch closes independently.

**Recipient:** this skill.

### 17. Redundant stereotype in label

**Symptom.** `boundary "Screen X\n<<boundary>>"`.

**Why it matters.** PlantUML already draws the stereotype icon. Repetition clutters the real name and complicates comparison with `DR-XX`.

**Correction.** Keep only the name.

**Recipient:** this skill.

### 18. Overnested fragments

**Symptom.** Three or more levels, such as `alt` inside `opt` inside `loop`.

**Why it matters.** Fowler calls frames *"very heavy, obscuring the main point of the diagram"*. Nesting multiplies execution paths and prevents readable, manual verification.

**Correction.** Usually **split the use case**, rather than shrink the diagram.

**Recipient:** `/mkl-use-case-specifier`.

### 19. Oversized diagram

**Symptom.** Dozens of participants/messages, unreadable in one view.

**Why it matters.** Sequence diagrams *"are densely packed with information, which can make them as difficult to read as to draw"*. Beyond a certain size they cease to help.

**Correction.** Split the use case; never shrink the font.

**Recipient:** `/mkl-use-case-specifier`.
