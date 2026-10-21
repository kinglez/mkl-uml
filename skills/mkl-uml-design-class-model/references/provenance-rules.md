<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Provenance: what traces to what

This is the governing rule, and the one to remember if the rest is forgotten. This file makes it operational.

---

## The rule

Rosenberg & Stephens, corpus lines 4363 and 4365 (division of work at 4363; instruction to revisit earlier artifacts at 4365):

> *"It's tempting to add detail to the class diagram because you think it might be needed, but… it's better fill in the detail while drawing the sequence diagrams. If, after you've fleshed out the static model using the sequence diagrams, the static model still appears to be missing some detail, then you should revisit the sequence diagrams (and possibly even the robustness diagrams and use cases), as it's likely that something has been missed."*

The conclusion makes this a rule rather than advice:

> *"Always trust your gut instinct, but use it as an indication that you need to revisit your previous diagrams, not that you need to second-guess yourself and add detail arbitrarily to the static model."*

**Operational interpretation:** a sense that something is missing is information about **earlier** artifacts, not permission to fill the gap. Report it rather than conceal it.

---

## Provenance table

Line 4363 explicitly divides the work:

| Model element | Source | Verification |
|---|---|---|
| **Operation** | An Operation-signed `synchCall`/`asynchCall` in a `DS-XX`, or a declared contract/design delta | The call invokes the receiving classifier's operation; trace the originating call or justified contract/delta. Replies, Signals, and lifecycle messages are not ordinary operations |
| **Problem-space class** | Domain model | Exists there under the same name, or name drift is declared |
| **Solution-space class** | Design: scaffolding, infrastructure, framework | **Marked accordingly** and justified |
| **Relationship** | Domain model, or an operation requiring it | Exists in the domain, or an operation needs to navigate it |
| **Attribute** | `CU-XX` specification, prototypes, or domain model | Name appears in use case text, a wireframe, or the domain |
| **Invariant or constraint** | An `RN-XX` specification rule | Business rule exists and is cited |

The source describes a sound model as *"contains purely the detail we've uncovered during domain modeling, robustness analysis, and sequence diagramming, and nothing more. There are no leaps of logic, leaps of faith, or leaps of any kind."*

---

## Handling untraceable elements

**Neither delete nor invent: report.** Include each untraceable element in the *report of elements without provenance*, stating what it is, why it seemed necessary, and which artifact needs revisiting.

| Situation | Meaning | Destination |
|---|---|---|
| Operation has no originating call or declared contract/design delta within scope | The selected sequence may be incomplete, another scenario/contract may justify it, or the operation may be unnecessary | Check scope and provenance, then `/mkl-uml-sequence-diagram` if needed |
| Attribute appears in no text | Either the specification is missing a step or the attribute is speculative | `/mkl-use-case-specifier` |
| Class is absent from the domain and undeclared as solution | Problem and solution are being silently mixed | Declare it, or `/mkl-uml-domain-modeler` |
| Entity discovered in robustness never reached the domain | Robustness delta was not applied; PDR should have caught it | `/mkl-uml-robustness-diagram` · `/mkl-pdr-review` |
| Relationship exists neither in domain nor as an operation requirement | Invented structure | Justify or remove it |

**A declared provenance category:** solution-space classes need not originate in the conceptual domain model. They arise here or in sequences. That is why they are explicitly declared rather than traced: their declaration *is* their provenance.

---

## The special case of solution classes

The source anticipates them and explains why:

> *"don't be surprised if you start to see lots of new classes appear on the static model that were never there on the domain model during analysis. That's because you're now identifying the solution space classes. By contrast, the domain model shows classes only from the problem space."*

Agile Development (2005) describes this stage's characteristic movement: *"moving the class model from a pure problem domain model into a solution space model that reflects the detailed technical architecture of the system."*

**Why mark them.** Any reviewer, including the CDR, must distinguish problem-driven structure from technology-driven structure. The source gives the deeper reason:

> *"base the key abstractions in the code on true statements about the problem domain, because the problem domain winds up being the most stable"*

If the spaces are mixed without marking, nobody knows which classes survive the next framework change.

**Declaration caution.** A legitimate solution class addresses a real technical need: persistence, presentation, framework coordination, or a required data structure. An **illegitimate** one is a renamed domain entity used to evade justification. Test it: if removing the stereotype would make you put it in the domain model without hesitation, it is not a solution class.

---

## Vocabulary drift

A common subtle case: the class **does** come from the domain, but under another name. `Order` in the domain and `Purchase` in the design are one class with a vocabulary problem, not two classes.

**Rule:** the domain-model name governs unless the change is declared and justified. If the design name is better, route the correction **back** through `/mkl-uml-domain-modeler`, never silently forward.

**Automatic-detection limitation.** Lexical similarity detects `VaccinationRecord` versus `VaccineRecord`, but **not** synonyms such as `Order` versus `Purchase`. Human judgment must identify those. An automatic check is useful for what it finds, not proof that no drift exists.

---

## Why this matters more here than in earlier skills

In earlier stages, an unsupported element is a local defect: an extra robustness controller can be seen and removed. Here its consequence is different.

This is **the last artifact before code**. Unsupported elements become classes, attributes, or methods someone will write, maintain, and test without knowing why they exist. The source marks the timing: *"It's your last chance to do so before coding."*

That is why the provenance matrix is a deliverable rather than an appendix.

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

