<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# The ten rules of the CDR

The core of the method. Each rule goes with its **verbatim quotation**, its **explanation**, **what satisfies it**, **what violates it** and **if it is automatable**.

Everything is transcribed here: applying this skill does not require opening the book. The line numbers are for auditing the quotation.

*Vocabulary: the book calls them* guidelines; *the course material calls them* **rules**, *and that is the term this skill uses.*

---

## Before the rules: the three objectives and the timing

**What the CDR aims to achieve** (4535-4539):

> *"The CDR helps you to achieve three important goals, before you begin coding: — Ensure that the "how" of detailed design matches up with the "what" specified in your requirements… — Review the quality of your design… — Check for continuity of messages."*

And the closing of the chapter repeats it as an exit criterion (4950-4956):

> *"the CDR involves three main goals: — Matching the use case text with its sequence diagram — Checking for continuity of messages — Reviewing for good design. If you've gone through the detailed design for each use case and reviewed it for these three criteria, then your design really should be **fighting-fit** now and easily ready for coding."*

The ten rules are the operationalization of those three objectives. If you ever doubt what a rule does, ask yourself which of the three it serves.

**When the review is convened** (4555-4557) — this is the entry criterion, developed in `review-protocol.md`:

> *"You need to have completed all of the sequence diagrams for the use cases that you're planning to implement in the current release. You should also have updated the class diagrams so that all of the operations that you assigned during sequence diagramming are reflected in the static model."*

**The precondition is in the previous chapter**, as rule #1 of that chapter's Top 10 (4035-4037): *"**Clean Up the Static Model Before Proceeding to the CDR.** Take a long, hard look at your static model… This should at least be done as a final step before proceeding to the CDR."* The exit rule of the detailed design is the entry criterion of the CDR: they fit together like a zipper.

---

## How to traverse the package — the checklist algorithm

There is no need to invent the order of the review. Chapter 11 of the same book explains how to build a review list in MKL, and it works the same here (6063, 6067):

> *"The high-level list of items to review should be based on the **use case titles**… it's better to drive the list from the use cases, as this provides for a more structured review."*
> *"Because the high-level checklist is essentially a list of use case titles, it's possible to drive the fine-grained list from the **controllers on the robustness diagrams**."*

**Two levels, derived from the material:**

- **Coarse traversal** = one use case per review cycle. It is also the natural unit to divide the package into sessions.
- **Fine traversal** = the robustness diagram controllers for that use case. Each controller is a logical function that must appear as a behavior in the sequence, as an operation in the model, and as a test case.

This explains why **robustness is an input to the CDR even though the CDR does not judge it**: it is not reviewed, it is used as an index.

And the chapter adds that the checklist must **grow** (6081): *"During code reviews, you tend to notice the same old issues again and again. Turning these into a checklist can save a lot of time… Over time, add to the list of checklists."* It coincides with what IEEE 1028 §6.9 requires.

---

## Rule 10 — The sequence matches the use case text

> *"Make sure the sequence diagram matches the use case text."* (4567)

**Explanation** (4580):

> *"During reviews, the **'highlighter test'** works exceptionally well (again). Highlight a sentence of use case text on the margin, and then highlight the messages that show the design for that bit of required behavior."*

The *"(again)"* matters: it is the same technique as the PDR, **repointed** from the robustness diagram to the sequence diagram.

**Procedure** (course material): select a phrase from the use case → search for messages that implement it → highlight both → repeat until all the text is covered. *"If the phrase does not have a clear representation in the diagram, there is a traceability problem."*

**Satisfied when:** each behavior phrase in the text has messages that realize it, and each message is explained by some phrase.
**Violation:** text without corresponding design (required behavior left undesigned), or design without corresponding text (invented behavior).

**Automatable: partial.** Vocabulary coverage between text and message labels can be measured, and flows declared without any messages can be detected. **What automation cannot do** is judge whether the pairing is *faithful*: just because the words match does not prove that the design does what the phrase asks for. That half is done by whoever reviews.

---

## Rule 9 — Basic and alternative courses

> *"Make sure (yes, again) that each sequence diagram accounts for both basic and alternate courses of action."* (4568)

**Full explanation** (4588-4590) — just one sentence, and it's the one that counts:

> *"Don't make the mistake of saying YAGNI about those pesky rainy-day scenarios."*

The course expands on it: *"Many teams model only the successful path. This is a mistake. Alternative scenarios usually contain much of the system's complexity."* And it lists the usual ones: unauthenticated user, invalid data, record not found, communication error, insufficient permissions.

**Satisfied when:** each `FA-XX` and each `FE-XX` in the specification has a fragment (`alt`, `opt`, `break`) or diagram of its own in the sequence.
**Violation:** a specified alternative flow that does not appear in the sequence.

**Automatable: yes.** It is comparing flow identifiers against fragments. It is one of the most reliable CDR checks.

---

## Rule 8 — Operations are well allocated

> *"Make sure that operations have been allocated to classes appropriately."* (4569)

**Explanation** (4592-4594): refers to *Responsibility-Driven Design* and gives a practical disambiguator:

> *"you can usually distinguish between operations on classes and messages that have just been labeled on the sequence diagram by looking for **parentheses '()'** following the operation name."*

**The reverse technique, which is the heart of the CDR** (4642-4648):

> *"A technique that works really well during the CDR is… using the class diagrams to find errors on the sequence diagrams. Basically, this involves the reviewer zooming in on various classes in the class diagram and looking for methods on the wrong classes, or other anomalies, and then finding the guilty sequence diagrams."*
> *"**You can find most sequence diagram errors by looking at the class diagram.**"*

**The canonical case** (4646):

> *"In a recent training workshop, Doug found a Queue class that had only an Add method. **Nobody was removing anything from the queue, ever!** Doug found the sequence diagram that was supposed to use the items from the queue and discovered that the message arrows were drawn backward—the Pull Item from Queue method had been put on the wrong class."*

Lesson: **an asymmetric class can reveal a reversed message arrow**. It adds without removing, or opens without closing. It is not fixed in the class model: it is fixed in the sequence.

**Satisfied when:** each significant operation in the selected scope has an Operation-signed call **directed to that class**, or a declared contract/design-delta origin. Behavior allocation also needs responsibility judgment. A UML reply maps original-call outputs, a Signal maps Signal/Reception semantics, and creation/deletion maps lifecycle behavior; none creates a reverse operation. See [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) §17.4.3 and the sequence skill's `notation-rules.md`.
**Violation:** a demonstrated mismatch between an operation and its originating call receiver, or unjustified provenance after checking selected scope and contracts. `Queue`-style asymmetry is only a review clue; it does not require an inverse operation or prove a reversed arrow.

**Automatable: partial**, comparing classified operation calls by receiver rather than against a global vocabulary pool. Unresolved sorts/signatures/receivers remain explicit gaps; lexical labels and asymmetry alone cannot establish the defect.

---

## Rule 7 — Appropriate attributes and operations

> *"Review the classes on your class diagrams to make sure they all have an appropriate set of attributes and operations."* (4570)

**Explanation** (4594, 4600, 4602):

> *"Follow the principles of Responsibility-Driven Design… and make sure each of your classes has a **cohesive, focused** set of operations."*
> **Tip:** *"**Look for classes without attributes and for classes with 'schizophrenic personalities' (i.e., unrelated sets of operations).**"*
> *"Sometimes you'll find that you've overloaded a class with too many responsibilities, or you may find that, once all the behavior allocation is done, some classes end up rather **impoverished, with no responsibilities**."*

And the rationale, quoted from Wirfs-Brock (4608): *"Responsibilities are meant to convey a sense of the purpose of an object and its place in the system."*

**The three warning signs**—the course names them that way—are:

1. **Empty class**: without attributes or operations. *"probably the design is incomplete."*
2. **Multiple personality**: unrelated operations, such as a `BookManager` with `saveBook()`, `deleteBook()`, `generateInvoice()`, `sendEmail()`, `calculateTaxes()`.
3. **Wrapper class**: only encapsulates another. See the rule at `anti-patterns.md`.

**And the three questions of the course for suspicious classes**, which serve as a procedure: does it have its own behavior? · does it just encapsulate another class? · Does it exist for technical or business reasons?

**About entities without attributes** (Tip 4912): *"You should identify attributes and add them to their classes during robustness analysis. You then put the functions where the data lives."*

**Satisfied when:** each class has cohesive responsibilities, and entities declare attributes to hold their data.
**Violation:** class without operations · entity without attributes · disparate operations in the same class · wrapper without its own responsibility.

**Automatable: partial.** Counting operations and attributes is trivial; **measuring cohesion is not**, because it requires understanding what each operation does. The validator counts and flags candidates; Deciding if a class has multiple personalities is done by the reviewer.

---

## Rule 6 — The real design, reflected

> *"If your design reflects the use of patterns or other detailed implementation constructs, make sure that these details are reflected on the sequence diagram."* (4571)

**Explanation** (4610-4612):

> *"the sequence diagram should show the **'real design' as you intend to code it**. **Magic is not permissible on sequence diagrams.**"*

The course calls it *magic functionality*: *"There should be no 'magic' functionality. All important behavior must appear explicitly."* The course's example: if the design uses a DAO, the DAO must be seen — with its interface and its implementation.

**Satisfied when:** The patterns and infrastructure that the code will have appear in the diagrams.
**Violation:** behavior that occurs without any message producing it · a pattern in the class model that no sequence required (and then the problem is the opposite: pattern without origin).

**Automatable: partial.** It is detected that a pattern named in the model does not appear in any sequence. **It is not detected** whether the pattern is *appropriate* — that is design judgment.

---

## Rule 5 — Map out the requirements

> *"Trace your functional (and nonfunctional) requirements to your use cases and classes to ensure you have covered them all."* (4572)

**The chain** shown in the course: `Requirement → Use Case → Sequence Diagram → Classes → Code`. *"If any connection disappears, there is a problem."*

And the questions that traceability should be able to answer: what requirement does this class implement? · what use case uses this operation? · What part of the design satisfies this requirement?

**Why it matters** (course): without traceability it is not known if functionality is missing, if there are excess components, or what breaks a change in requirements.

**Satisfied when:** each requirement reaches at least one class, and each class is explained by at least one requirement.
**Violation:** requirement without implementation (lack of functionality) or class without requirement (excess design). **Both directions matter** and are reported separately.

**Automatable: yes**, if there is a list of requirements. Without it the rule remains **not executed** and is declared — do not claim the rule was covered.

---

## Rule 4 — Programmers validate the design

> *"Make sure your programmers 'sanity check' the design and are confident they can build it and that it will work as intended."* (4573)

**Explanation** (4618-4620), in bold in the original:

> *"**Programmers need to be involved in detailed design.**"*

The questions that the course proposes: can this design be easily implemented? · Are there any technical limitations? · Will the solution have acceptable performance? · Are the patterns used appropriate?

The course's analogy, which gives the reason: *"Designing without consulting developers is similar to designing a building without talking to the engineers who will build it."*

**Automatable: NO, and this is final.** No automated check can replace confirmation from the developers who will implement the design. If no one with that role participated, the rule is declared **not executed** in the minutes. Falsely claiming coverage would be the worst possible failure of this skill: it is the only rule that provides information that no artifact contains.

---

## Rule 3 — Types, parameters and returns

> *"Make sure all your attributes are typed correctly, and that return values and parameter lists on your operations are complete and correct."* (4574)

**What the course adds, and is automatable**, on two fronts:

**Type precision.** Correct: `public Book load(int id)` — you know what you receive and what you return. Problematic: `public Object process(Object data)` — *"Lacks precision. Makes maintenance difficult. Generates ambiguity."*

**Names with intent.** Good ones: `loadBook()`, `calculatePrice()`, `saveReview()`. Bad: `doStuff()`, `process()`, `handle()`. *"Names must clearly express the intention."*

**Satisfied by:** every typed attribute, every operation with a declared return and typed parameters, and names that say what they do.
**Violation:** untyped attribute · operation without a declared return type · untyped parameters · `Object`/`var` as type · generic names.

**Automatable: yes**, and it is one of the cheapest and highest performing checks.

---

## Rule 2 — Generate headers and inspect them

> *"Generate the code headers for your classes, and inspect them closely."* (4575)

**Explanation** (4628):

> *"See, we told you that you were about to generate code. Once you've done so, **inspect the code headers carefully**."*

**Why it works** (course): when translating the design into code, questions arise that the diagram hides — is an attribute missing? Are there any parameters missing? Are there duplicate operations? Are there unnecessary dependencies? *"Many times errors appear immediately when trying to translate the design into code."*

**How this skill treats it:** generation is automated (`scripts/generate_code_headers.py`) when requested or included in already authorized work. Ask only if an unresolved scope choice remains; no mandatory re-confirmation. The inspection is done by whoever reviews. Headers are marked as **a review instrument, not production code** — see `traceability-and-headers.md`.

**Automatable: generation: yes; inspection: no.** It is exactly the division that the rule asks for.

---

## Rule 1 — Review the test plan

> *"Review the test plan for your release."* (4576)

**Explanation** (Tip of 4638) — and here is the precision that the statement does not reveal:

> *"Remember that you can generate (stub) test cases **for the controllers on your robustness diagrams** automatically… You can then collect these into a test plan."*

**The unit of verification is the robustness controller**, not the sequence message. That sets what to count: if a controller has no test case, there is a gap.

**Course questions:** Can each operation be tested? · Are alternative cases covered? · Can dependencies be isolated? · Is it possible to automate tests? The course's observation, which is the reason this rule closes the list: *"A design that is easy to test is usually more modular, more maintainable, less coupled. On the contrary, designs that are difficult to test usually hide structural problems."*

**Testing the design is the best way to review it.** That's why rule #1 is the last and highest in descending numbering.

**Automatable: partial.** Each controller and each alternative flow is checked to have a test case. **It is not checked** if the test case is good.

---

## Two more checks, from the development of the chapter

They are not numbered rules, but are explicit checks of the source and go into the validator.

**Object without messages** (4820-4846, *"Why Is 'Book' Unused on the Sequence Diagram?"*):

> *"If you find an object sitting all on its own on the sequence diagram, **without any messages being passed to it**, it's likely that you've discovered a part of the design that hasn't been thought through in sufficient detail."*

**Missing Multiplicities** (4864):

> *"At this stage of the design process, we really should have identified the multiplicity for all these kinds of relationships and added them onto the diagram."*

Note the nuance: in the **domain** model the multiplicities are optional; **not in the CDR anymore**, because the design is on its way to the code.

---

## Two warnings that avoid wasting time

**Do not polish the aesthetics** (Caution 4944):

> *"try not to spend hours tinkering with the layout until it's so tidy and symmetrical it could be mistaken for a map of midtown Manhattan."*

Close findings first; The pretty diagram with traceability gaps is useless.

**Look for stable abstractions** (box 4874-4886):

> *"**base the key abstractions in the code on true statements about the problem domain, because the problem domain winds up being the most stable**"*

It is the original of what the course calls *stable vs. unstable abstractions*: `Book`, `Customer`, `Order` survive the framework change; `Hibernate`, `SpringBookController` or `JdbcBookDao` no. A design organized around technology ages with it.

---

## When to stop detailing

The question that always appears in a CDR. The only substantive answer in the corpus is in *Agile Development (2005)* (4147-4151):

> *"If we reflect every last detail of the source code in the class diagrams and sequence diagrams, we'd still be finishing off the same diagrams in several years' time… Conversely, if we draw the diagrams at such an abstract level that they're largely meaningless, then that's not much use either. So finding the 'sweet spot'… is an important design skill."*

And the operational heuristic: *"every change we make to our design diagrams needs to be justifiable"*. If you can't say what a detail is for, it's unnecessary.

With an allocation of maintenance effort (4185): *"it's not necessary to redraw all the sequence diagrams. But **the static model (class diagrams) should be cleaned up**, and the classes in the model should match the classes in the code."* The static model is kept synchronized; updating every sequence is not required.

---

## Light mode

*Agile Development (2005)* relativizes rigor (3574):

> *"'Traditional' [MKL] Process uses the Critical Design Review (CDR) to make sure the design is specified at an appropriate level of detail that the code headers can be generated from the classes. **With a low-ceremony approach, the CDR might get skipped, or at least not be as rigorous.**"*

And it gives the criteria to decide it (3580): *"If the gap between the design and the code is large in one iteration, this should be an indicator to pay closer attention to CDR during the next release."*

That's why this skill has **modes**: the complete one executes the ten rules; the light one is limited to the automatable ones and **declares** those that it omits. Skipping checks without declaring them is an incomplete review, not a lightweight mode.

---

## Origin

Rosenberg & Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice*, chapter 9 (lines 4515-4964), with chapter 8 (4029-4037) for the precondition and chapter 11 (6042-6157) for the checklist algorithm. *Agile Development [abbreviated title]*, lines 3574-3580 and 4147-4197. Course material, *Session 09 — Critical Design Review*. Detail in `sources-and-methods.md`.
