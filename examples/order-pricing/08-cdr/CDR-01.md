# CDR-01 — detailed-design review

**Historical technical disposition: Ready for the fictional technical example and design handoff.** CDR-01-F01 and CDR-01-F02 were independently closed. **Formal human/business acceptance: Not fully verified.**

This is a publication adaptation of the actual AI technical review begun on 2026-10-29 and completed on 2026-10-30. Paths, role labels and presentation have been normalized for the repository. The published files are not claimed to be byte-identical original review evidence or signed records. Machine-specific command logs and original hash manifests are excluded; [VALIDATION.json](../VALIDATION.json) records the published edition's executed checks. Local reruns write fresh logs under `validation/latest/`.

## Scope and participants

The review covers **CU-01 / DR-01 / DS-01 / DS-02 / MC-01**, including requirements, independent oracle, member/operation provenance, generated declarations, test design and the runnable reference implementation. DS-01 realizes the user goal. DS-02 observes RNF-02 and does not claim business-flow coverage.

| Actual role | Evidence boundary |
|---|---|
| Design author (AI) | Prepared and corrected the detailed model. Its checks are author evidence. |
| Reference implementation author (AI) | Implemented the code and tests; actual execution supports technical feasibility. |
| Independent technical reviewer (AI) | A different agent examined the detailed model/code, recorded findings and verified corrections. The same reviewer also performed the earlier PDR. |
| Coordinator (AI) | Located the earlier nested-break scope error and coordinated correction/handoff. |
| Human/customer/business decision maker | No such acceptance or sign-off is evidenced. Permission to create a teaching example does not approve fictional policies for production. |

Reviewed sources include the [requirements and oracle](../00-input/), [PDR](../05-pdr/PDR-01.md), [specification](../03-spec/CU01-quote-cart.md), [robustness correspondence](../04-robustness/correspondence.md), both [interactions](../06-interactions/), [operation delta](../06-interactions/operation-delta.md), [test plan](../06-interactions/test-plan.md), [design decisions](../06-interactions/DESIGN_DECISIONS.md), [classes](../07-class-model/classes.puml), [member provenance](../07-class-model/provenance.md), [SOLID assessment](../07-class-model/SOLID.md) and [reference implementation](../09-reference-implementation/README.md).

## Mechanical results and actual declaration inspection

The original independent CDR runs used both sequences and every applicable comparison input: classes, specification, domain, robustness, requirements and test plan. Both the initial and corrected runs exited **0**, with **zero errors and ten warnings**. The initial green result did not detect the two semantic findings below.

The final model contains **17 classifiers, 25 explicit attributes, 16 significant operations, zero receptions and 24 relationships**. The real header generator also exited **0**, producing [headers.java](headers.java). The independent reviewer then compared the declarations against the model and Python implementation; generation alone was not counted as inspection.

The [header-inspection record](header-inspection.md) covers all modeled declarations, parameter/result types, generic Map/Optional forms, the association-derived Cart collection and six realizations. It retains translation limits for tuple/read-only behavior, Python integer precision and Boolean exclusion, aware UTC, aliases, constructors and exception semantics. These Java-like declarations are inspection aids, not executable production Java or a fidelity certificate.

## Findings and independent closure

### CDR-01-F01 — multiplicity contradicted shared line values

| Field | Record |
|---|---|
| Category / severity / priority | Inconsistent / Moderate / P2. |
| Initial defect | `Cart "1" --> "0..*" CartLine` requires each CartLine instance to relate to exactly one Cart. The design note and implementation permit immutable line values to be shared. Ordinary association does not remove the source-end multiplicity constraint. |
| Demonstration | The independent reviewer constructed and successfully validated two Carts referencing the same CartLine instance. The [initial class illustration](../review-history/classes-initial.puml) retains the contradictory model. |
| Correction | Both association ends are `0..*`. A line value can be unused or shared; an unvalidated Cart can contain zero lines. `Cart.validate()` still requires a nonempty valid cart. |
| Independent verification | The reviewer reread model/provenance/code, inspected the class render and regenerated headers. The derived collection comment now carries source multiplicity `0..*`. Business rules, target multiplicity, code behavior and identifiers were unchanged. |
| Final status | **Closed**, verified on 2026-10-30. |

### CDR-01-F02 — break frames did not cover the enclosing lifelines

| Field | Record |
|---|---|
| Category / severity / priority | Not conforming to the specified UML notation / Moderate / P2. |
| Initial defect | After the nested-break correction, break operands were outermost but their rendered frames still enclosed only the few left-side participating lifelines. |
| Governing meaning | [OMG ISO/IEC 19505-2, §14.3.3](https://www.omg.org/spec/UML/ISO/19505-2/PDF) defines break scope and all-lifeline coverage. Moving a break outside a nested fragment does not by itself fix narrow coverage. |
| Historical illustrations | The [initial sequence](../review-history/sequence-initial.puml) retains the earlier nested-scope error; the [intermediate sequence](../review-history/sequence-before-frame-correction.puml) retains the narrow outer frames. These are normalized historical illustrations. |
| Correction | All **12** terminating breaks are at the outer quote-interaction level. Each contains an accurate note spanning the actual first/last participants, covering all **nine** lifelines. No fake call is added. PriceQuote construction is an internal completion action and the result is returned by value, without an artificial early-created lifeline. |
| Lifecycle and IDs | Former explicit creation message **DS-01-M10 is retired**, not reused. The completion note, RF-08, AD-01, operation delta and actual constructor retain successful result creation and invariant checks. |
| Independent verification | The reviewer reread guards, actions and termination, checked fragment nesting, inspected the actual SVG/PNG and measured that every break frame covered all nine lifeline centers. Construction remains after all refusal and policy checks. |
| Final status | **Closed**, verified on 2026-10-30. |

The earlier nested-break error was a separate author correction. A break inside a loop/optional fragment cannot be explained by a legend as an unconditional exit from the whole quote. [IBM's sequence-diagram explanation](https://developer.ibm.com/articles/the-sequence-diagram/) describes this enclosing-fragment distinction. The author also recorded an installed-renderer failure for `note across`; the supported explicit endpoint note supplies the actual full-width rendering. A renderer limitation does not alter UML semantics.

## Ten warning dispositions

The original final CDR's ten warning instances were retained and individually examined. None required further correction in the selected scope after F01/F02 were closed.

| Warning | Independent semantic disposition |
|---|---|
| Rule 3: generic `QuoteRequestPort.handle` name | Discharged in context: the named machine port, request/result schema, AD-05/07 and actual adapter define concrete decoding, validation and encoding responsibilities. |
| Rule 7: Cart has no explicit attribute | Discharged: the named association supplies its one stored tuple collection. No duplicate `lines` attribute is needed. F01 corrected the real multiplicity defect. |
| Rule 7: CartLine has attributes and no operation | Discharged: it is an immutable requested value. Cart owns collection/quantity validation and totaling; no independent line lifecycle was missing. |
| Rule 7: Product has attributes and no operation | Discharged: it is a detached trusted catalog value. Lookup/validation provenance and Cart arithmetic are explicit. Dummy operations would add no responsibility. |
| Rule 7: PriceQuote has attributes and no ordinary operation | Discharged: actual constructor/`__post_init__` behavior enforces result invariants. An ordinary-operation view need not invent a constructor method. |
| Rule 7: Refusal has attributes and no operation | Discharged: it is a technical exception/result payload with an explicit reason, propagation and boundary-mapping responsibility. |
| Rule 6: Refusal is not a sequence lifeline | Discharged: exception replies and boundary mapping use the payload. A propagated value need not receive a fake operation or become an interacting lifeline. |
| Rule 5: RNF-03 has no matching class vocabulary | Discharged by runtime/import evidence: standard-library-only code actually passed on Python 3.9.6 and 3.14.7. No compatibility class was required. |
| Rule 5: RNF-05 has no matching class vocabulary | Discharged by actual narrow protocols, source dependency inspection and working independent lookup/resolver substitutes. |
| Rule 1: wrapped `Return\nrefusal` label is not matched in the test plan | Discharged as a lexical mismatch. Operation allocation, executed oracle refusals and CP-31–40 cover explicit failure/no-quote outcomes across all seven FE paths. |

Reply/call proportions and the 256-path enumeration cap were also treated as tool limits rather than proofs of a God Object or exhaustive coverage. Boundary renaming is explicitly mapped. DS-02 cannot discharge DS-01's user-goal branches.

## Semantic coverage

| Evidence layer | Independent result |
|---|---|
| Scenario realization and alternatives — rules 10/9 | All seven basic steps, three FA paths and seven FE paths have actual collaboration, guards, outcomes and continuation/termination. Refusal bypasses successful completion. |
| Operation allocation — rule 8 | The nine maintained DS-01 calls and DS-02 snapshot/handle calls map the sixteen significant declarations through receivers or their interface realizations. Replies add no reverse operations; M10 retirement is explicit. |
| State and responsibilities — rule 7 | All seventeen classifiers and modeled state have requirement, contract or design-decision origins. Immutable values, rule owners, coordinator, narrow ports and adapters have justified roles. F01 is closed. |
| Real collaboration — rule 6 | Trusted lookup/configuration, eligibility, calculation, invariant checks and refusal propagation match the reference code. No unexplained order or persistence capability appears. |
| Bidirectional traceability — rule 5 | RF-01–10, RN-01–08 and RNF-01–05 connect through CU/DR/AD/DS/MC to observable CP or runtime evidence. Technical CP-31–44 remain distinct from the independent CP-01–30 oracle. |
| Implementer assessment — rule 4 | Actual AI implementation and independent execution support bounded feasibility. Human implementing-team, architecture and business acceptance remain unverified. |
| Signatures and headers — rules 3/2 | Individual arguments/results, time, exact integer money, Optional absence, map schema and factory aliases resolve through model, interface and code. Declarations received independent AI inspection with explicit conversion limits; human header inspection is not claimed. |
| Test design/execution — rule 1 | Every selected basic/FA/FE outcome has a test criterion and executed evidence. The test plan itself was not counted as execution. |
| PDR and trust obligations | The catalog boundary, explicit time, configuration-before-calculation, no mutation/fallback and PDR's unresolved negative-minimum policy are preserved. |

## Runtime, contract and SOLID evidence

The [code audit](CODE-AUDIT-01.md) records the independent source examination. Original runs on Python **3.9.6** and **3.14.7** passed **15 unittest methods**. One method contains **30 independent oracle subcases**, each called twice with literal result and complete request/fixture/catalog equality checks. They are not thirty test methods. Model-only corrections did not alter the reviewed code or expected results.

The shared pure-policy vectors cover subtotal 0, 333 and 25500 for no discount, fixed 3000, percentage 1000 basis points and fixed 50000. The capped-half extension adds literal discounts 0, 166 and 2000 on the same inputs. Eligibility remains outside pure calculation; a low-subtotal policy test does not waive a Coupon minimum.

SOLID was examined through responsibilities, protected changes, common behavior, client capabilities and source imports. The coordinator has no discount-kind switch and imports no concrete adapter/registry. External registration supplies the additional strategy. Independent minimal Product/Coupon/resolver substitutes work, while caller-injected catalog data remains nonauthoritative. See the retained [independent probes](independent_code_probes.py) and [SOLID assessment](../07-class-model/SOLID.md).

This demonstrates one supported extension point and finite substitution evidence. It is neither a historical zero-edit Git-diff proof nor a universal OCP/LSP certificate. The technical probe does not silently approve a third Coupon kind in the business baseline.

## Final boundary

The original fictional technical example was ready for handoff after independent closure of both findings and all ten warning dispositions. The repository edition is a publication adaptation with its own rerunnable verification record; replacing old hashes alone would not recreate the original review.

Formal human/business acceptance remains **Not fully verified**. Negative-minimum acceptance/refusal, simultaneous-fault precedence, production time authority and excluded production capabilities remain outside the verified policy scope. Changed inputs require impact analysis and actual affected-scope review before a replacement handoff baseline.
