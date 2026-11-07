# Operating, input and traceability contract

Advanced reference for connecting stages or interpreting reviews. For daily use, start
with the [skill selector](STANDALONE.md). These rules apply to all nine skills.

## Modes and operations

**Standalone is the default:** complete the requested artifact or scoped review.
Use the full MKL workflow only when requested. These modes are agent behavior, not CLI flags.
Generation needs a goal and sufficient behavior/responsibilities. Review, refactoring
and validation need their actual target. Preserve scope and existing authorization;
a review-only request does not authorize changing its inputs.

Missing information blocks only the choice/check that depends on it. Continue useful
independent work and ask only questions that change the requested result.

## Input matrix

| Skill | Standalone input | Additional full-handoff evidence |
|---|---|---|
| Domain modeler | Business concepts/behavior or target model | Requirements and domain behavior |
| Use case diagram | Boundary/goals or target diagram | Actors, vocabulary and CU registry |
| Use case specifier | Goal/behavior or target specification | Rules, acceptance and related models |
| Robustness | Specified scenario or target diagram | CU text, domain and interface context |
| PDR | Supplied analysis targets | Robustness, specification, domain and applicable scope/review evidence |
| C4 architecture | Architecture question/drivers or views | Current analysis/PDR, quality scenarios and decisions |
| Sequence | Scenario/responsibilities or target sequence | Specification, robustness, domain and applicable PDR/architecture |
| Design class model | Responsibilities/contracts or target model | Domain, interaction calls, behavior and architecture |
| CDR | Supplied detailed-design targets | Classes, sequences, specification, applicable analysis/requirements/tests and human review evidence |

CLI minimums: sequence `--secuencia`; class `--clases`; PDR `--robustez`;
CDR `--clases` plus `--secuencia`. Optional inputs enable comparisons only when usable.
Never fabricate an artifact to satisfy a CLI. Supplied Spanish CLI flags remain compatible.

## Coverage and acceptance

- **checked:** the named check ran with sufficient evidence.
- **partial:** some applicable checks or paths remain unverified.
- **blocked:** the target or indispensable evidence is missing.

Empty files, comments, notes and unrecognized support do not establish completed checks.
Parse usable evidence first. Pair every supplied use case with its applicable artifacts;
scope local flows by their CU. A label or prose reference alone is not implemented behavior.
Report executed tools and omitted checks with reasons.

Formal dispositions are separate: **Accepted**, **Accepted with rework verification**,
or **Reinspection required**. Missing applicable evidence means **Not fully verified**;
a missing review target means **Not reviewed — entry criteria not met**. Machine results
are provisional evidence, not human participation or formal approval. Explain justified
non-applicability. Recheck corrected scope; fixed multi-pass counts/certificates are not required.
Historical audits are records, not instructions to repeat their ceremonies.

## PDR to detailed-design handoff

Keep the reviewed CU/DR/flow scope, input versions, checks/limits, findings and correction
evidence, remaining constraints and technical recommendation in the PDR record.
Separate JSON manifests/hashes are optional; record actual formal acceptance separately.

The next stage reads that record, matches current inputs and re-examines changed sources
or unresolved blockers. A closed finding needs correction-verification evidence; a clean
CLI result, matching hash or missing finding list is not a substitute. Reopen only the
affected scope. Missing PDR evidence limits its dependent transition, not unrelated
standalone tasks. Scoped technical work may proceed on a documented basis while formal
acceptance remains unverified.

## Architecture and detailed-design handoff

Requirements may come from any supplied medium; no PRD or filename is mandatory.
Separate confirmed functions/quality scenarios, assumptions and open choices. Existing
code shows current behavior, not automatic agreement on intended behavior.

When architecture is requested, carry selected views/previews, sources/scope, alternatives
and costs, data/dependency ownership, quality strategies and detailed-design constraints.
Context/container views normally explain a system; add other views for a real question.
Reuse existing architecture for bounded work.

Sequence/class design reads current architecture before dependent choices: map
responsibilities to interfaces/classes, preserve communications, ownership and failure/
quality constraints. Stale evidence or an architecture-changing open question blocks
its dependent choice until rechecked. CDR manually compares actual design and architecture;
its CLI does not parse C4. The optional C4 record checks a local profile and declared
links/consistency, not design adequacy or achieved quality.

## Vocabulary and semantics

Domain elements resolve to domain evidence or a proposed delta. Actors are external
participating roles; supporting actors need not initiate. Boundaries represent actual
interaction interfaces. Solution classes and operations need a responsibility, contract,
requirement or justified design decision.

Keep replies, Signals/receptions and creation/destruction distinct from operation calls.
For mechanical provenance use `<<synchCall>>`, `<<asynchCall>>`, `<<reply>>`,
`<<asynchSignal>>`, `<<createMessage>>` or `<<deleteMessage>>`; operation calls need
a signature. Unannotated synchronous labels retain lexical matching; ambiguous async
messages remain unverified. Parsers check profiles, not the complete UML metamodel.

Derived `/property` means derivable, not a storage/caching policy. Composition permits
at most one composite owner at a time and detachment before composite deletion;
it does not imply permanent attachment or a database choice. Separate UML semantics,
local BCE conventions and heuristics. See the [bibliography](BIBLIOGRAPHY.md).

## Identifier lifecycle

Keep the project's scheme. Defaults: RF/RNF requirements, CU use cases, DR robustness,
DS sequences, MC class models, CP tests, RN rules, PDR/CDR reviews and H findings.
FA/FE IDs belong to their CU; findings belong to their review. Write scoped references
such as `CU-01/FA-02`. Similar numbers, display order and aliases are not traceability.

- Preserve identity through renaming, reordering and partial regeneration.
- Import existing keys, IDs and the reserved high-water mark, including retired IDs.
  Allocate above it; retain a registry with stable keys and active/retired status.
- Omission from a partial edit does not retire anything. Retire explicitly, keep history,
  and never reuse a retired key/ID for a different identity.
- Splits/merges receive needed new identities and predecessor/successor links.
  Resolve collisions explicitly; preserve unaffected items.
- Without an authoritative registry, preserve observed IDs and mark new ones provisional.

The optional [registry helper](../tools/trace_ids.py) retains omitted keys, scoped
namespaces and retirement history; it writes JSON to stdout. Installed skills can follow
the same rules manually without that helper or sibling skills.

## Deliverables

Match the requested artifact and language. A small/code-only task needs no formal report
bundle; a scoped review needs findings and coverage. Formal handoffs add applicable
traceability, decisions, risks and action ownership. Do not invent approval, participants,
owners, dates or test results. Reuse existing authorization for corrections/header generation.
