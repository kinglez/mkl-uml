# MKL UML workflow assessment

This is an English publication adaptation of the workflow assessment performed on **MKL UML v1.0.2**, commit `fb519f3bb2c0aff48dc655be4a15ddeb56ec60d4`, on 2026-10-29. It evaluates the workflow definition; the example's execution and technical review have their own evidence in [VALIDATION.json](VALIDATION.json), [PDR](05-pdr/PDR-01.md) and [CDR](08-cdr/CDR-01.md).

**Conclusion:** the workflow provides a coherent path from requirements and use case analysis through object collaboration, detailed classes and implementation handoff. Its stages have distinct responsibilities, its two reviews have evidence boundaries, and findings can return to the appropriate source. The assessment found no fundamental Critical/Major workflow defect that invalidated that structure.

The workflow supports SOLID-oriented design. Completing eight stages, rendering diagrams and obtaining successful validator exits do not establish SOLID by themselves. The useful improvements are repeatable handoff records, explicit change impact and concrete design probes, rather than replacement of the eight-stage structure.

## Stage contracts and feedback

The assessment read all eight skill entry points and the relevant operating, methodology, PDR/CDR, behavior-allocation, provenance, test-derivation and state-modeling references. Source links below refer to repository files, without machine-specific paths or line-number assumptions.

| Stage | Evidence that should be produced | Assessment |
|---|---|---|
| 1. Domain model | Supported concepts, relationships/cardinality meanings and unresolved questions | Separating conceptual vocabulary from implementation design is appropriate. Extracting nouns alone is insufficient. |
| 2. Use case diagram | System boundary, external roles, user goals and stable CU identities | Goals belong here; detailed behavior belongs in the textual specification. Genuine machine/supporting roles can participate. |
| 3. Use case specification | Trigger, preconditions, basic/alternative/exception actions and observable postconditions | Branch anchors, conditions, actions and resumption/termination create a usable comparison baseline. |
| 4. Robustness analysis | Boundary/control/entity responsibilities and correspondence with text/data | Analysis controls remain logical responsibilities; they are not mandatory implementation Controller classes. |
| 5. PDR | Versioned cross-artifact examination, findings and dispositions | It is an analysis handoff. Review coverage, a technical recommendation and an authorized formal decision are distinct. |
| 6. Interactions and tests | Collaboration with message semantics, operation allocation and outcome-based test design | Receivers acquire justified operations. Dynamic and static designs should evolve together. |
| 7. Design class model | Typed state, operations, relationships and their origins | Technical constraints/contracts/decisions are legitimate origins; every technical detail need not become a business flow step. |
| 8. CDR | Scenario realization, allocation, cohesion, requirement/test traceability and feasibility | It supports a technical handoff judgment. Missing applicable human evidence prevents unconditional formal acceptance. |

Sources: [input matrix and coverage contract](../../docs/OPERATING_CONTRACT.md), [methodology](../../docs/MKL_METHODOLOGY.md), [CDR rules](../../skills/mkl-cdr-review/references/cdr-rules.md).

## Existing strengths

1. **Scope determines the required evidence.** Standalone work does not require manufacturing an entire preceding pipeline. An explicitly requested full review checks its applicable supporting inputs. A missing target blocks that operation; absent comparison material leaves the relevant layer unverified. [Operating contract](../../docs/OPERATING_CONTRACT.md).
2. **Mechanical output, semantic coverage and acceptance remain distinct.** Empty material, comments or flow-ID repetition do not replace actual evidence. `checked`, `partial` and `blocked` describe coverage separately from gate disposition. [Review protocol](../../skills/mkl-cdr-review/references/review-protocol.md).
3. **Corrections return to their origin.** New domain meaning requires a domain delta; technical state/operations may originate in architecture, configuration, contracts or design decisions. Genuine missing business behavior belongs in the use case; a technical member does not automatically justify inventing that behavior. [Provenance rules](../../skills/mkl-uml-design-class-model/references/provenance-rules.md), [PDR guidance](../../skills/mkl-pdr-review/references/pdr-guidelines.md).
4. **Allocation examines rule/state ownership.** One analysis Control may map to multiple operations. Calls, replies, signals, creation and destruction have different semantics; replies do not manufacture reverse methods. [Behavior allocation](../../skills/mkl-uml-sequence-diagram/references/behavior-allocation.md), [message provenance](../../skills/mkl-uml-design-class-model/references/provenance-rules.md).
5. **Tests derive from outcomes.** Preconditions, stimuli and observable results matter. Controller-responsibility coverage and branch coverage are separate; one test per internal message would not establish behavior. [Test derivation](../../skills/mkl-uml-sequence-diagram/references/test-derivation.md).
6. **Identities and roles remain accountable.** Stable/retired/split/merged IDs support change traceability. Switching skill names is not independent review; generating declarations is not actual inspection. [ID contract](../../docs/OPERATING_CONTRACT.md), [review roles](../../skills/mkl-cdr-review/references/review-protocol.md).

These are workflow safeguards. Project artifacts and review records must show that they were actually applied.

## Historical handoff gap: W-01, Minor

At the assessed v1.0.2 baseline, the generic stage-6 prompt in `docs/EXAMPLES.md` named requirements, specification, robustness and domain inputs but omitted the PDR record. The [operating contract](../../docs/OPERATING_CONTRACT.md) and [sequence skill](../../skills/mkl-uml-sequence-diagram/SKILL.md) already required PDR evidence for the full workflow. Separate chats could therefore lose unresolved analysis findings or entry conditions when following that prompt literally.

This was a prompt-reproducibility gap, rather than demonstrated failure of the gate itself: the existing fifth-stage explanation and README already required resolution of findings affecting the next stage. The reference example's [replay prompt](HOW_TO_REPLAY.md#6-interactions-operation-allocation-and-test-design) explicitly reads `05-pdr/PDR-01.md`, checks its conditions and records the technical basis for proceeding. Keep any copied generic prompt aligned with the contract for the revision being used.

## Practical improvements

| Area | Remaining practical risk | Small, useful addition | Evidence that it helps |
|---|---|---|---|
| Repeatable handoff | Required information is spread across references; different contributors may hand off different subsets. | A project-level manifest records scope, input versions/hashes, outputs, checks, findings, gaps and transition basis. | A new reviewer can locate the same baseline and open issues from the record and files. |
| Incremental changes | Stable IDs exist, but a project must identify which reviews become stale after an upstream change. | Record changed rule/contract → affected CU/DR/DS/MC/CP → reinspection → execution evidence. | Unchanged identities remain stable, and only justified affected scope is revalidated. |
| State and quality attributes | The workflow admits state/architecture sources but does not automatically supply every risk-specific artifact. | Add state tables, contracts or decisions when shared state, retries, idempotency, atomicity, external effects or measurable quality scenarios require them. | State transitions, duplicate requests, concurrency, failure/recovery and performance have observable criteria. |
| SOLID assessment | Cohesion and provenance help, but the five principles require actual change and substitution evidence. | Add applicable responsibility, extension, shared-contract, client-capability and import-direction probes during design/CDR. | Concrete changes or replacements preserve the specified behavior and reveal their true impact. |

The absence of a dedicated state-machine or deployment-diagram skill is not itself a defect in this use-case-driven object analysis/design scope. A project with distributed transactions, reliable delivery or performance targets still needs the corresponding design and verification evidence. Sources: [incremental review](../../skills/mkl-cdr-review/references/review-protocol.md), [state-model boundary](../../skills/mkl-uml-sequence-diagram/references/notation-rules.md), [quality/architecture checks](../../skills/mkl-cdr-review/references/cdr-rules.md).

## What a SOLID claim needs

SOLID concerns responsibilities, reasons for change, behavior contracts, clients and source dependencies. An interface icon or runtime call arrow supplies only part of that evidence. Principle background: [Robert C. Martin's explanation](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html) and [Liskov/Wing's author-institution summary](https://www.cs.cmu.edu/afs/cs/project/calder/www/fmdp.html).

| Principle | Workflow support | Additional project evidence |
|---|---|---|
| S — single responsibility | Allocation keeps rules/state together; CDR examines cohesion and independent reasons for change. | Explain responsibility and change sources; compare an algorithm change with a storage/representation change. |
| O — open/closed | Justified strategies, contracts and adapters can enter detailed design. | Select the variation to protect and demonstrate a new rule's actual modification scope. A Strategy class alone is insufficient. |
| L — substitution | Generalizations/realizations preserve an explicit common contract. | Check common preconditions, postconditions, errors and invariants for each replacement with shared cases. |
| I — interface segregation | Signatures and collaborators expose client dependencies. | Show which actual client needs each capability and which unrelated methods it can avoid. Interface size alone is insufficient. |
| D — dependency inversion | Technical contracts need ownership and design rationale. | Identify high-level policy, low-level adapters, contract ownership and source import direction. Runtime calls do not establish source dependency direction. |

The order-pricing example applies these checks in [SOLID.md](07-class-model/SOLID.md), the [extension exercise](CHANGE_IMPACT.md#4-controlled-extension-half-off-capped-at-cny-2000) and [independent CDR](08-cdr/CDR-01.md). Finite cases support the selected scenarios; they do not issue a universal SOLID certificate.

## What the complete example demonstrates

The example preserves the full chain `RF/RN → CU/FA/FE → DR responsibility → DS call/completion → class member → CP expected result`. Independent PDR corrected an unsupported business policy. Detailed-design examination corrected nested-break semantics; independent CDR corrected association multiplicity and full-lifeline break coverage. A registered discount extension challenges the design without changing the protected quote workflow.

The reference implementation and literal acceptance oracle provide additional behavioral evidence. The [review history](CHANGE_IMPACT.md) and [published validation record](VALIDATION.json) keep actual findings, run results and acceptance limits distinguishable. Formal human/business acceptance remains **Not fully verified**.
