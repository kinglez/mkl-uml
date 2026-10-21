<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Ten guidelines, four steps, and three goals

Primary source: Rosenberg & Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice*, chapter 8 (“Design and Coding”), corpus lines 3829-4368. Quotations are short and direct; line locators enable checking. Verification records are inherited from upstream research, not newly verified for this translation.

The source uses a **countdown**, with #1 most important. Its order is preserved.

---

## Ten guidelines

### #10 — Understand **why** you draw

> *"Understand **why** you're drawing a sequence diagram, to get the most out of it."* (3879)

The single reason is **allocating behavior to classes**. The chapter repeats it three times, once humorously: *"which is (repeat after us) allocation of behavior among collaborating objects"* (3988).

Its strongest sidebar (3911): **“DON'T TRY TO DRAW FLOWCHARTS ON SEQUENCE DIAGRAMS (FOCUS ON BEHAVIOR ALLOCATION INSTEAD)”**. Flowcharting *"simply misses the point of what you should be thinking about when you draw a sequence diagram"* (3915). The UML 2.0 notation appendix reiterates this (8282).

### #9 — One diagram per use case, all courses included

> *"Draw a sequence diagram for every use case, with both basic and alternate courses on the same diagram."* (3880)

**On the same diagram**, not separate diagrams—the same requirement as robustness analysis.

### #8 — Start where robustness ended

> *"Start your sequence diagram from the boundary classes, entity classes, actors, and use case text that result from robustness analysis."* (3881)

In the full MKL recipe these inputs come from `DR-XX` and text. For independent sequence work, use equivalent supplied participants, interface/domain evidence, and scenario text; record missing provenance without fabricating an upstream artifact.

### #7 — Show objects accomplishing behavior

> *"Use the sequence diagram to show how the behavior of the use case (i.e., all the controllers from the robustness diagram) is accomplished by the objects."* (3883)

The parenthesis is central: **use case behavior *is* the robustness Controllers**. Their list becomes the allocation worklist.

### #6 — Map text to messages

> *"Make sure your use case text maps to the messages being passed on the sequence diagram. Try to line up the text and message arrows."* (3884)

Apply the PDR *highlighter test*: walk the text and mark each corresponding message. **Visual alignment** makes checking inexpensive.

### #5 — Do not overinvest in focus of control

> *"Don't spend too much time worrying about focus of control."* (3885)

See `notation-rules.md` for all three positions. The source prefers omission: *"the focus of control is best switched off, as it tends to be something of a distraction"* (3871), and *"If focus of control starts to become a distraction, the easiest thing to do is just switch it off"* (3990). It explicitly says showing it **is not an error**: *"this isn't necessarily an error, as some people do prefer to show these"* (4451).

### #4 — Allocate operations while drawing messages

> *"Assign operations to classes while drawing messages."* (3886)

**For operation calls, allocate while drawing, not afterward.** The source says *"in UML each message is also called an operation once it's assigned to a class"* (3907). This is practitioner shorthand for call-oriented design; UML also has replies, signals, and lifecycle messages. Apply the message-sort distinctions in `notation-rules.md` before adding any operation.

### #3 — Review class diagrams frequently

> *"Review your class diagrams frequently while you're assigning operations to classes, to make sure all the operations are on the appropriate classes."* (3887)

Operational form (4280): *"with each message arrow you draw on the sequence diagram, you take a peek at the class diagram to make sure it's updated correctly"*. Add missing attributes as soon as you notice them.

### #2 — Prefactor before coding

> *"**Prefactor** your design on sequence diagrams before coding."* (3888)

Refactoring models is cheaper than refactoring code. The companion book calls it *"model refactoring: iterating through various design possibilities until we zero in on the design"*. It is faster *"because there are no unit tests to write and rewrite, and no source code to slow us down (yet)"*.

### #1 — Clean up the static model before CDR

> *"Clean up the static model before proceeding to the CDR."* (3889)

**Critical Design Review** (Milestone 3) follows, with its own Top 10 at 4563-4576. Apply a useful review technique already: *"Using the Class Diagrams to Find Errors on the Sequence Diagrams"* (4642); *"You can find most sequence diagram errors by looking at the class diagram"* (4648). A class with one nonsensical operation or twenty unrelated operations points to a sequence defect.

---

## Four essential steps

Heading at 4061. Explicit effort allocation (4065):

> *"The first three steps are completely mechanical in nature. This means they can be automated… The fourth step, **deciding which methods go on which classes**, is really what sequence diagramming is all about."*

| Step | Action | Nature |
|---|---|---|
| 1 | *"Copy the Use Case Text Straight into the Diagram"* (4081) | Mechanical |
| 2 | *"Copy the Entity Objects from the Robustness Diagram"* (4105) | Mechanical |
| 3 | *"Copy the Boundary Objects and Actors from the Robustness Diagram"* (4123) | Mechanical |
| 4 | *"Assign Operations to Your Classes"* (4149)—*"This step is where the real decision-making takes place"* | **Judgment** |

The authors automated the first three with a skeleton-generation script (4077), confirming this reading.

Step 4 divides into *"Converting the Controllers from Your Robustness Diagram"* (4169) and *"Deciding Which Controllers to Assign to Which Classes"* (4185): responsibility-driven allocation, explained in `behavior-allocation.md`.

**Book note (4069):** *"In Chapter 12, we extend these steps to show how to systematically build a suite of test cases at the same time as your sequence diagrams"*. `CP-XX` belongs to the same pass, not a later stage. See `test-derivation.md`.

---

## Three goals

Verbatim headings, 3901-3903:

1. *"Allocate behavior to your classes"*
2. *"Show in detail how your classes interact with each other over the lifetime of the use case"*
3. *"Finalize the distribution of operations among classes"*

Summary (3917): *"In [MKL] Process, the primary purpose of the sequence diagram is to make this behavior allocation visible so that you get it right."*

---

## Controller transformation

The most misunderstood part, stated precisely at 3865:

> *"there are **no controller objects on the sequence diagram** (although there could be)"*
> *"the controllers (the verbs) are turned into messages on the boundary and entity objects (the nouns)"*
> *"80% or so of the controllers from the robustness diagrams can be implemented as one or more operations on the entity and boundary classes"*

Repeated at 3938 (*"controllers will map to messages between objects on the sequence diagram"*) and 3901 (*"Often, a controller turns into two or more operations"*, *"occasionally a controller may also be turned into a controller class"*). The worked example adds (4177): *"every now and then it makes sense to turn a controller into a full-fledged control class"*.

**Three operational readings:**

1. **No one-to-one mapping.** A Controller yields **one or several** operations; verify **coverage**, never matching counts.
2. **Controller classes account for the remaining 20%**, with concrete roles such as managers/dispatchers.
3. **Framework warning**, also at 3865: *"sometimes a framework might tempt you to litter your design with dozens of tiny 'controller classes'"*. A controller and service per entity is not object-oriented design.

---

## Convergence of two spaces

“Updating Your Class Diagrams As You Go Along” (4270), and “Synchronizing the Static and Dynamic Parts of the Model”:

> *"don't be surprised if you start to see lots of new classes appear on the static model that were never there on the domain model during analysis. That's because you're now identifying the solution space classes. By contrast, the domain model shows classes only from the problem space."* (4284)

> *"The two spaces are now converging during detailed design. By updating the static model as you work through the sequence diagrams, you're now converging the problem space with the solution space."* (4286)

**Consequence:** a new solution-space class **is not a traceability defect**. Record this expected design result in the delta. A **domain entity** absent from the domain is a finding: it was discovered late or its name drifted.

Also watch for (4282) generalization opportunities, useful patterns, and classes with excessive responsibilities that **need splitting**.

---

## Source-named anti-patterns

Three named solved exercises (4405-4463), detailed in `anti-patterns.md`:

| Exercise | Name | Defect |
|---|---|---|
| 8-1 | *"Non-OO Behavior Allocation"* (4405) | Message sent to the wrong object rather than the responsible class |
| 8-2 | *"Flowcharting"* (4423) | *"the sequence diagram is being used as a flowchart, instead of for its primary purpose in life"* (4425) |
| 8-3 | *"Plumbing"* (4441) | Missing infrastructure creates *"leaps of logic"*; *"it's probable that a part of the design has been missed"* (4453) |

## UML message semantics and operation provenance

The practitioner quotations below describe a call-centered design recipe, not a UML equivalence between Message and Operation. Apply the distinctions in [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) §17.4.3 and §17.12.18:

| Message sort | Trace to | Class-model consequence |
|---|---|---|
| `synchCall` / `asynchCall` with an Operation signature | The invoked operation of the receiving lifeline's classifier | Check or allocate that receiving-class operation; call arguments map to `in`/`inout` parameters |
| `reply` | The original synchronous call and its operation | Check its `out`/`inout`/`return` values; do **not** invent an operation on the reply receiver |
| `asynchSignal` with a Signal signature | Signal and the receiver's reception/handling responsibility | Model the Signal and any applicable Reception; no operation follows merely from the signal arrow |
| `createMessage` / `deleteMessage` | Instance creation/destruction and lifecycle evidence | Trace lifecycle behavior; no ordinary receiver operation is implied |
| Unspecified or ambiguous sort/signature | Explicit unresolved semantic classification | Report the gap; do not guess a call or create a reverse operation |

A reply label such as `result`, `ok`, or `receipt` names returned information, not a callable operation. A dashed/open arrow alone may be ambiguous in a rendering tool: use declared message intent and signature as evidence. A self-call follows the same call/signature rule. UML's `MessageKind` (`complete`, `lost`, `found`, `unknown`) describes available message ends; it is distinct from `MessageSort`. Neither an unknown end nor an ambiguous label licenses invented behavior. A known call with an unresolved receiver stays an unresolved allocation.

MKL requires provenance for modeled significant operations within the selected behavioral scope. This is a modeling convention, not a UML requirement that every operation of a classifier appear in one selected interaction. Declared framework/interface contracts and justified design deltas are separate origins, with their limits stated. Lexical matching is a candidate check and cannot prove semantic equivalence.

