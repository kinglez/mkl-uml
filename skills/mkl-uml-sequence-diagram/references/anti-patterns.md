<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sequence diagram anti-patterns

A catalog for review, refactoring, and audit: **symptom → why it matters → correction → recipient**. The recipient is the skill owning the defective artifact, or this skill for design defects.

Three entries are **named by the source** (solved exercises 8-1, 8-2, 8-3); the others derive from explicit method or notation rules.

---

## Purpose failures: three source-named patterns

### 1. Disguised flowchart (*Flowcharting*)

**Symptom.** Decisions, loops, and algorithm steps dominate, but most messages begin and end on the same participant. Little collaboration; the actor often disappears after the first message.

**Why it matters.** Algorithm detail can obscure the collaboration and responsibility decisions this artifact is meant to explain (Rosenberg & Stephens, chapter 8; Fowler, chapter 4).

**Correction.** Ask **which class should be responsible** for each step and redraw collaboration. If nearly everything belongs to one class, consider #3.

**Recipient:** this skill (redesign).

### 2. Non-OO Behavior Allocation

**Symptom.** Messages target objects lacking the data needed by the operation. Typically, a controller retrieves all entity data and processes it itself.

**Why it matters.** Behavior becomes distant from knowledge; each entity-structure change forces controller changes.

**Correction.** Move behavior to the class with the information. An operation needing three attributes from another class usually belongs there.

**Recipient:** this skill.

### 3. Missing *Plumbing*

**Symptom.** Significant results have no modeled collaboration or declared contract explaining how they occur.

**Why it matters.** An unexplained integration or persistence effect leaves implementation work and assumptions unresolved.

**Correction.** Add missing infrastructure. Detailed design **does** allow architecture/storage objects; omission conceals rather than simplifies.

**Opposite risk:** adding plumbing before domain behavior is allocated produces #6.

**Recipient:** this skill.

---

## Behavior-allocation failures

### 4. Centralized control

**Symptom.** One lifeline sends nearly all messages while others only return data.

**Why it matters.** Excessive central processing can make one participant depend on many collaborators' internal state. Inspect whether delegation would localize change and preserve invariants (Fowler, chapter 4).

**Correction.** For each dominant-participant message, ask whether the target can own that work; move what can move.

**Caveat.** Centralized coordination can be legitimate or framework-required. The validator uses a **threshold warning**, not an error.

**Recipient:** this skill.

### 5. Anemic domain model

**Symptom.** Entities receive only `get`/`set`; controllers/services own all logic. Domain classes are named data structures.

**Why it matters.** Accumulated #4/#2 defects separate data from behavior and turn object-oriented design into functional decomposition.

**Review prompt:** repeated controller/service pairs for each Entity may reflect framework scaffolding rather than a deliberate distribution of domain responsibility. Confirm the actual contract before treating that pattern as defective.

**Correction.** Return state-dependent operations to each Entity: self-validation, derived-value calculation, invariant decisions.

**Recipient:** this skill and the class-model operation delta.

### 6. Premature implementation detail

**Symptom.** Full signatures, concrete types, framework method names, sessions, transactions, or caches appear before domain behavior is allocated.

**Why it matters.** Detailed design is not code. Infrastructure introduced **before** problem-behavior decisions buries them under plumbing.

**Correction.** Allocate domain behavior first; then add the required infrastructure.

**Recipient:** this skill.

### 7. Message chain

**Symptom.** A participant requests an object, asks it for another, then operates on that third object.

**Why it matters.** The sender depends on others' internal object structure, which may expose unnecessary structural coupling. This needs semantic review, not a graph-only conclusion.

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

**Why it matters.** Repeated uninformative replies obscure the outputs and decisions that matter to the selected interaction.

**Correction.** Keep meaningful synchronous replies addressed to their original caller. Model asynchronous completion as a separate callback call or Signal with its own semantics. Follow [notation-rules.md](notation-rules.md) for message-sort classification.

**Recipient:** this skill.

### 16. Unnecessary activation bars

**Symptom.** Unrequested `activate`/`deactivate` commands.

**Why it matters.** This profile omits unrequested activation detail for readability. Presence alone is a style choice; structural balance remains independently checkable.

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

**Why it matters.** Nested branches multiply review paths and can make the selected collaboration difficult to inspect. Depth is a local warning heuristic, not proof that the behavior is wrong.

**Correction.** Usually **split the use case**, rather than shrink the diagram.

**Recipient:** `/mkl-use-case-specifier`.

### 19. Oversized diagram

**Symptom.** Dozens of participants/messages, unreadable in one view.

**Why it matters.** When participants and messages cannot be read together, reviewers lose the relationships needed to assess responsibility and outcomes.

**Correction.** Split the use case; never shrink the font.

**Recipient:** `/mkl-use-case-specifier`.
