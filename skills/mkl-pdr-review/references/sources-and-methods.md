<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sources and methods

> Historical upstream record: this English edition translates the original author's source-verification and audit claims. Those source checks and historical audits have not been newly repeated for this fork.

What was taken from each source, what was discarded, and—most importantly—**what could not be verified**. This file exists so that any assertion of the skill can be traced back to something someone actually read.

---

## Corpus books

### Rosenberg & Stephens — *Use Case Driven Object Modeling with UML: Theory and Practice*

**Primary source of the method.** It is the only book in the corpus that contains the PDR chapter (lines 3131-3424 of the corpus file). From here come: the ten guidelines (3179-3278), the six steps (3267-3278), the position in the process (826), the participants (3151-3153), the "back to step 1" (3157-3163), the highlighter test (3192-3202), the data flow (3210-3214), the quantification of the alternate courses (3224), the mini-contracts and the level of abstraction (3251-3253) and the two passes (3265).

**What this book DOES NOT give:** a duration for the PDR session. We searched and it is not there. The time budgets for this skill come from and are attributed to IEEE 1028 and Wiegers.

**Provenance of the six steps:** the footnote of the chapter itself attributes them to a previous book by Rosenberg & Scott that is **not in the corpus**. They are cited from the book that is there, where they are reproduced. The original work is not cited.

### Wiegers & Beatty — *Software Requirements, 3rd ed.*, chapter 17

**Primary source for how a review is conducted.** Rosenberg tells what to look for; Wiegers tells how to look at it. Hence: the four roles and their separation, the entry and exit criteria, the five stages, the pace of 2-4 pages/hour, 75% of defects found in preparation, the return of up to 10 hours per hour invested, the team of seven or less, the limit of three reviews of the same material, the meeting of no more than two hours, the absence of the author's boss, and the finding that several small teams outperform a large one.

The chapter itself states that its description of the inspection is based on Fagan's technique.

### Rosenberg, Stephens & Collins-Cope — *Agile Development [abbreviated title]*

It provides two concrete things: the **four milestones** of the process (1657-1663), which place the PDR as Milestone 2; and the BCE→MVC mapping (1761): *"Entity objects are delivered by the Model, Boundary objects form the View, and Control objects form the Controller"*, which is what makes the optional architecture layer usable.

**Caveat stated:** the book contains a client review meeting section in its case study, but it is **not labeled PDR** in the text. It is used as an example of a review in an iterative context, not as a description of the PDR.

### Fowler — *UML Distilled*

**CONTRIBUTES NOTHING TO THIS SKILL.** Explicitly searched for "Preliminary Design Review", "PDR", "robustness diagram", "Boundary-Control-Entity", "walkthrough" and "inspect": **zero relevant occurrences**. Occurrences of “review” in that book are incidental.

The closest are his three perspectives on UML—conceptual, specification, implementation—which are a modeling classification, not a review procedure, and which the book never connects to MKL or a review milestone. **Does not stretch**: It is stated that this book does not establish any rules for this skill.

---

## Standards — verified on primary text

### IEEE 1028-2008 — Software Reviews and Audits · **the anchor**

The upstream author read the primary text and used these clauses:

| Clause | What it contributes |
|---|---|
| §1.5 | The seven-part anatomy of every review — minutes structure |
| §6.1 | Team size: 2-6 participants |
| §6.2 | Inspection roles |
| §6.4.3 | Entry criteria, including automatic pre-detection |
| **§6.5.2** | **Pace: preliminary design 3-4 pages/hour** |
| **§6.5.6.5** | **The three-state exit decision — the verdict model** |
| §6.7 | Mandatory content of the output — structure of the record |
| §6.8 | Classification of anomalies, mandatory in inspection |
| Annex A | Comparison of types; inspection is the only one that requires a checklist |

### IEEE 1016-2009 — Software Design Descriptions

Primary text read. §3.2.3 (design verification is done by review or inspection, referring to IEEE 1028) and §4.4 (definitions of "complete" and "consistent" for a design description) are used.

### ISO/IEC/IEEE 29148:2018 — Requirements Engineering

Primary text read. §5.2.5 and §5.2.6 (characteristics of individual requirements and requirement sets) are used as vocabulary when judging use case text, and §6.3.3.7 NOTE 1, which refers to IEEE 1028 for reviews.

---

## What could NOT be verified — explicit flags

These four warnings are as much a part of the rationale as the quotes. Omitting them would make the rest less reliable, not more.

**1. ISO/IEC/IEEE 12207:2017 §6.4.5 "Design Definition" — VERIFIED (correction).** A previous version of this file marked it as secondary because it could not be confirmed. **It was an error**: the primary text is in the corpus itself, in `libros_y_normas_markdown/ISO_IEC_12207_2017_en.md`, line 2863. §6.4.5.2 h) and §6.4.5.3 (traceability between design elements, requirements and architecture), §6.4.9 (Verification) and §6.3.6, which literally states the seven criteria of the information item, are also verified. The failure came from trying to confirm them on the web—where they are behind a paywall—and generalizing that failure without looking at the repository. It is left in writing because **excessive caution can also misrepresent the evidence**: marking a solid quote as dubious is as misleading as inventing it.

**2. ISO/IEC/IEEE 15289 — NOT VERIFIED for review record.** No clause specifying the content of a review record could be confirmed in its text. That is why the `PDR-XX` document is structured around **IEEE 1028 §6.7**, which was read in full. If 15289 is ever cited for this, it will be a secondhand quote.

**3. Boehm's 1:10:100 ratio — POPULARIZATION.** The increasing cost of fixing a defect as the cycle progresses is a real result, but the round "1:10:100" ratio is a later simplification, of disputed origin, that discards the confidence intervals and segmentation by project type of the original work. This skill **does not cite that ratio as Boehm's literal finding**. It supports the value of the PDR through other evidence: the evidence of the effectiveness of the inspection and the documented gap in the investigation.

**4. MKL has no independent empirical validation.** No rigorous studies were found measuring the effectiveness of MKL PDR—defect rates, savings—comparable to the inspection literature. What exists is descriptive and pedagogical material. **The legitimacy of this skill does not rest on MKL studies**, but on: (a) the book's method, (b) the science of IEEE 1028 and Wiegers inspection, and (c) the documented research gap described below.

---

## Empirical research that does support the design of the skill

**The gap exists and is measured.** Torre, Labiche & Genero, *UML Consistency Rules: A Systematic Mapping Study*, EASE 2014 (full text read). From 95 primary studies they extract 263 unique consistency rules between UML diagrams. The study reports:

- **98.10%** of the rules are horizontal; virtually none cover consistency throughout evolution.
- **88.21%** are syntactic; only 11.79% semantic.
- The class diagram appears in 71.58% of the studies and the sequence diagram in 47.37%, but **the use case diagram only in 14.74%**.
- For the pair Class↔Use Case there are **5 rules** (4.20%); the same for Sequence↔Use Case.
- **44.21%** of the studies do not offer any tool support.

That is to say: the frontier that the PDR monitors—use cases versus object models—is precisely the least studied and least automated of UML. This skill fills a documented gap, it does not reinvent resolved territory.

**Consistency checking is tractable.** Egyed, *Instant Consistency Checking for the UML*, ICSE 2006 (full text read): 29 real models, some with more than 100,000 elements, 24 rule types, more than 140,000 evaluations; 99% of changes are verified in less than 50 ms. It supports that checking consistency between artifacts is feasible incrementally, not just in theory.

**Why checklist and not perspectives.** Sabaliauskaite, Matsukawa, Kusumoto & Inoue, ISESE 2002 — **SECONDARY EVIDENCE** (a consistent account in secondary sources; the primary text was not read). In an experiment with 59 subjects **on inspection of UML design documents**, reading based on checklists surpassed reading based on perspectives, contrary to what is observed in code and requirements. This skill is built as a checklist engine in part for this reason, and the confidence level is stated because the statement goes against the grain of the general literature.

**Where inspection is useful.** Shull, Carver, Vegas & Basili, *What Do We Know about Defect Detection Methods?*, IEEE Software 2006 — **SECONDARY**. Synthesizing twelve studies, they recommend using inspection for requirements and design defects, and testing for code defects. It is the argument for why a gate like the PDR is the right instrument at this stage, rather than leaving everything to testing.

**Inspection effectiveness.** Fagan's original data (82% of errors found by design and code inspections in a product) is verified through an SEI technical report that reproduces it — **second-hand quote, stated**. The original 1976 article is behind a paywall and was not read.

**Faster inspection rates reduce detection.** Russell, *"Experience with Inspection in Ultralarge-Scale Developments"*, IEEE Software, January 1991, pp. 25-31: defects found per thousand lines fell from 50 to 15 by tripling the inspection rate (from 150 to 450 lines/hour). **SECONDARY EVIDENCE** — read reproduced in the SEI technical report itself, not in the original article. This is the figure supporting the session budget notice in `review-protocol.md`; It is cited with author and venue precisely because a figure without origin should not be in an artifact that promises traceability. Wiegers points in the same direction from the corpus, without giving the figure: *"the optimum rate for maximum defect-detection effectiveness is about half that rate"*, citing Gilb and Graham.

**Caveat on Wiegers' page/hour figure.** His "two to four pages per hour" is stated for inspection of **requirements documents**, not design documents, and his book does not segment by document type as IEEE 1028 does. The match to IEEE 1028's 3-4 for preliminary design is of the same order but **is not matched by artifact type**; The number that governs this skill is IEEE 1028.

**The meeting controversy.** There is a line of work that questions whether the inspection meeting provides value over individual preparation. It is mentioned here so as not to conclude something that is not settled: this skill automates the preparation—where the evidence is solid—and leaves the form of the meeting up to the user's decision.

---

## How to combine

- **Rosenberg** provides the specific PDR checklist: the ten guidelines and the six steps. It's the **what**.
- **IEEE 1028** provides the procedure, entry and exit criteria, review rates, and three-state verdict model. It's the **how**.
- **Wiegers** provides the roles, stages and efficiency numbers that justify automating preparation. It's **why it works**.
- **IEEE 1016 and 29148** provide the regulatory bridge and quality vocabulary.
- **Empirical research** justifies the form of the tool—checklist, verification between artifacts—and honestly locates what is known and what is not.
- **Agile Development (2005)** provides the BCE→layers mapping that makes the optional architecture review usable.
- **Fowler** does not contribute anything here, as explicitly recorded.
