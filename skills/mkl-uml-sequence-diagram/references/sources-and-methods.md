<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sources and methods

This record identifies each source's contribution, excluded material, and **unverified claims**, so that every skill rule has an inspectable basis. Corpus locations, line numbers, and verification statuses describe the **upstream author's research**. The source corpus is not bundled here, and its checks were not repeated for this English edition.

## Books in the original corpus

### Rosenberg & Stephens — *Use Case Driven Object Modeling with UML*: primary source

Chapter 8, corpus lines 3829–4368; condensed overview at 841–901; exercises at 4369–4519.

This source supplies most method guidance: **ten guidelines** (3879–3889), **four steps** (4061–4077), **three goals** (3901–3903), control transformation and its **80%** estimate (3865), behavior allocation among collaborating objects (3988), return-message guidance (3869), focus of control (3871, 3990, 4451), class-model synchronization (4270–4286), convergence of problem and solution spaces (4284–4286), responsibility and discordant-attribute checks (4192–4210), four criteria for a good class (4212–4222), and three named anti-patterns (4405–4463).

**Critical Design Review**, chapter 9 (4521–4958), belongs to the next stage, although its technique of using class diagrams to find sequence errors (4642) is already applicable.

### Fowler — *UML Distilled*: a substantive contribution here

Chapter 4, lines 1506–1651, supplies **centralized versus distributed control** (1526–1556), message kinds and arrowheads (1634–1640), activation bars (1532), returns (1536), creation/destruction (1560–1562), combined fragments (1570–1630), and situations where sequence diagrams are unsuitable (1642–1648).

**Source-quality qualification:** the corpus file contains **OCR corruption**. Three used quotations have the pronoun *I* scanned as **1** at lines 1536, 1630, and 1640, in statements about returns, interaction frames, and arrowheads. This skill normalizes them to the intended printed wording and discloses the change to explain discrepancies with extracted text. The upstream record says other used Fowler quotations were clean. An earlier statement that all were clean was corrected after an adversarial audit.

Fowler contributed no robustness/PDR-specific guidance in those skill source reviews. Its substantial relevance here illustrates why applicability must be checked separately for each artifact.

### *Agile Development [abbreviated title]*

Contributes a condensed three-step recipe (3688–3690), model refactoring (3684–3778), and particularly **Model-Driven Testing** (7289–7315) and chapter 12 on MKL/TDD (6584 onward), supporting `CP-XX` derivation.

### Wiegers — *Software Requirements*: no applicable sequence-specific guidance found

The upstream search found “sequence diagram” exactly once, at line 3318, without substantive development. Chapter 29's traceability framework remains at requirements level, and test derivation begins with use cases rather than sequence diagrams.

**No sequence-specific rule in this skill is attributed to this book.**

### Course material outside the corpus: the source resolving a default

Chapter 7 of Gloria L. Giraldo's *Análisis, Diseño y Construcción de Productos de Software* [Analysis, Design, and Construction of Software Products] supplies four passages used by the skill. **Guideline 6 determines the default activation-bar convention**; another passage permits architecture and storage objects during detailed design.

This material was **not present in `libros_y_normas_markdown/` or elsewhere in the original repository**. It was available through a user-provided PDF. Consequently, its quotations cannot be checked from the packaged corpus. Verification requires that PDF.

Its provenance matters because it resolves a design choice. The robustness skill also cites this course material in eleven places. An adversarial audit identified its omission from an earlier source record; this qualification preserves the correction.

## Standards: upstream primary-text verification

The upstream author checked `ISO_IEC_12207_2017_en.md` in `libros_y_normas_markdown/`:

| Clause | Recorded status | Contribution |
|---|---|---|
| **§6.4.5**, Design Definition (line 2863) | **VERIFIED** | Process context for detailed sequence design |
| **§6.4.5.2 h)** | **VERIFIED** | Traceability from design characteristics to architectural entities |
| **§6.4.5.3**, task 2) | **VERIFIED** | Links between detailed design elements, requirements, and architectural entities, reflected in this skill's matrix |
| **§6.4.9**, Verification (3239) | **VERIFIED** | Design-review context |
| **§6.3.6**, Information Management | **VERIFIED** | Seven information item quality criteria |

**Declared evidence gap:** searches for “sequence diagram,” “interaction diagram,” and “class diagram” across the original ISO corpus found no matches. No local standard explicitly named UML. The closest connection is 12207 Annex F.2.4's behavioral model, addressing execution sequencing, synchronization, and concurrency without UML vocabulary. **The mapping from those process/model concepts to UML notation is synthesis, not a direct standard requirement.**

**Historical correction:** an earlier package review called §6.4.5 secondary because primary text was supposedly unavailable. That was incorrect: the author had generalized a failed web/paywall search without inspecting the local corpus. Unsupported uncertainty is also inaccurate evidence reporting.

## OMG UML: normative notation source

**Historical edition qualification:** the upstream review read **UML 2.5** (`formal/2015-03-01`) from a public mirror and could not open the **UML 2.5.1** PDF (`formal/17-12-05`, December 2017) within its download limit. Its original clause checks below therefore referred to 2.5.

**Current correction:** the relevant 2.5.1 primary text was available and checked for Message/MessageSort semantics (§17.4.3, §17.12.18), actor participation (§18.1.3), and Property/composition semantics (§9.5.3). Current semantic corrections cite [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF). This limited check does not claim a new audit of every historical 2.5 clause below.

Clause 17, *Interactions*, supports the following, all recorded as verified upstream:

- **17.12.17 Lifeline:** an individual interaction participant, representing a single interacting entity.
- **17.12.18 Message** and **17.12.22 MessageSort:** `synchCall` (**default**), `asynchCall`, `asynchSignal`, `createMessage`, `deleteMessage`, and `reply`.
- **17.4.4.1 Message notation:** filled synchronous arrowhead, open asynchronous arrowhead, dashed reply, and dashed creation message with open arrowhead.
- **17.12.8 ExecutionSpecification:** activation bars.
- **17.12.3 CombinedFragment**, **17.12.14 InteractionOperand**, and **17.12.12 InteractionConstraint:** `opt`, `loop`, `break`, `assert`, and `neg` have **exactly one operand**; an omitted guard defaults to **true**.
- **17.12.15 InteractionOperatorKind:** twelve operators.
- **17.7 InteractionUse:** `ref`.

**Two negative findings limit the skill's claims:**

1. **The inspected specification does not state that activation bars are optional or mandatory.** The optionality claim comes from Fowler. Omitting them here is a **style convention**, not a demonstrated normative requirement.
2. **The specification does not require an association or visibility path for every sender/receiver pair.** The complete `Message` constraints (17.12.18.7) contain no such restriction; `Message::connector` has optional multiplicity `[0..1]`. Requiring the sender to hold a receiver reference is a **design/tool rule**, not a UML-standard constraint, and this skill labels it accordingly.

## Empirical research

### Class–sequence consistency: central to this skill

**Torre, Labiche & Genero, EASE 2014**, full text read in the upstream review: 95 primary studies yielded 119 nonredundant rules. The **class–sequence pair accounts for 26 rules (21.85%)**, the largest group; the class–use case pair relevant to PDR had only five. Of all rules, 98.10% are horizontal and 88.21% syntactic; sequence diagrams appear in 47.37% of studies.

**Recorded erratum:** §6.2's prose names CD-SD, CD-COD, and SD-SCD as the top three pairs, but its summed percentages correspond to CD-SD, CD-SCD, and CD-COD. This does not change the rules used here.

**Torre et al., FormaliSE 2020**, full text read upstream, explicitly enumerates relevant rules:

| Rule | Statement |
|---|---|
| **R110** | A referenced operation belongs to the class typing the receiving lifeline; supports the operation delta |
| **R112** | Sender has a reference to receiver according to the class diagram; **design rule, not normative UML constraint** |
| **R116** | Operation use respects visibility |
| **R109** | An operation referenced by a message is not abstract |
| **R98** | Each sequence diagram corresponds to a use case, matching MKL guideline 9 |
| **R115** | Each class is instantiated in some sequence diagram; the authors identify this as deliberately strong |

The authors could not encode **19 of 52 rules** in OCL because of complex algorithms or information absent from the UML standard. This skill encounters the same automation limits.

### Responsibility allocation

**Wirfs-Brock, *A Brief Tour of RDD in 2004***: the author's presentation was read upstream. It supplies six role stereotypes and guidance to keep related behavior/information together and information about one thing in one place. *Object Design: Roles, Responsibilities and Collaborations* was **absent from the corpus** and is cited through restatements. Because secondary sources disagree on publication year (2002 in course material; 2003 in Rosenberg's footnote), the source record avoids fixing a year.

**GRASP, Larman:** **secondary confidence** through two restatements, not direct reading of the book. Used as supplementary vocabulary rather than the sole basis for a rule.

**Law of Demeter:** Lieberherr and Holland, *IEEE Software* 6(5), 1989, DOI 10.1109/52.35588. Located copies were scanned images without searchable text; the original class/object formulations were **not read directly**, and are known through restatements.

### Test derivation

A systematic review of UML-based test generation, **62 primary studies from 443 candidates**, 1999–2019, identifies path coverage as common and **combined fragments as the hardest problem**, with combinatorial growth under exhaustive coverage. **Secondary confidence:** indexed text was consulted rather than the digital-library version.

## Searches with no supporting result

These limits constrain what the skill may claim:

1. **No published numerical readability threshold** was located for lifeline count, message count, or fragment nesting. Validator thresholds are **skill conventions**, not empirical findings; the script identifies them as such.
2. **No canonical sequence-diagram smell catalog** was found. This skill's anti-pattern catalog combines specification constraints, Torre's class–sequence rules, responsibility criteria, and named MKL anti-patterns.
3. **No inspected study isolated lifeline count or nesting depth as measured comprehension predictors.** Located comprehension studies were paywalled and only abstracts were read.
4. **The complete list of Torre's 119 rules was not obtained.** The 2014 paper points to a technical report; a 2018 doctoral thesis was identified as a likely source.

## Combining the evidence

- **Rosenberg & Stephens:** method guidelines, construction steps, control transformation, and behavior allocation.
- **Fowler:** design quality criteria and notation precision.
- **Agile Development (2005):** iterative workflow and test derivation.
- **OMG UML 2.5:** normative notation semantics and explicit limits on what the standard states.
- **12207 §6.4.5:** traceability expectations addressed by the matrix.
- **Empirical research:** class–sequence consistency and test-coverage guidance, with disclosed limits.
- **Wiegers:** no sequence-specific rule contribution in this source review.

## UML correction and limits of consistency rules

Message-sort interpretation was checked against [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) §17.4.3 and §17.12.18: Operation calls (`synchCall`/`asynchCall`) allocate receiving-class operations; replies return outputs of original synchronous calls; Signals and lifecycle messages have separate semantics. Unknown sorts/signatures remain unresolved. The call-centered practitioner shorthand and R110 above must be read with that scope. Torre's enumerated rules are research consistency rules, not universal UML requirements: in particular R109 is not a blanket prohibition on invoking an abstract operation through polymorphic dispatch, R98 is this method's use-case alignment convention, and R115 is deliberately stronger than the selected-scenario coverage normally needed. Never synthesize operations from reply labels or from every arrow indiscriminately.
