# Traceability: from a business rule to an observable result

This map covers the fixed order-pricing baseline and supplements the detailed correspondence records. **CU-01** is the user goal, **DR-01** its robustness analysis, **DS-01** its complete business interaction and **MC-01** its design model. **DS-02** describes RNF-02 test observations; it does not introduce another user goal.

## Follow SAVE30 through the workflow

1. **Requirement:** [RF-04, RN-03 and RN-06](00-input/requirements.md) require a 3000-cent fixed discount after the threshold is met, capped at the subtotal and applied after eligibility checks.
2. **Textual behavior:** [CU-01 FA-01](03-spec/CU01-quote-cart.md) calculates that discount after configuration, expiry and minimum checks, then resumes basic step 6 to complete the quote.
3. **Analysis allocation:** [DR-01](04-robustness/robustness.puml) identifies Check Coupon eligibility, Apply selected discount and Complete PriceQuote. These are responsibilities, not three mandatory implementation Controllers.
4. **Collaboration:** [DS-01](06-interactions/sequence.puml) lets QuoteService obtain the definition through CouponCatalog, resolve a configured policy, ask Coupon to check eligibility, invoke DiscountPolicy and complete the PriceQuote value.
5. **Operations and structure:** [Operation allocation](06-interactions/operation-delta.md) maps `resolve`, `check_eligibility` and `discount` to [MC-01](07-class-model/classes.puml). PriceQuote construction is internal completion/lifecycle behavior; no ordinary `createQuote` operation is invented.
6. **Independent outcome:** [CP-02](00-input/acceptance-oracle.json) expects subtotal 25500, discount 3000 and payable 22500. Tests read these literal expectations; CP-06/07 check below/exactly-at the minimum.
7. **Review and handoff:** [PDR](05-pdr/PDR-01.md) examines the analysis; [CDR](08-cdr/CDR-01.md) examines realization, allocation, signatures and test evidence. Changed reviewed source makes the [handoff baseline](handoffs/analysis.json) stale.

## Requirements, responsibilities, members and expected results

CP-01–30 come from the independent oracle. Additional tests have disclosed interface/design-contract origins; they do not imply business approval. See the [test source](09-reference-implementation/tests/test_pricing.py), [test plan](06-interactions/test-plan.md) and [published validation record](VALIDATION.json). A local verification run writes fresh execution logs under `validation/latest/`.

| Source | CU-01 behavior | DR-01 responsibility | DS-01 / MC-01 allocation | Independent CP or additional evidence |
|---|---|---|---|---|
| RF-01, RN-02 | Steps 2–3; FE-01/02 | Check Cart request; Resolve trusted catalog values | `Cart.validate`; `ProductCatalog.lookup_product` | CP-10–18, CP-29; free and empty carts remain distinct |
| RF-02, RN-01 | Steps 3–4 | Resolve trusted catalog values; Total Cart lines | `Cart.subtotal` uses trusted Product prices | CP-01–05, CP-11; additional untrusted-price test |
| RF-03 | Step 5, no Coupon | Apply selected discount | `PolicyResolver.resolve(None)` → `NoDiscount.discount` | CP-01, CP-10 |
| RF-04, RN-03 | FA-01 | Apply selected discount | `FixedDiscount.discount`; PriceQuote invariants | CP-02, CP-04; fixed cap and zero payable |
| RF-05, RN-04 | FA-02 | Apply selected discount | `PercentageDiscount.discount` integer division | CP-03, CP-05, CP-25/26; rate endpoints and cent floor |
| RF-06, RN-05 | FE-04/05 | Check Coupon eligibility; Return refusal | `CouponCatalog.lookup_coupon`; `Coupon.check_eligibility` | CP-08/09, CP-19; exact expiry and one microsecond before |
| RF-07, RN-06 | FE-06 | Check Coupon eligibility | `Coupon.check_eligibility`; refusal propagation | CP-06/07, CP-27/28; minima for both Coupon types |
| RF-08 | Steps 6–7; FA-03 | Complete PriceQuote | PriceQuote constructor checks; `QuoteRequestPort.handle` encoding | Every success CP checks all output fields and amount invariants |
| RF-09 | FE-01–03, FE-07 | Request/catalog/configuration checks; Return refusal | Boundary, Cart, catalog adapter, factories and Coupon validate their respective data | CP-12–18, CP-20–24, CP-29; additional Product/time/configuration cases |
| RF-10, RN-07 | At most one Coupon; all postconditions | Request check; Return refusal; all read-only paths | `QuoteRequestPort.handle`; detached catalog; no Order writer | CP-30; repeated calls and request/catalog snapshots for every CP |
| RN-08, RNF-01 | Configuration/eligibility before calculation | Separate eligibility from selected discount | Distinct PolicyResolver, Coupon and DiscountPolicy contracts | Registration extension and protected-source checks; [change exercise](CHANGE_IMPACT.md) |
| RNF-02 | Same inputs and explicit instant give the same result | All responsibilities | No implicit clock/write; DS-02 observes real state | Every CP repeats twice with before/after comparisons |
| RNF-03 | Local execution constraints | Analysis preserves the constraint | Python standard library; no network client | Recorded runtimes and execution; not every possible Python environment |
| RNF-04 | Algorithms preserve one common contract | Apply selected discount | DiscountPolicy and its replacements | Independent vectors at three subtotals plus extension vectors; finite evidence |
| RNF-05 | Small, replaceable collaborators | Logical controls need not map one-to-one to classes | Application-owned ProductCatalog, CouponCatalog and PolicyResolver; local adapters | Minimal substitutes, import/client examination and SOLID record |

## Reading the evidence correctly

- The [glossary](01-domain/glossary.md) defines business meanings; the [interface contract](03-spec/interface-contract.md) defines representation and error categories.
- [Robustness correspondence](04-robustness/correspondence.md) connects text, responsibilities and data origins. [Member provenance](07-class-model/provenance.md) explains business state, technical contracts, observation operations and lifecycle origins.
- A [test plan](06-interactions/test-plan.md) specifies criteria; the [oracle](00-input/ACCEPTANCE_ORACLE.md) supplies independent expectations; an actual run supplies execution evidence. These are separate layers.
- A negative Coupon minimum has no specified acceptance/refusal outcome in this bounded baseline. An incidental implementation path cannot upgrade it into approved policy. Simultaneous-fault priority and production time authority are also outside the verified scope.
- Name/marker coverage does not establish semantic correspondence. The review must inspect actual data, guards, responsibilities and outcomes across artifacts.

This publication adapts editorial text and paths from the local exercise. Its handoff hashes describe the publication's reviewed source, rather than claiming byte identity with historical local review files.
