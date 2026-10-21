<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Traceability and headers — the two instruments towards the code

Rules #5 and #2 share a purpose: to check that the design **gets** to the code without gaps. The first verifies it backwards; the second, forward.

---

# Part 1 · The traceability matrix (rule #5)

> *"Trace your functional (and nonfunctional) requirements to your use cases and classes to ensure you have covered them all."* — Rosenberg, 4572

## The chain

The course draws it like this, and it is the complete pipeline:

```
Requirement → Use Case → Sequence Diagram → Classes → Code
```

*"If any connection disappears, there is a problem."*

In package identifiers: `RF-XX → CU-XX → DS-XX → MC-XX → CP-XX`.

## The three questions you should be able to answer

From the course material, and they are the criterion of whether the matrix is useful:

1. What requirement does this class implement?
2. Which use case uses this operation?
3. What part of the design satisfies this requirement?

The matrix is incomplete if it cannot answer any of these questions.

## How to build

One row per requirement, with columns for the traceability chain. It is filled **from both ends**, not just from the top: going through only requirement→class finds what is missing, but not what is left over.

| `RF-XX` | `CU-XX` | `DS-XX` | Classes and operations | `CP-XX` |
|---|---|---|---|---|
| The requirement, cited | Use cases that realize it | Sequences | Where the behavior lives | How to verify |

## The two gaps, which are different defects

| Gap | What does it mean | Recipient |
|---|---|---|
| **Requirement without a class** | **Functionality is missing.** Something was requested that the design does not implement | `/mkl-use-case-specifier` if use case is missing; `/mkl-uml-sequence-diagram` if behavior is missing |
| **Class without requirement** | **The design contains an unjustified element**, or there is an implicit unwritten requirement | `/mkl-uml-design-class-model`, or `/mkl-use-case-specifier` if the requirement exists but is not documented |

**The second is often overlooked and is usually the most informative.** A class that no one asked for may be legitimate scaffolding—so it is marked `<<solucion>>`—or it may be a requirement that someone knew about and never wrote about. The authentication example in the course material is exactly that: the design needed it, no one had specified it.

## Non-functional requirements

The rule says *"functional (and nonfunctional)"*, and nonfunctional requirements are the hardest to trace: performance, security or auditing rarely fall into a specific class. **They map to design decisions**, not classes: what part of the design responds to this requirement. If none, it is a finding — and an expensive one, because the non-functional ones are the ones that cost the most to add later.

## Check limit — and it is important to know it

The validator matches by **vocabulary**, and the two directions **use different checks**:

| Direction | What does it compare against | Threshold |
|---|---|---|
| Requirement → class | Name, attributes **and** operations of all classes | **Two** words in common |
| Class → requirement | Only the **name** of the class | One word |

**Why two words and not one.** A single match was enough to cover a requirement that no one had implemented: a requirement about *"export personal data in PDF format"* was silently satisfied by a financial reporting class that declared an attribute `format`. The failure was worse than a false positive, because it was **mute**: the requirement simply did not appear on the list. The threshold of two is **convention of this skill**; it does not guarantee semantic coverage, but it eliminates the accidental match on a single word.

**What remains undetected, and must be said:**

- **Synonyms and paraphrases.** A requirement that talks about "access" and a class called `Authentication` do not pair together.
- **Overlap on two generic words.** Less likely than with one, but possible.
- **Partial coverage.** Just because the vocabulary matches does not prove that the design does *everything* the requirement asks for.

That is why the matrix is a **deliverable that is reviewed**, not an automatic verdict. The validator flags candidates; The one who decides if a requirement is actually implemented is you.

---

# Part 2 · Code headers (rule #2)

> *"Generate the code headers for your classes, and inspect them closely."* — Rosenberg, 4575
> *"See, we told you that you were about to generate code. Once you've done so, inspect the code headers carefully."* — 4628

## What they are and what they are not

**They are** the mechanical translation of the class model into code signatures: classes, attributes with their type, operations with parameters and return. **No bodies.**

**They are not production code.** They are a **review tool**: they exist so that an incoherent model becomes evident. No one should start from them to implement without going through the design of the implementation.

This distinction is marked in the generated file itself, with a header that declares it. If someone finds them loose in six months, they have to be able to know what they are.

## Header scope and authorization

Generate headers when requested or already included in the authorized review-and-fix work. Ask only if a genuine unresolved scope decision remains; existing authorization persists. Report that these are review instruments with unresolved signatures marked explicitly, and inspect/recheck the generated result.

## Why it works: what the translation reveals

The course lists it, and it is the list of questions that appear when viewing the model as code:

- Are any attributes missing?
- Are any parameters missing?
- Are there duplicate operations?
- Are there unnecessary dependencies?

*"Many times errors appear immediately when trying to translate the design into code."*

**The underlying reason:** a diagram tolerates ambiguity; a signature does not. `process(data)` looks plausible in a diagram but exposes unresolved questions in `public ??? process(??? data)`. The generation does not find new defects: it **makes visible those that the diagram concealed**.

## What the generator produces

The default is language-neutral in intent, using familiar Java-like syntax that can be read without knowing the project:

```java
/* CODE HEADERS GENERATED FOR INSPECTION — CDR-XX
 * Review instrument, NOT production code.
 * Generated from MC-XX. Do not edit: edit the model. */

public class Loan {
    private Date startDate;
    private Date dueDate;

    public Loan register(Member member, Copy copy, Date dueDate) { }
    public String generateCertificate() { }
}
```

- **Complete signatures**, because checking them is the objective.
- **Empty bodies**, always.
- **Gaps are marked, not filled.** An absent type returns as `???`, not `Object` — inventing a type would destroy the finding that rule #3 seeks.
- **Relationships are also generated as fields**, because that is where missing multiplicity becomes visible: without it it is not known if a field is a reference or a collection.

## The pace at which they are inspected

The PDR reference paraphrases §6.5.2 as **100–200 lines/hour**, while the CDR historical transcription mixes PPH and LPH. This unit inconsistency remains **unverified against the official table**; do not assume a pages-to-lines conversion or use it as a mandatory header budget. Until verified, estimate from actual header volume and a declared project rate. See `session-budget.md`.

## Where this activity stops

**Generation is automated; inspection is not.** Reading the headers and asking if the model makes sense is human work — it's half of rule #2 that the skill declares as not automatable.

And there is one more border, from the contrast of two figures from the corpus: on the CDR map the arrow `Class Model → Code` goes **in only one direction**; in the code review map it is **bidirectional**. **The CDR authorizes the move.** Resynchronizing the model with the code already written is another, later activity, and is not part of this skill.

---

## Origin

| Source | What it contributes |
|---|---|
| Rosenberg, lines 4572, 4575, 4628 | The two rules and the instruction to inspect |
| Course material, *Session 09* | The traceability chain, the three questions, and what the generation reveals |
| IEEE Std 1028-2008 §6.5.2 | The pace of code inspection |
| *Agile Development [abbreviated title]*, line 1802 | *"the source code headers should have been generated from these class diagrams"* |

## Identifier continuity

Preserve existing `RF-XX`, `CU-XX`, `DS-XX`, `MC-XX`, `CP-XX`, class, operation, and finding mappings. Allocate IDs only for new identities; retire deleted IDs and record replacement links without reuse. Renames retain identity with aliases/change records. After an edit verify every trace reference resolves to a current or explicitly retired/replaced item. The full chain above describes available full-package traceability; independently scoped work reports the links it can check without inventing absent artifacts.
