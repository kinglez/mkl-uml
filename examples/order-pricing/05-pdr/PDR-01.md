# PDR-01 — preliminary-design review

**Historical technical disposition: Ready for detailed design.** PDR-01-F01 was corrected and independently rechecked before stage 6 began. **Formal human/business acceptance: Not fully verified.**

This publication summary adapts the actual AI technical review performed on 2026-10-29. An analysis author (AI) prepared the artifacts; a different, independent technical reviewer (AI) examined and verified the correction. No customer, human architect or designated business decision maker approved the fictional policies. The English publication normalizes paths and presentation, so these files are not presented as byte-identical originals or signed review records. Machine-specific logs and original hash manifests are excluded. The published edition's executed checks are recorded separately in [VALIDATION.json](../VALIDATION.json); rerunning the verifier creates local logs under `validation/latest/`.

## Scope and reviewed material

The review covers **CU-01 Quote cart** and **DR-01**, before detailed design:

- [Requirements](../00-input/requirements.md), [independent oracle explanation](../00-input/ACCEPTANCE_ORACLE.md) and [literal oracle cases](../00-input/acceptance-oracle.json).
- [Conceptual domain model](../01-domain/domain.puml) and [glossary](../01-domain/glossary.md).
- [Use case diagram](../02-use-cases/use-cases.puml) and [actor/goal mapping](../02-use-cases/actor-goal-map.md).
- [Use case specification](../03-spec/CU01-quote-cart.md) and [interface contract](../03-spec/interface-contract.md).
- [Robustness diagram](../04-robustness/robustness.puml) and [behavior/data correspondence](../04-robustness/correspondence.md).

The selected goal is read-only pricing from a trusted internal catalog. Checkout, payment, stock, persistence, external integration and production authentication are outside its boundary. Analysis Controls describe responsibilities; they do not prescribe seven implementation Controller classes.

## Finding and verified correction

### PDR-01-F01 — unsupported negative-minimum rejection

| Field | Review record |
|---|---|
| Severity / priority | Major for this analysis handoff / P1. |
| Initial defect | The glossary, FE-07 and CA-13 required rejecting a Coupon minimum solely because it was negative. The fixed requirements and independent oracle did not define that policy. |
| Consequence | Detailed design and tests could inherit an invented restriction on the accepted business domain. The 30 literal oracle cases would not expose it because they deliberately contain no negative-minimum case. |
| Historical illustrations | [Initial glossary](../review-history/pdr-initial-glossary.md) and [initial specification](../review-history/pdr-initial-specification.md). These retained illustrations have publication-normalized presentation. |
| Correction | Keep minimum values as integer cents; remove the unsupported sign-based refusal from the glossary, FE-07 and CA-13. State explicitly in the interface contract and scope limits that negative-minimum acceptance/refusal is undefined in this bounded baseline. |
| Independent verification | The reviewer reread the changed declarations and linked flows, compared them with the preserved baseline, and reran PDR with the specification, robustness diagram, domain model and use case diagram. The business requirements and oracle were unchanged. No stage-6 design existed at that point. |
| Final status | **Closed.** The correction removes an invented rejection rule; it does not introduce a new requirement to accept negative minima. |

Details are retained in the [correction handoff](../03-spec/pdr-corrections.md). Quantity bounds, nonnegative Product prices, fixed-discount limits, percentage floor, exact-expiry refusal, no fallback and read-only behavior remain unchanged.

## Tool diagnostics and semantic adjudication

| Actual historical observation | Independent disposition |
|---|---|
| Initial PDR CLI exited **1**, reporting ten alternative/exception flows without behavior. | These were representation false positives. Each compact row already had a trigger, action and resumption/termination. The parser recognizes numbered System steps such as `FA-01.1`; the specification was expanded into equivalent numbered details. This was a format correction, separate from F01. |
| Corrected PDR CLI exited **0**, with zero behavior errors, zero non-domain entities and zero BCE syntax violations. | Accepted as mechanical evidence for the supported profile. The reviewer also compared all three FA and seven FE details with their original meaning. Numbering alone does not prove completeness. |
| Five no-attribute warnings, one for each conceptual domain class. | Discharged by the chosen conceptual view, the glossary and the field-by-field correspondence. Required values and their destinations are explained outside the diagram. Attributes were not added simply to suppress the heuristic. |
| Approximate highlighter coverage was **100%**. | Lexical evidence only. The real F01 defect passed this metric. |
| The corrected CLI proposed `ACCEPTED WITH REWORK VERIFICATION`. | A tool recommendation, not formal acceptance or a substitute for the semantic review. |

All existing CU/FA/FE/RF/RN/RNF/CA identities and all resume/termination positions were preserved. The documented shared refusal/no-quote/no-mutation postconditions were made explicit in the numbered rows; no new actor, goal, entity or failure precedence was introduced.

## Semantic coverage

| Check | Result and evidence |
|---|---|
| Scope and requirement fidelity | RF-01–RF-10 and RN-01–RN-08 preserve CNY integer cents, caps, floor, zero prices, explicit UTC evaluation, exact expiry, explicit refusal and read-only quoting. F01 was closed before handoff. |
| Actor and system boundary | Shopper is the external actor for one user goal. The trusted catalog is internal setup, not an invented external actor or separate user goal. |
| Domain closure | Cart, CartLine, Product, Coupon and PriceQuote in DR-01 resolve to the same five domain concepts. A request port and refusal reason do not force additional domain entities. |
| BCE discipline | The actor communicates through the named boundary; controls mediate relevant entity access. The diagram contains no forbidden actor/entity, boundary/entity or entity/entity link, and no premature operation-call or lifeline notation. |
| Basic behavior | Seven steps cover request, validation, trusted lookup, total, no-Coupon discount, invariant-preserving completion and observable return. |
| Successful alternatives | FA-01 caps fixed discounts; FA-02 uses integer floor; FA-03 retains a valid nonempty zero-priced Cart and still checks any selected Coupon. A zero subtotal does not waive a positive minimum. |
| Exceptions | FE-01–FE-07 have actual guards, refusal behavior, termination and corrected-new-request recovery. No refusal path produces a successful quote or silently falls back to full price. |
| Data and trust | Product identity/quantity originate in the request; price and Coupon definitions originate in trusted setup. Currency, time, rule parameters, totals and result fields have explicit data paths in the correspondence table. |
| Observable contracts | Success fields and failure/no-quote results are specified. Request, catalog and Coupon state preservation remain downstream execution obligations at the PDR stage. No fake empty Order repository is prescribed. |
| Quality constraints | RNF-01–RNF-05 preserve the extension requirement, determinism, Python/stdlib constraint, shared policy contract and small collaborator interfaces. Their actual enforcement requires later design/code/test evidence. |
| Formal participation | Missing human/customer/business acceptance remains explicitly unverified; it is not treated as a technical diagram defect or filled in by an AI role. |

### Independent oracle correspondence

| Cases | Preserved behavior |
|---|---|
| CP-01–05 | No Coupon, fixed 3000, percentage 1000 basis points, capped 50000 and 333-cent rounding. |
| CP-06/07 and CP-27/28 | One cent below and exactly at both Coupon minima; eligibility uses `<`, not `<=`, for refusal. |
| CP-08/09 | Exact expiry refuses; one microsecond before expiry remains eligible. |
| CP-10 | A nonempty zero-priced Cart is valid and differs from an empty Cart. |
| CP-11–16 and CP-29 | Quantity 99 is valid; out-of-range, Boolean and fractional quantities refuse. |
| CP-17–19 | Empty Cart, unknown Product and unknown Coupon refuse explicitly. |
| CP-20–23 | Invalid fixed/rate configurations refuse before calculation; none settles the negative-minimum policy. |
| CP-24–26 | Unsupported currency refuses; percentage endpoints 0 and 10000 remain valid. |
| CP-30 | At most one Coupon; the malformed-array representation and reason spelling are adapter conventions. |
| Every CP | Later execution must compare literal results, repeat at the same instant and verify unchanged inputs/catalog state. The PDR did not claim these tests had already run. |

## Handoff obligations

### Maintained detailed-design handoff

This compact handoff applies the current workflow guidance to the maintained example. It preserves the historical semantic review above; the English publication baselines identify the current files rather than reusing original local hashes.

| Field | Recorded basis |
|---|---|
| Scope | PDR-01; CU-01 / DR-01; basic steps 1–7, FA-01–FA-03 and FE-01–FE-07. |
| Reviewed baseline | Requirements baseline 1 and the maintained analysis artifacts, pinned by [analysis.json](../handoffs/analysis.json). The current validator snapshot and execution are in [SKILL_SOURCE.json](../SKILL_SOURCE.json) and [VALIDATION.json](../VALIDATION.json). |
| Checks and limits | Vocabulary, BCE, flows, data origins and the independent expected values were examined as recorded above. Mechanical recognition does not establish semantic completeness or human participation. |
| Finding/action state | PDR-01-F01 is closed: the unsupported negative-minimum mandate was removed and independently reinspected. The negative-minimum policy remains outside the bounded baseline; it is not a deferred in-scope blocker. No open in-scope blocking analysis finding remains. |
| Downstream effect | Preserve trusted catalog data, explicit UTC, no-quote refusals, read-only behavior, separate eligibility/calculation and the shared policy contract. A changed source or reopened finding requires affected-scope reinspection before relying on this recommendation. |
| Technical transition | Ready for detailed design of CU-01 within this teaching scope. Read this record before allocating behavior and retain its basis in the design decisions. |
| Formal disposition | Not fully verified: formal human/business acceptance is absent. This is not production release authority. |

Stage 6 may proceed for this fictional technical example. Carry forward the trusted catalog boundary, separate configuration/eligibility from pure discount calculation, justify the extension point and preserve the independent expected values. Wiring changes remain allowed; universal zero-change extension is not promised.

The subsequent [CDR](../08-cdr/CDR-01.md) and [code audit](../08-cdr/CODE-AUDIT-01.md) provide the later implementation evidence. Negative-minimum policy, simultaneous-fault precedence and production capabilities remain outside the verified business scope. This technical readiness result supplies no formal human/business acceptance or production release authority.
