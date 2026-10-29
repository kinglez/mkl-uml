# Operating, input and traceability contract

This contract applies to all eight MKL skills. It separates the artifact operation from the review workflow and the evidence available. Existing Spanish CLI flags and supported parser terms remain compatible; the modes below are agent workflow choices, not new CLI flags.

## Modes and operations

| Dimension | Value | Behavior |
|---|---|---|
| Workflow | standalone (default) | Complete the requested artifact or scoped review using supplied evidence |
| Workflow | MKL workflow (explicit) | Check the applicable cross-artifact handoff and formal gate evidence |
| Operation | generate/complete | Need a goal and enough behavior or responsibilities to construct the requested scope |
| Operation | review | Need the artifact being reviewed; report located findings and coverage |
| Operation | refactor | Need the artifact and intended correction; preserve supplied identity and constraints |
| Operation | validate | Need an input in the chosen validator's supported profile; distinguish syntax, local rules and heuristics |

A missing target blocks that operation. A missing predecessor makes only dependent checks unverified. Continue independent useful work. Ask for clarification only when missing information changes the requested result; do not require a full pipeline for a standalone diagram.

## Input matrix

| Skill | Minimum standalone evidence | Additional evidence for a full MKL handoff |
|---|---|---|
| Domain modeler | Business scope/concepts, or target domain model | Requirements and specified domain behavior |
| Use case diagram | Subject boundary and actor goals, or target diagram | Requirement/actor sources, domain vocabulary, CU registry |
| Use case specifier | Goal and behavior/draft, or target specification | Actor/CU diagram, domain, rules and acceptance sources |
| Robustness | Goal and specified flows, or target diagram | CU text, domain model, actor/interface context |
| PDR | Supplied preliminary-design artifact(s) for scoped checks | Robustness, CU text, domain and applicable scope/interface/review evidence |
| Sequence | Scenario and participants/responsibilities, or target sequence | CU text, robustness, domain and PDR evidence |
| Design class model | Design responsibilities/constraints, or target model | Domain, interaction calls, CU state requirements and design decisions |
| CDR | Supplied detailed-design artifact(s) for scoped checks | Classes, sequences, CU text and applicable domain, robustness, requirements, tests and human review evidence |

The CLI minimum may differ from a full review minimum. Sequence CLI requires `--secuencia`; class CLI requires `--clases`; PDR CLI requires `--robustez`; CDR CLI requires both `--clases` and `--secuencia`. Optional inputs enable dependent checks, not evidence that those checks occurred. Do not fabricate a file to satisfy a CLI.

## Coverage and acceptance

Use **checked** when the named check ran against sufficient evidence, **partial** when some applicable checks or paths remain unverified, and **blocked** when the target or indispensable evidence for that operation is missing. List executed tools and omitted checks with their reasons.

A supplied path is not sufficient evidence by itself. Empty files, comments, notes and unrecognized supporting structures do not establish coverage. Parse the usable artifact before marking its dependent checks as executed; an absent usable review target blocks its review. Pair every supplied use case with its applicable artifacts and evaluate local flow IDs within that use case. References to a flow in explanatory prose do not establish that the flow is implemented in an interaction fragment.

These coverage states are separate from formal gate dispositions: **Accepted**, **Accepted with rework verification**, and **Reinspection required**. Missing applicable evidence withholds acceptance (**Not fully verified**); an absent review target means **Not reviewed — entry criteria not met**. A machine result is a provisional input to a gate decision, never proof of semantic correctness or evidence of human participation. Document justified non-applicability rather than hiding missing checks.

Run a scoped review and recheck affected areas after correction. Fixed two-clean-pass/five-pass cycles and certificate bundles are not default requirements. Historical research/audit records in references are context, not instructions to repeat them. Reuse existing authorization for remediation or header generation. Review-only requests remain review-only.

## Vocabulary and semantics

| Origin | Closure requirement |
|---|---|
| Domain entity/value/property | Resolve to domain evidence or propose a domain delta |
| Actor | Resolve to an external participating role; supporting actors need not initiate |
| Boundary | Resolve to an interaction interface: screen, API, webhook, device port or adapter |
| Solution class | Resolve to a responsibility, architectural constraint or explicit design decision |
| Operation | Resolve to an operation call, contract, requirement or justified design decision |
| Signal/lifecycle/reply | Record the appropriate interaction semantics separately from ordinary operations |

A reply returns results of an earlier operation; a Signal can lead to a reception; creation/destruction has lifecycle semantics. Arrow style alone can be ambiguous. For mechanical provenance, annotate labels with `<<synchCall>>`, `<<asynchCall>>`, `<<reply>>`, `<<asynchSignal>>`, `<<createMessage>>`, or `<<deleteMessage>>`; explicit operation calls need a signature. Unannotated synchronous labels retain lexical matching for compatibility. Ambiguous asynchronous messages remain unverified. The tools are profile-specific parsers, not a complete UML metamodel validator.

A derived `/property` specifies derivability, not a storage strategy. Composition permits at most one composite owner at a time and allows detachment before composite deletion. Neither justifies an automatic database or permanent-lifetime policy. UML semantics are distinct from local BCE rules and heuristic quality checks. See [the bibliography](BIBLIOGRAPHY.md) for primary normative references.

## Identifier lifecycle

Use the project's existing ID scheme. Defaults are RF/RNF for requirements, CU for use cases, DR for robustness, DS for sequences, MC for class models, CP for tests, RN for rules, PDR/CDR for review records, and H for findings. FA/FE flow IDs are scoped to their parent CU; finding IDs are scoped to a review record. A full reference includes its scope, for example `CU-07/FA-02`.

- Identity is stable across renamed titles, declaration order, prominence and partial regeneration. Display numbering and PlantUML aliases are not traceability identity.
- Import existing IDs and the high-water mark before allocating. Keep a registry with stable business keys and active/retired status. Allocate above the reserved high-water mark, including retired IDs.
- Omission from a partial edit does not retire an artifact. Retire explicitly, retain its history, and never reuse its key or ID for a different artifact.
- Splits/merges receive new identities where needed and record predecessor/successor links. Existing unaffected artifacts retain their IDs. Resolve collisions explicitly; do not silently renumber.
- Without an existing registry, preserve observed IDs and mark new allocations provisional until the authoritative namespace is checked. Never imply that CU/DR/DS happen to share a number as proof of traceability: maintain explicit links.

The repository helper `tools/trace_ids.py` produces a JSON registry using only Python's standard library. It retains omitted keys, supports scoped namespaces and explicit retirement, and rejects collisions and inconsistent high-water marks. It writes to stdout; callers choose where to save the result. Installed skills can follow this contract manually without requiring the helper or sibling skills.

From the repository root, this executable example creates a new registry; the business key is illustrative. It is not an installation or a record of a project allocation:

```bash
python3 tools/trace_ids.py --prefix CU --key reserve-room
```

## Deliverables

Match the user's requested artifact and language. A code-only request can return code only; disclose material limitations in artifact notes when necessary. A scoped review needs findings and coverage, not an entire formal report. A formal handoff adds the applicable traceability, decisions, remaining risks and action ownership. Do not invent accepted decisions, owners, dates or test evidence.
