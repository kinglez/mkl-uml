<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Notes on figures in the source corpus

The figures in the CDR chapter were examined individually. This file records **what each figure demonstrates** in words, because the images are not included in the package, but their substance must remain available.

---

## A warning that applies throughout this file

**The book's figures are a catalog of defects, rather than examples of correct models.**

This may seem surprising in the book that defines the method. Examining the figures makes the reason clear: the CDR chapter teaches **how to review** by presenting flawed designs and correcting them. Several figures showing the design “after the fix” **retain defects** named in the chapter's own Top 10.

**Do not copy them as examples of good design.** Their value lies elsewhere: they document real, published defects and explain why they are defects—excellent material for test fixtures.

**A note on captions.** An automated extractor generated the image filenames from nearby floating text, so **the filenames do not always describe the contents**. A file named *"book_is_devoid_of_all_responsibilities"* actually contained a refactored sequence diagram. The filename is unreliable; the descriptions below refer to what the images **contain**.

---

## The wrapper class—the chapter's best-documented defect

**What it shows.** A class model with `WriteCustomerReviewCommand` at the top, aggregating `Book`, `CustomerReview`, and `Customer`, with `WriteCustomerReviewController` depending on it.

`WriteCustomerReviewCommand` declares:

- Attributes `book: Book`, `customer: Customer`, and `customerReview: CustomerReview`
- Operations `getRating(): int`, `getReview(): String`, and `getTitle(): String`

An attached note in the diagram makes this evidence explicit:

> *"getRating(), getTitle() and getReview() are **wrapper methods around the CustomerReview properties**."*

`CustomerReview` declares `book: Book`, `customer: Customer`, `id: int`, `rating: int`, and `review: String`.

**What it demonstrates.** All three criteria for anti-pattern #10 are visible together: **X aggregates Y** · **X's attributes are a subset of Y's** (`book` and `customer` appear in both) · **all X's operations are delegating accessors** (as the note states). These criteria make automated detection possible instead of relying on intuition.

**Another visible defect:** **all attributes are public** (`+`) in all four classes.

---

## The refactored version still has defects

**What it shows.** The same model with the wrapper removed: `CustomerReview` is central; `Book` and `Customer` aggregate it with multiplicities `1`/`0..*`; and `WriteCustomerReviewController` depends on `CustomerReview`, with signatures `doSubmitAction(CustomerReview): void` and `formBackingObject(HttpServletRequest): CustomerReview`.

**What it demonstrates.** The refactoring achieves its purpose—one fewer class and clearer dependencies—**while the resulting model still exhibits three defects named in the Top 10**:

1. **All attributes are still public.**
2. **`CustomerReview` has five attributes and no operations**—a class without responsibilities, rule #7.
3. **`book: Book` and `customer: Customer` still duplicate the associations already drawn**—the same information appears twice.

**Lesson for this skill:** an artifact can improve and still fail the CDR. Correcting one finding does not close the others, and a figure in a book is not a certificate of correctness.

---

## The process map and the boundary guarded by the CDR

**What it shows.** Two dotted boxes. The **Dynamic** box contains `Use Case Model → Robustness Diagram → Sequence Diagram`, fed by a `GUI Storyboard`. The **Static** box contains `Domain Model → Updated Domain Model → Class Model`. Both boxes feed `Test Plans` on the right, and a red arrow leads from `Class Model` to `Code + Unit Tests`.

**What it demonstrates:**

- **Test plans draw on both sides**, rather than on the sequence alone. This confirms that the test plan is a required review input under rule #1.
- **The red `Class Model → Code` arrow is what the CDR authorizes or blocks.** It depicts the review gate's boundary.

**A comparison clarifies that boundary.** The same map appears in the **code review** chapter with one change: the arrow between `Class Model` and `Code + Unit Tests` is **bidirectional**. **The CDR authorizes the transition to implementation; resynchronizing the model with existing code is a separate, later activity** outside this skill's scope.

---

## Why the gate exists, shown quantitatively

**What it shows.** A chart with *Number of Discrepancies* on the vertical axis and *Time* on the horizontal axis over a release. Three lines: **Design** rises most steeply, **As-Built Code** rises more slowly, and the **Gap** between them **grows** over time.

**What it demonstrates.** Without a gate to reconcile design and implementation, they diverge, and the gap widens rather than stabilizing. This is the case for the CDR in a single image. The accompanying text also uses it to calibrate rigor: *"If the gap between the design and the code is large in one iteration, this should be an indicator to pay closer attention to CDR during the next release."*

---

## A design that satisfies rule #9

**What it shows.** A refactored sequence diagram for *Show Book Details*: `Dispatcher Servlet`, `BookDetailsController`, `Book`, and `ModelAndView`. `Book` is created as a command object (`command := new Book()`), receives `setId(id)`, and then `load()`.

It has two notes: *"book ID is extracted from URL"* and an alternate-course annotation **in red**—*"Alternate Course: Book ID not found…"*—with `throw BookNotFoundException` and `new("booknotfound")`.

**What it demonstrates.** Rule #9 is satisfied: the alternate path **is drawn**, rather than merely mentioned. It also illustrates the convention of highlighting alternate courses in color, consistent with `/mkl-uml-robustness-diagram`.

---

## Charts of review effectiveness

Three charts from the RITME study are transcribed with their numbers in `session-budget.md`. They show:

1. **Effectiveness versus document length.** A scatter plot falls from approximately 2.8 faults/page for documents shorter than 10 pages to approximately 0.2 for documents longer than 25. The decline is steep and begins early.
2. **Review speed versus length.** The same pattern: up to 15 min/page for short documents, and 1–2 min/page for documents longer than 25 pages. **This explains the first chart**—long documents are skimmed, rather than having fewer defects.
3. **Faults per page by subsystem.** Ten bars range from 2.4 to almost zero. Defect density **is not uniform**, which supports triage.

---

## The review cycle, illustrated

**What it shows.** A cycle with the stages `Prepare review → Review the software → Hold review meeting → Analyze measurements → Correct defects`, a return from `Correct defects` to `Repeat review`, and another from `Analyze measurements` to `Improve process`.

**What it demonstrates.** Two practices implemented by this skill: the **correct → review again** loop, represented by `Reinspect`, and the way **measurement analysis improves the process** as well as the product. IEEE 1028 §6.9 requires the latter; this skill implements it through the review self-check.

---

## Where the figures are located

**The skill does not require the images.** Their evidence is described above, and their defects are reconstructed as **executable** fixtures in `tests/examples/`, preserving the behavior that matters. Original-image locations are in `sources-and-methods.md`, the only file in this package containing source-corpus paths.
