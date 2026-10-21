<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sources and methods

What each source contributed, what was excluded, and **what could not be verified**. Every skill claim should trace to material someone actually read.

---

## Corpus books

### Rosenberg & Stephens — *Use Case Driven Object Modeling with UML* · primary source

| Section | Lines | Contribution |
|---|---|---|
| "Updating Your Class Diagrams As You Go Along" | 4270-4295 | Sequence synchronization; three design opportunities; solution versus problem; *getters* and *setters* |
| "Synchronizing the Static and Dynamic Parts of the Model" | 4278-4294 | *"with each message arrow… take a peek at the class diagram"* |
| Worked-example model evolution | 4298-4331 | Attribute becomes operation; extracted `View` superclass; multiplicity sidebar |
| "Clean Up the Static Model Before Proceeding to the CDR" | 4035-4058 | Definition of cleanup |
| **Chapter 9, Critical Design Review** | 4521-4963 | Entry criterion (4557); attendees (4545); **Top 10 at 4567-4576**; reverse technique (4642-4648) |
| Named anti-patterns | 4600, 4602, 4726-4746, 4902-4914, 1382 | “Schizophrenic personality,” class without responsibilities, swarm of tiny classes, anemic model, entity without attributes, premature pattern adoption |
| Stable abstractions | 4874-4886 | *"the problem domain winds up being the most stable"* |

**The governing quotation** is at 4363: operations/relationships/attributes allocation and the instruction to revisit earlier work rather than invent details.

**Duplicate note:** CDR Top 10 appears in chapter 1 (890-899) and chapter 9 (4567-4576), with minor wording differences. **Chapter 9** is canonical here.

### Fowler — *UML Distilled* · main notation source

| Section | Lines |
|---|---|
| Conceptual and software perspectives | 677-685 |
| Ch. 3 "Class Diagrams: The Essentials" | 1135-1505 |
| Ch. 5 "Class Diagrams: Advanced Concepts" | 1678-2061 |
| Documentation and detail level | 1083-1105 |

Contributes: properties as one concept (attributes and associations), attribute/operation syntax, multiplicity, navigability, generalization versus classification, dependencies, aggregation/composition, interfaces and abstract classes, `{readOnly}`, visibility, and—most valuable—detail limits.

**Source-quality notice.** The corpus file has **systematic OCR corruption**: `dass`→class, `an`→on, `lt`→it, `1`→I, `saure`→same, `muck`→much, `irrmutable`→immutable. **Fowler quotations are normalized to the correct printed wording**; this disclosure explains discrepancies with the file. *(The sequence skill learned this through an adversarial audit that caught three affected quotations; this skill declares it from the outset.)*

**Edition precision.** The third edition **merged** specification and implementation into one software perspective: *"I found that it was too hard to draw a precise line between the two."* “Fowler's three perspectives” refers to the first edition, not the corpus edition.

### Agile Development [abbreviated title]

| Section | Lines | Contribution |
|---|---|---|
| Static model in the process | 1789-1817 | *"the grittier, more detailed version of the domain model"*; keep domain and static models **separate** |
| Model refactoring | 1902-1913, 2128-2145 | Definition and four-step procedure |
| Problem space to solution space | 1943-1948 | *"moving the class model from a pure problem domain model into a solution space model"* |
| Worked example (mapplet / hotels) | 3508-4189 | Evolution across iterations; aggregation/composition decided during design; feedback from code |
| BCE → layers | 1755-1765 | *"Entity objects are delivered by the Model, Boundary objects form the View, and Control objects form the Controller"* |

**Most useful warning:** omit private methods because they couple model and code *"too tightly"*. The class model is **persistent**; sequences *"have served their purpose"* after code is written.

### Wiegers — *Software Requirements* · limited contribution, but not NOT FOUND

Eleven occurrences of “class diagram” in almost 12,000 lines, **all as an analysis artifact**. The glossary explicitly defines it as *"An analysis model that shows a set of system or problem domain classes, their interfaces, and their relationships."*

Useful contributions:

- **Analysis→design handoff** (4692): *"the designer maps the problem-domain objects to the system's objects and further details each class's attributes and operations."*
- **Data model versus design model** (4762): *"When class diagrams are used for object-oriented analysis or design, the bottommost section of a class rectangle … normally shows the operations… For data modeling, though, that third section of the class rectangle is left empty."*
- **Framing** (4694): *"The UML is primarily used for creating design models."*

**NOT FOUND in Wiegers:** operation allocation from sequences, visibility, patterns in the model, static-model cleanup, or a design-class-diagram checklist. Its traceability framework stays at requirements level rather than detailed design.

---

## Standards and a previously overlooked connection

`ISO_IEC_12207_2017_en.md` is primary text in the corpus.

**This skill's finding: ISO/IEC/IEEE 12207:2017, Annex F.2.2, is literally titled “Static model”**, with an object-oriented definition:

> *"A static model describes the structure of a software system. In object-oriented programming, it is represented through a set of objects (classes) and their relationships (inheritance, association, and dependency), depicted as nodes and links."*

This defines the artifact produced here. **VERIFIED** against primary text, line 4428 (heading at 4426).

**Declared correction:** an earlier version called it *normative*. **That was false**: Annex F is labeled *(informative)* in the standard itself (4402); ISO drafting rules define informative annexes as non-normative. An adversarial audit discovered the error. The correction remains because attributing normative force to an informative annex is exactly the overstatement this file exists to prevent.

**Scope caveat:** Annex F belongs to **Architecture Definition**, not Design Definition. Citing F.2.2 for a **detailed-design** class model is a **reasonable extension, not a direct reading**.

Sibling models: F.2.1 Functional, **F.2.3 Data model**, F.2.4 Behavioral model (the sequence skill's connection), F.2.6 Structural.

**§6.4.5 Design Definition** (2863-2962), **VERIFIED**. Applicable content:

| Clause | Content |
|---|---|
| §6.4.5.1 | *"to provide sufficient detailed data and information about the system and its elements to enable the implementation"* |
| §6.4.5.2 a) | *"Design characteristics of each system element are defined."* |
| §6.4.5.2 d) | *"Interfaces between system elements composing the system are defined or refined."* |
| §6.4.5.2 h) | *"Traceability of the design characteristics to the architectural entities… is established."* |
| §6.4.5.3, note | Design strategy may include *"progressively more detailed definition of objects and their relationships"*: the closest normative connection to a class model |
| §6.4.5.2, note | *"Design provides the 'implement-to' level of the definition"*, sufficiently detailed *"to permit software implementation (construction) and test planning"* |

**Verified gap.** Searching **“class diagram”** across fourteen normative corpus files returns **zero results**, as does **“UML”** (the only apparent match is surname *Umlas* in PMBOK acknowledgments). The §6.4.5.3 artifact list—*"prototypes, data models, pseudocode, entity-relationship diagrams, use cases…"*—**does not name class diagrams**. No local standard names UML. The bridge from standard to notation is declared **synthesis**.

---

## External research

| Source | Status | Contribution |
|---|---|---|
| **OMG UML 2.5.1**, `formal/17-12-05` | **URL VERIFIED, TEXT NOT READ** | Identified by the source research as the current specification. The normative PDF could not be extracted; **no specific clause** (Classifier, Property, Association, navigability) is cited as verified. Notation claims here come from Fowler and MKL, not the standard |
| **CK metrics** (Chidamber & Kemerer, IEEE TSE 20(6), 1994) | **SECONDARY** | WMC, DIT, NOC, CBO, RFC, LCOM. Five of six can be computed from a design class model. Common thresholds (DIT ≤ 5, CBO > 14 excessive) **are not cited as standards**; this skill's thresholds are its own conventions |
| **Genero & Piattini**, class-diagram maintainability | **SECONDARY** | Understandability, modifiability, and analyzability predicted from early structural measures, particularly **associations and generalizations** |
| UML *model smells* | **SECONDARY** | God Class / Blob confirmed as a **model** smell, not only a code smell. Smell→diagram-element mapping **was not obtained verbatim**: PDF not extractable |
| **Torre, Labiche & Genero**, EASE 2014 | **NOT REVERIFIED** | The Class↔Sequence figure cited by the sequence skill **could not be confirmed in this attempt**: ACM, ResearchGate, and ScienceDirect returned 403; open PDFs were not extractable. A later paper by these authors plus Elaasar (*JSS* 144, 2018) validates 116 rules with 106 experts and is preferable if obtainable |

**Honesty rule.** No figure enters without provenance. Validator thresholds—God class, class swarm, inheritance depth—are declared in code as **skill conventions, not evidence**, and generate warnings rather than errors.

---

## Combining the sources

- **Rosenberg & Stephens:** **what and when**—space convergence, pre-CDR cleanup, named anti-patterns, and review checklist.
- **Fowler:** **notation**—detail limits and fine distinctions; most cited in `notation-rules.md`.
- **Agile Development (2005):** **evolution**—model refactoring, domain/static separation, and the artifact's role after coding.
- **Wiegers:** **boundary** between analysis and design.
- **12207:** **standards framing** for the static model and design traceability, with scope caveat declared.
- **External research:** quality-assessment vocabulary, always marked secondary.
