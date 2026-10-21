<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# The static model: convergence, cleanup, and the next gate

Short direct quotations with corpus-file line locators for verification.

---

## Convergence of the two spaces

**Rosenberg & Stephens, 4284:**

> *"don't be surprised if you start to see lots of new classes appear on the static model that were never there on the domain model during analysis. That's because you're now identifying the solution space classes. By contrast, the domain model shows classes only from the problem space."*

**4286**, emphasized in the book:

> *"The two spaces are now converging during detailed design."*

**Agile Development (2005)** contrasts this with the domain artifact: *"The static model is the grittier, more detailed version of the domain model, and it contains more implementation details."* It explicitly **keeps the diagrams separate**:

> *"The domain model reflects our current understanding of the business domain (i.e., it's an analysis-level artifact), whereas the fleshed-out class diagrams … are collectively a detailed design artifact."*

This separation is why the skill creates a new file instead of editing the domain model.

---

## Synchronize while drawing, not at the end

**4280:** *"with each message arrow you draw on the sequence diagram, you take a peek at the class diagram to make sure it's updated correctly."*

**4282:** *"It's a good habit to check that the operations are added to the correct class each time you draw a message"*, and *"if you spot any missing attributes, add them as soon as you notice they're missing."*

The same line identifies **three design opportunities** to seek actively during synchronization:

> *"You might spot an opportunity for generalization, for example; you may see a possible use of a design pattern"* … *"a class has gained too many responsibilities and needs to be split in two using aggregation."*

**Agile Development (2005)** gives the ideal chain: *"the operations on the classes on the static model should have gotten there by message arrows drawn on sequence diagrams, and the source code headers should have been generated from these class diagrams."*

---

## Clean up before the CDR

Sequence guideline **#1** explains “cleanup”:

> *"tidying up the design, resolving real-world design issues, identifying useful design patterns that can be factored in to improve the design"*

The list, verbatim:

- *"Using infrastructure/scaffolding classes"*
- *"Using design patterns"*
- *"Meshing the design with application frameworks"*
- *"Completing parameter lists on operations"*

The framing: *"plan on finalizing your class model during detailed design"*, while allowing *"draw the sequence diagram at a slightly simplified level and then finalize the class model in the coding environment"*.

**Presentation caution:** *"try not to spend hours tinkering with the layout"*. Diagrams are *"about showing a structural overview of the code you're about to write"*.

---

## Model refactoring

**Agile Development (2005)** distinguishes it from code refactoring:

> *"Model refactoring means changing the design at the object modeling stage, prior to coding, without changing the functionality."*

Scope and drivers:

> *"Model refactoring affects the class diagrams (i.e., the structure of the code) and is driven by both the robustness diagram and the sequence diagram."*

The stated goal—**prefactoring**—is *"getting the factoring of methods to classes right the first time instead of relying on refactoring"*, which *"minimizes the need for Constant Refactoring After Programming"*. Rosenberg supplies the economic rationale: *"Prefactoring your design on sequence diagrams saves massive amounts of refactoring after code."*

The Agile Development (2005) worked example states: *"this is the essence of model refactoring: iterating through various design possibilities until we zero in on the design that works for everyone involved."*

**Shortcut warning:** *"myopically Doing The Simplest Thing That Could Possibly Work … will almost always generate the need for massive amounts of refactoring"*.

---

## CDR: the next gate and this artifact's assessment criteria

**Milestone 3**, chapter 9 (4521-4963). The CDR is a separate sibling skill; its criteria define what this model must satisfy.

**Entry criterion, 4557:**

> *"You should also have updated the class diagrams so that all of the operations that you assigned during sequence diagramming are reflected in the static model."*

**Attendees, 4545**, unlike PDR: *"the customer should not be involved in the CDR—just the designers and developers."*

**Ten guidelines** (4567-4576), in the book's countdown order. Directly applicable items are marked:

| # | Guideline | Applies to class model? |
|---|---|---|
| 10 | *"Make sure the sequence diagram matches the use case text."* | No |
| 9 | *"Make sure (yes, again) that each sequence diagram accounts for both basic and alternate courses of action."* | No |
| 8 | *"Make sure that operations have been allocated to classes appropriately."* | **Yes** |
| 7 | *"Review the classes on your class diagrams to make sure they all have an appropriate set of attributes and operations."* | **Yes** |
| 6 | *"If your design reflects the use of patterns or other detailed implementation constructs, make sure that these details are reflected on the sequence diagram."* | Partial |
| 5 | *"Trace your functional (and nonfunctional) requirements to your use cases and classes to ensure you have covered them all."* | **Yes** |
| 4 | *"Make sure your programmers 'sanity check' the design and are confident they can build it and that it will work as intended."* | Partial |
| 3 | *"Make sure all your attributes are typed correctly, and that return values and parameter lists on your operations are complete and correct."* | **Yes** |
| 2 | *"Generate the code headers for your classes, and inspect them closely."* | **Yes** |
| 1 | *"Review the test plan for your release."* | No |

**Especially relevant elaborations:**

- #8: *"make sure each of your classes has a cohesive, focused set of operations"*. Identify actual operations by *"the parentheses '()' following the operation name"*.
- #7: *"continuously bounce back and forth between the sequence diagram and a detailed class diagram that shows all the attributes and operations"*. Diagnostic test: *"Look for classes without attributes and for classes with 'schizophrenic personalities' (i.e., unrelated sets of operations)"*, and the opposite defect, classes *"rather impoverished, with no responsibilities"*.
- #6: *"Magic is not permissible on sequence diagrams."*
- #4, in bold: *"Programmers need to be involved in detailed design."*

**Duplicate note:** the same list appears in chapter 1 (890-899) with minor wording differences. Chapter 9 is canonical here.

---

## Reverse technique: find sequence errors by inspecting classes

Section 4642-4648 runs in the opposite direction to the pipeline:

> *"this involves the reviewer zooming in on various classes in the class diagram and looking for methods on the wrong classes, or other anomalies."*

The workshop anecdote (4646): *"a Queue class that had only an Add method. Nobody was removing anything from the queue, ever!"* The remove method was on the wrong class because arrows had been reversed.

The strong claim (4648): *"You can find most sequence diagram errors by looking at the class diagram."*

**Use here:** asymmetric operations—adds without removes, opens without closes—are clues for checking scope and responsibility. They do not prove a misdirected call or mandate an inverse operation. Confirm message sort/signature and actual receiver before reporting a mismatch; replies, Signals, and lifecycle messages have separate semantics.

---

## After the CDR

Chapter 11 is **Code Review and Model Update**. Guideline #1 (6055) captures the intent: *"Remember that it's also a Model Update session, not just a Code Review."*

Agile Development (2005)'s maintenance rule (4185): *"it's not necessary to redraw all the sequence diagrams. But the static model (class diagrams) should be cleaned up, and the classes in the model should match the classes in the code."*

**Consequence:** the class model is the **persistent** design artifact. Once code is written, sequence diagrams *"have served their purpose"*. This output outlives the rest of the pipeline, another reason to require provenance for every element.

## Scope of the call-oriented recipe

The quoted “each message arrow” instructions describe practitioner synchronization of operation calls. For UML `synchCall`/`asynchCall`, trace the invoked Operation to the receiving classifier; for `reply`, trace the original call's outputs; for `asynchSignal`, trace the Signal and applicable Reception; for `createMessage`/`deleteMessage`, trace lifecycle behavior. Unknown or ambiguous sorts/signatures remain unresolved. Never create a reply-receiver operation merely to make labels match. See [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) §17.4.3 and `provenance-rules.md`.
