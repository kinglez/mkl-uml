<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Notation, style, and output contract

What to draw, omit, and why. Every rule includes its rationale; disagreements are declared together with the position followed. Source-verification statements preserve historical upstream research rather than claim a new check during translation.

---

## Three positions on activation bars

The available sources **disagree**:

| Source | Position | Quotation |
|---|---|---|
| **Course material** (Giraldo, ch. 7, guideline 6) | **Omit** | Translated: “We will omit this element because it adds little, can distract attention, and can visually complicate the sequence diagram.” |
| **Rosenberg & Stephens** | **Prefer omission; presence is not an error** | *"the focus of control is best switched off, as it tends to be something of a distraction"* (3871) · *"If focus of control starts to become a distraction, the easiest thing to do is just switch it off"* (3990) · *"this isn't necessarily an error, as some people do prefer to show these… a matter of personal taste"* (4451) |
| **Fowler**, *UML Distilled* | **Favors them** | *"Activation bars are optional in UML, but I find them extremely valuable in clarifying the behavior"* (1532) |

**Precision about “optional in UML.”** This is Fowler's statement, **not a standard clause**. Upstream research searched all UML 2.5 clause 17 and found **no statement declaring `ExecutionSpecification` optional or mandatory**. Notation clause 17.2.4.4 only explains drawing it: *"thin rectangles (gray or white) on the lifeline"*. Omission is therefore a **style convention supported by Fowler and the method**, not normative conformance.

**Skill default: omit.** Two sources prefer omission; the course requires it.

**Additional practical rationale, historically checked in PlantUML's issue tracker.** Issue [#1104](https://github.com/plantuml/plantuml/issues/1104) describes repeated activation cycles failing with *"Activate/Deactivate already done on A"*. Dividers (`==`, `...`) and spacing do not reset internal state. Other reported issues concern nested-group activations. When bars are needed, prefer **message-line `++`/`--` shorthand or `autoactivate on`** to manually paired commands crossing `else`, where reported defects occur. Issue status is historical, not newly checked here.

**Validator: warn on presence, never error for presence alone.** Rosenberg explicitly calls it a matter of taste (4451); blocking would overstate the source.

**An activation leak is an error.** An unclosed `activate`, or `deactivate` without an opening, on any execution path is malformed structure rather than style. `--con-activaciones` suppresses the usage warning, **not** leak detection.

**When the user requests bars**, include them and check balance **on every execution path**, not only total counts.

**Another practical reason** (3996): tools can make sequence diagrams hard to edit *"especially if the focus of control is visible"*.

---

## Activation balance: per path, not counts

Within `alt`, **each branch may deactivate, but only one executes**. A linear count can report two closes for one opening and invent an error.

The correct check **enumerates execution paths**, one operand per fragment, and verifies each independently:

- no `deactivate` on a participant without an open activation;
- no activation left open at the end;
- nested activation on one participant is legal in PlantUML, but each level needs closure **on every branch**.

This was an observed false positive in seed material: a linear scanner produced it; branch-aware checking eliminated it.

---

## Return messages: only when useful

All three sources **agree**:

- **Rosenberg** (3869): *"You normally don't need to draw a return arrow, except in special circumstances (e.g., to show an asynchronous return value)."* Technical reason: *"parameters can be passed back as arguments to the operation"*.
- **Fowler** (1536): *"I prefer to use them only where they add information; otherwise, they simply clutter things."*
- **Course material**, translated: “These response messages are omitted unless strictly necessary.”

**Draw an explicit reply when** its returned value is used in a later visible step or it distinguishes an error/exception outcome of the original synchronous call. For an **asynchronous completion**, model a later callback call or Signal with its own semantics, not a UML `reply` to an asynchronous call. The source's phrase “asynchronous return value” is informal practitioner terminology.

**Excessive returns are an anti-pattern.** The validator warns when their proportion exceeds its declared threshold. This remains a warning: many returns can be justified.

---

## Message types

- **Synchronous** (`->`): sender waits; default for application detailed design.
- **Asynchronous** (`->>`): sender continues. Fowler (1634-1640) explains filled/open arrowheads and cautions: *"I think that this arrowhead distinction is too subtle."* **Label asynchronous messages explicitly** as well.
- **Return** (`-->`): dashed line; UML `reply` returns outputs from a synchronous call and does not imply a reverse operation. Declare intent when tool notation is ambiguous.
- **Self-call:** legitimate for a class's own responsibility; several consecutive self-calls suggest an algorithm rather than collaboration.
- **Creation/destruction:** Fowler (1560-1562): creation arrow enters the participant box; **X** ends the lifeline. PlantUML: `create`, `destroy`.

---

## Combined fragments

`alt` for mutually exclusive courses, `opt` for optional behavior, `loop` for repetition. Fowler calls them *"interaction frames"* (1576), warning *"I find the interaction frames very heavy, obscuring the main point of the diagram"* (1630).

**Use fragments for specification-declared flows, not every imaginable condition.** The stopping criterion (1574):

> *"Treat sequence diagrams as a visualization of how objects interact rather than as a way of modeling control logic."*

**Mandatory labels:** `alt FA-01 <condition>`, `opt FE-02 <condition>`. Without identifiers, coverage cannot be mechanically verified and specification comparison becomes manual.

**Nesting** multiplies paths and reading difficulty. More than two levels suggests splitting the use case.

---

## Names

- **Name operation calls as operations:** specific infinitive or third-person verbs translatable to code identifiers. Name Signals as events, replies as outputs of the original call, and lifecycle messages by lifecycle intent. `check parking space availability` is useful; `process` says little; `doStuff()` adds implementation noise.
- **Full signatures are unnecessary.** Include parameter/type details only when distinguishing otherwise ambiguous operations.
- **Preserve `DR-XX` participant names.** Renaming across artifacts breaks traceability and is a finding.
- **Optional `_model` suffix for collisions.** Course material recommends it when Controller and Entity share a name; translated rationale: “distinguishing and importing them is sometimes impossible.” Particularly useful before code generation.

---

## Stereotypes and participants

| PlantUML keyword | Purpose | Alias prefix |
|---|---|---|
| `actor` | Use case actor | `ACT_` |
| `boundary` | Human or machine interaction interfaces: screens/forms, APIs, webhooks, message ingress, device adapters | `B_` |
| `control` | Actual controller classes: remaining 20% | `C_` |
| `entity` | **Only** domain-model classes | `E_` |
| `participant` · `database` · `queue` | Detailed-design infrastructure | `INF_` |

**Two frequently broken rules:**

1. **Infrastructure is not an Entity.** ORM, database connections, HTTP clients are legitimate. Course source, translated: “objects related to architecture and storage mechanisms will appear.” Declaring these as `entity` corrupts vocabulary and domain-closure checks.
2. **Do not repeat stereotypes in labels.** Keywords already draw icons; adding `<<boundary>>` duplicates information.

---

## PlantUML output contract

```
@startuml
' DS-XX - Sequence for CU-XX <name>
skinparam style strictuml
skinparam shadowing false
skinparam responseMessageBelowArrow true

<participants in order: actor, boundary, control, entity, infrastructure>

<basic-course messages>
alt FA-01 <condition>
  <alternate branch>
else basic course
  <continuation>
end
@enduml
```

- Start `@startuml`; end `@enduml`.
- All three `skinparam` directives are contractual: standard notation, reduced clutter, readable returns.
- **No `activate`/`deactivate`** unless explicitly requested.
- `==` dividers for useful phase separation.
- Use case text may appear as a `note`, but **the actual sweep uses the specification file**, not a pasted copy that can become stale.
- Filename: `caso_NN_secuencia.puml` (legacy compatible).

---

## When a sequence diagram is unsuitable

Fowler (1642-1648):

- Useful *"when you want to look at the behavior of several objects within a single use case"*.
- **Unsuitable for precise behavioral definitions:** *"they are not so good at precise definition of the behavior"*.
- **One object across many use cases:** use a state diagram.
- **Behavior across many use cases or threads:** use an activity diagram.

If the problem matches one of the last three cases, state that instead of producing a diagram that cannot answer it.

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

