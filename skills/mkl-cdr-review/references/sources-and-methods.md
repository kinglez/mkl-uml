<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sources and methods

> Historical upstream record: this English edition translates the original author's source-verification and audit claims. Those source checks and historical audits have not been newly repeated for this fork.

What was taken from each source, its verification status, and **what was not found**. The explicit limitations are as much a part of the foundation as the quotes: without them, the rest seems stronger than it is.

---

## Self-contained operation — read first

**This is the only file in the package that details the editorial origin of the personal corpus used to build the skill**, as **auditable origin**, not as an operational dependency. This corpus is a personal collection of the author and is not distributed with this repository (due to copyright of the cited sources).

**The skill works without any of this.** Each quote used is transcribed in full in the corresponding references; The line and clause numbers are used so that someone with access to the original sources can verify that the quote is faithful. If you install this skill without access to that corpus, **all of its rules still apply**.

No instructions in this skill require consulting an external source. If you find one, it is a packaging defect and should be reported.

---

## Primary sources

### Rosenberg & Stephens — *Use Case Driven Object Modeling with UML: Theory and Practice*

**The source of the method.** It is the only book in the corpus with a chapter dedicated to CDR.

From here comes: the three objectives (4535-4539) · the entry criterion (4555-4557) · that the client does not participate and that it is a technical review (4545) · **the ten rules** (4567-4576) and their development (4578-4948) · the Highlighter Technique applied to the sequence (4580) · the inverse class→sequence technique and the case of `Queue` (4642-4648) · the `Book` case without responsibilities (4658-4746) · the `WriteCustomerReviewCommand` case (4848-4872) · the object without messages (4820-4846) · the entities without attributes (4902-4914) · the notice about aesthetics (4944) · stable abstractions (4874-4886) · closure (4950-4964).

And two contributions from neighboring chapters: the **precondition** of chapter 8 (4035-4037) and the **checklist construction algorithm** of chapter 11 (6042-6157).

**What the upstream search did not find in this book:**
- **No verdict scale.** Chapter 9 has no acceptance or rejection language; closes qualitatively (*"fighting-fit"*). The three-state scale comes from IEEE 1028, and is cited as such.
- **No session duration.** Rates come from IEEE 1028; size limits, from GQM.
- **No numerical threshold** for God class, coupling or complexity.

### IEEE Std 1028-2008 — *Software Reviews and Audits* · the anchor of the procedure

**Primary text read in full** (52 pages).

**Clause 5 — Technical reviews**, which governs this CDR: §5.1 purpose and mandate to examine alternatives · §5.2 roles, with the **decision maker** · §5.3 inputs · §5.4.2 preconditions · §5.5.6 the seven determinations and the note on action points · §5.6 exit criteria · §5.7 **mandatory content of the minutes**.

**Clause 6 — Inspections**, from which **four explicitly borrowed elements** are taken: §6.5.2 rate table · §6.5.6.5 three-state scale · §6.7 the material size field · §6.8.2 and §6.8.3 categories and ranking of anomalies. Plus §6.9, which requires analyzing the review process itself.

**Location:** personal copy of the author's PDF, obtained separately from the general corpus of books and standards (not included in this repository due to copyright).

**Correction declared, and it should be left written.** During the construction of this skill an alarm was raised about the citations of IEEE 1028 in `mkl-pdr-review`, because **the standard was not in the author's general corpus of books and standards** (a search for "1028" on that corpus did not return the text). Upon obtaining the PDF and reading it, **the quotes from that skill were correct**: §6.5.2 does include the review rate table and §6.5.6.5 does include *"Make exit decision"* with three states. The alarm was about **verifiability from the corpus available at that time**, not about the content. It is closed, and is noted here because the doubt was registered at the time.

### Wiegers & Beatty — *Software Requirements, 3rd ed.*, chapter 17

**How a review is conducted.** From here: the four roles and their separation · entry and exit criteria · **the five stages** (not six: the *overview* is part of the preparation) · the 75% of defects found in preparation · the preparation ≥ 50% of the meeting time · the meeting ≤ 2 hours · the limit of three reviews due to fatigue · the three-state verdict for requirements (6318) · the types of informal review · the *review challenges*.

**What the upstream search did not find:** a section of metrics to record from the inspection itself. There are scattered mentions of the history of pace versus effectiveness, but not a prescriptive list. The mandate to measure is taken from IEEE 1028 §6.9.

### Course material — *Session 09: Critical Design Review*

**Established the terminology of the original Spanish skill**: *Critical Design Review*, *Highlighter Technique*, *Rule 10…1*, *red flags*.

And it provides its own content: the step-by-step procedure of the highlighter · **the two checks of rule #3** (vague types and names that do not express intent) · **the three questions for suspicious classes** · the development of *stable versus unstable abstractions* · two worked examples with class counting before and after.

**Attribution note, corrected during construction.** Two things that were initially attributed to this material turned out to be **also in Rosenberg**: that the client does not participate (4545) and the Highlighter Technique (4580). The course confirms and develops them in Spanish; does not originate them. It was corrected before writing these references.

### van Solingen & Berghout — *The Goal Question Metric Method*, Case B

**The only measured evidence from the corpus on revisions.** RITME project: 378 faults, 43 hours, 998 pages, 24 KSLOC. This is where all the empirical data of `session-budget.md` comes from.

**No sister skills used this book.** It is the contribution that allows the CDR to have session thresholds with support instead of convention — the problem that `mkl-uml-design-class-model` had to explicitly declare as "convention, not evidence."

### Ebert & Dumke — *Software Measurement*

**5/20/80 triage** (§9.3.3) and CK metric definitions (§10.4). **With the caveat that the LCOM formula is corrupted** in the corpus markdown and should not be copied from there.

### Quality standards

| Standard | What is used |
|---|---|
| **ISO/IEC/IEEE 12207:2017** | §6.3.3 *Decision Management*, the four outputs that structure Act II. And §6.4.5 *Design Definition*, with the note that *"Design reviews are conducted using the Validation process"* |
| **ISO/IEC 25010** | Maintainability subcharacteristics as a vocabulary for organizing findings, and the *Modularity* note that links cohesion and coupling |
| **ISO/IEC 25023:2016** | §8.8.1: normative formulas for coupling and complexity adequacy, **with the threshold delegated to the organization** |
| **ISO/IEC/IEEE 15939:2017** | The definition of *decision criteria*, which provides a method for establishing thresholds |
| **ISO/IEC/IEEE 90003:2018** | §8.3.4.1: The condition for proceeding with known deficiencies |

**On normative versus informative.** In ISO 12207 **only Annex A is normative**; Annexes B to I are labeled *(informative)*. The body clauses are normative by the verb convention declared in §4: *"Requirements of this document are marked by the use of the verb 'shall'"*. In 90003, the entire document is **guidance**: *"It does not add to or otherwise change the requirements of ISO 9001:2015."*

---

## Fowler — *UML Distilled*: does not contribute to this skill, and is said

*checklist*, *design review*, *code smell*, *god class* were explicitly searched. **Zero relevant results.** The only applicable thing is their general warning about class diagrams —*"The biggest danger with class diagrams is that you can focus exclusively on structure and ignore behavior"*—, which supports why the CDR reviews class and sequence **together**, and is already included in `/mkl-uml-design-class-model`.

**Do not overextend the source.** This book does not support any CDR rules.

*(The upstream corpus file also has systematic OCR corruption: `dass`→class, `an`→on, `1`→I. If it is ever cited, it must be normalized and declared.)*

---

## External investigation

Scientific sources were consulted on inspection effectiveness and UML diagram metrics. **They do not establish any rules for this skill**, for a deliberate reason: what they contributed was already available in the corpus, with verifiable primary text. They are noted for transparency:

- Literature on optimal inspection pace (~200 LOC/hour, 8-12 pages per session), which **converges** with IEEE 1028 and with GQM. It was preferred to cite the sources that are in the corpus.
- The Genero–Piattini line on class diagram metrics and its empirical validation as predictors of maintainability. It is relevant and solid, but **the full text could not be read** (PDFs whose full text could not be extracted). It is mentioned as a clue, **not cited as a basis**.

**Criteria applied:** If something could not be read, it is not cited as if it was. An unverified bibliographic reference in an artifact that promises traceability is exactly the defect that this skill looks for in others.

---

## What was NOT found — explicit flags

1. **Numerical threshold of cyclomatic complexity**: does not exist in the entire corpus, and ISO 25023 expressly delegates it to the organization.
2. **CK metrics thresholds** as objectives: there are only observed values on Java libraries, which are a comparative reference.
3. **Full LCOM formula**: corrupted in the corpus markdown.
4. **Total duration of a CDR**: no source gives it.
5. **Diagram↔page equivalence**: no source defines it. This skill (40 effective lines) is a declared convention.
6. **Rosenberg verdict scale**: does not exist; comes from IEEE 1028.
7. **A “Detailed Design Top 10” in Agile Development (2005)**: does not exist; its only Top 10 is agile values.
8. **Section on reviewing diagrams vs. text in Wiegers chap. 17**: only scattered mentions in another chapter.
9. **Independent Empirical Validation of MKL**: No studies were found measuring the effectiveness of the MKL CDR. **The legitimacy of this skill does not rest on that**, but on the book's method, the science of inspection (IEEE 1028, Wiegers) and the GQM review data.

---

## Historical review coverage of the upstream package

The skill requires reviewers to disclose their coverage. The upstream author recorded the following review history and its exclusions; this is a historical account, not a new audit of the English fork.

| Round | Reviewer | Scope | Verified findings | Status |
|---|---|---|---|---|
| 1 | Independent subagent | Complete package | 16 (3 critical) | Corrected, with regression fixtures |
| 2 | Independent subagent, interrupted by the spending limit | Rules #6/#8, parsing, budget | 6 leads, subsequently verified by the upstream author | Corrected |
| 3 and 4 | Self-audit | Probes targeting known weaknesses | 0 new | Two consecutive clean passes |
| A | Independent batch audit, batch A | PlantUML parsing, rules #6/#8, header generator | 7 (2 critical) | 6 corrected; 1 limitation documented |
| B, focused | Prose-to-code comparison on the packaged `.skill` | Every concrete prose claim: five vague-type tokens, six names that do not express intent, fourteen `[automated]` anti-patterns, and five cited numbers | 0 mismatches; 2 checks without regression coverage | Both gaps closed with dedicated fixtures |

**Historical stopping criterion:** the upstream author used two consecutive rounds without new findings within five passes. This is not the default workflow or a correctness guarantee for this fork; scoped checks and affected rechecks suffice unless a formal audit is explicitly requested.

**Explicit exclusions and limitations:**

- **Batch B covered only the focused comparison.** Every concrete statement about tokens, names, numbers, and `[automated]` annotations was checked against the code. The references did not receive a complete adversarial reading.
- **Batch C was not run.** Its intended scope was to verify every quotation against the exact wording of its source. Axis 2 of the consistency review (CDR-9) covered part of that scope through scripts, rather than direct comparison with the original texts.
- **Rounds 3 and 4 were self-audits**, rather than independent reviews. They provide weaker evidence than rounds 1, 2, and A, which is why the table distinguishes them.
- **A known, deliberate limitation:** uppercase accessor names such as `GETNOMBRE` are not recognized as accessors. Rule #8 therefore requires a source message for them and may produce a false positive. A pattern broad enough to recognize `GETNOMBRE` would also exempt `HASTA`, `SETENTA`, and `ISLA`, reintroducing a **silent** missed check, which is worse than a visible false positive. The pipeline uses `camelCase`. See `anti-patterns.md`.

---

## How to combine

- **Rosenberg** provides **what to review**: the ten rules and the worked examples.
- **IEEE 1028** provides **how to conduct it**: roles, inputs, determinations, minutes and disposition.
- **Wiegers** provides **why it works**: the stages and numbers that justify automating preparation.
- **GQM** provides **how much can fit in a session** and **how to know if the review was useful**.
- **12207, 25010, 25023, 15939 and 90003** provide the **standards-based framework** and the mechanism to avoid inventing thresholds.
- **The course material** provides **terminology in the original Spanish edition** and two automatable checks.
- **Fowler** does not contribute anything here, as explicitly recorded.

---

## Where each source lives

For those who want to audit the quotations. **The skill does not need it.**

| Source | Location in the construction environment |
|---|---|
| Rosenberg · Agile Development (2005) · Wiegers · GQM · Ebert & Dumke · ISO standards | Author's personal copy, in markdown extracted from the original PDFs (not included in this repository due to copyright) |
| IEEE Std 1028-2008 | Author's personal copy of PDF (not included in this repository) |
| Course material, Session 09 | Material from the author's university course (not included in this repository) |
| Figures from the corpus | Screenshots of the above sources, archived locally by the author (not included in this repository) |
