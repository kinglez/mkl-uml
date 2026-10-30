# Behavioral and contract test plan — CU-01

The independent baseline oracle (`00-input/acceptance-oracle.json`) fixes CP-01–CP-30 and literal amounts. These expected values were authored before code by another agent and were not regenerated from production functions. This document derives the trace and adds separately labeled technical checks; it does not change their meaning. Test implementation: `09-reference-implementation/tests/test_pricing.py`.

## Independent workflow cases

For each CP, use fresh trusted fixtures with only that case's overrides, submit the exact request twice at the same UTC instant, compare each result to its literal expectation and each other, and compare unchanged request/fixture/catalog/Coupon snapshots after each invocation. Refusals must contain only ok=false and reasonCategory, with no successful quote. No empty order repository is used as fake evidence; the reference collaboration exposes no order capability or side-effect sink.

| Stable CP | Preconditions / stimulus and literal observable result | CU flow / DR responsibility / DS operation |
|---|---|---|
| CP-01 | Main cart, no Coupon → subtotal 25500 / discount 0 / payable 25500 CNY | Basic; all basic controls; M01–M05/M07/M09/completion |
| CP-02, CP-04 | Eligible SAVE30 / BIGSAVE → discounts 3000 / 25500; payable 22500 / 0 | FA-01; selected discount/completion; M06–M09 and completion |
| CP-03, CP-05 | Eligible TENOFF; subtotals 25500 / 333 → discounts 2550 / 33; payable 22950 / 300 | FA-02; floor calculation; M06–M09 and completion |
| CP-06, CP-07 | Fixed minimum 20000, subtotal 19999 / 20000 → refusal / discount 3000, payable 17000 | FE-06 / FA-01; eligibility; M08 |
| CP-08, CP-09 | Exact expiry / one microsecond before → EXPIRED_COUPON / valid discount 3000 | FE-05 / FA-01; eligibility; M08 |
| CP-10 | Nonempty zero-priced cart, no Coupon → all amounts 0 | FA-03; cart total/completion; M03/M05/M09/completion |
| CP-11–CP-16, CP-29 | Quantity 99 succeeds with subtotal 148500; 0/100/-1/true/1.5/false each INVALID_QUANTITY | Basic / FE-01; request check; M03 |
| CP-17 | Empty Cart → EMPTY_CART, no quote | FE-01; M03 |
| CP-18 | Unknown Product → UNKNOWN_PRODUCT | FE-02; trusted resolution/refusal; M04 |
| CP-19 | Unknown Coupon → UNKNOWN_COUPON, no full-price fallback | FE-04; trusted resolution/refusal; M06 |
| CP-20–CP-23 | Negative fixed, rate-1/10001, fractional fixed cents → INVALID_COUPON_CONFIGURATION | FE-07; configuration before calculation; M07 |
| CP-24 | Requested USD → UNSUPPORTED_CURRENCY | FE-01; boundary validation; M01 |
| CP-25, CP-26 | Rates 0 /10000 → discounts 0 /25500; payable 25500 /0 | FA-02; M09 |
| CP-27, CP-28 | Percentage minimum 10000, subtotal 9999 /10000 → refusal / discount 1000, payable 9000 | FE-06 / FA-02; M08/M09 |
| CP-30 | Two Coupon codes in malformed request → MULTIPLE_COUPONS_NOT_ALLOWED | FE-01; boundary cardinality; M01 |

Exact fixture data and expected maps remain in the oracle. This table groups similar cases for reading; it does not replace their individual CP identities.

## Additional disclosed checks

These new local CP IDs are above the oracle's high-water mark 30. They are not inserted into that independent oracle. Each row identifies one unittest method, which may have several finite subcases.

| CP | Executable method | Given / when / then; source |
|---|---|---|
| CP-31 | test_FE03_invalid_product_price_and_currency | Selected trusted price -1/1.25/true/None or USD → INVALID_PRODUCT_CONFIGURATION, no quote, snapshots unchanged; FE-03/CA-14. |
| CP-32 | test_FE07_invalid_fixed_configuration | Fixed configuration true/None/string → INVALID_COUPON_CONFIGURATION before discount; FE-07/CA-13. |
| CP-33 | test_FE07_invalid_rate_configuration | Rate true/None/fraction/string → same refusal; FE-07/CA-13. |
| CP-34 | test_FE07_invalid_common_configuration | Noninteger minimum, invalid/naive/non-UTC expiry, USD Coupon, unregistered kind → same refusal; FE-07. No negative-minimum case is invented. |
| CP-35 | test_FE01_missing_naive_invalid_and_non_UTC_time | Missing/None/bad/naive/+08:00/Boolean time → INVALID_EVALUATION_TIME; FE-01/CA-15, demo adapter representation. |
| CP-36 | test_adapter_ignores_untrusted_presented_price | Client unitPrice/catalog field 1 cannot override trusted main-cart 25500; request and snapshot unchanged; CA-17/AD-05. |
| CP-37 | test_catalog_is_a_detached_snapshot | Change caller setup and returned snapshot copies → actual quote/catalog retain original authoritative 12000 price; AD-06/RNF-02. |
| CP-38 | test_FA03_zero_subtotal_preserves_coupon_conditions | Zero-priced cart with positive minimum refuses; same valid fixed Coupon with minimum 0 succeeds with all 0; FA-03/RN-06. |
| CP-39 | test_eligibility_refusal_does_not_invoke_discount | Exact-expiry Coupon with spy policy → EXPIRED_COUPON and 0 discount invocations; RN-06/08. Interaction-count assertion here verifies a specific forbidden calculation, not one test for every internal message. |
| CP-40 | test_policy_contract_violation_cannot_produce_a_quote | Inject result -1/25501/true/0.5 → POLICY_CONTRACT_VIOLATION, no quote; AD-09/RF-08. |
| CP-41 | test_domain_results_are_immutable | Assign quote payable/line quantity fails; inconsistent PriceQuote construction refuses; AD-01/RF-08. |
| CP-42 | test_shared_independent_policy_vectors | Same three literal oracle subtotal vectors 0/333/25500 for all four base policy configurations; integer/bounds/CNY/repeatability/policy-state checks; RNF-04. |
| CP-43 | test_all_policies_share_invalid_input_preconditions | Base and extension reject negative/Boolean/fractional subtotal or USD through the same ValueError contract; technical common precondition, not Coupon eligibility. |
| CP-44 | test_extension_shared_contract_and_workflow_stability | CappedHalfDiscount uses min(subtotal//2,2000); literal 0→0,333→166,25500→2000; registered main workflow gives payable 23500, protected source hashes equal; RNF-01/04. |

## Coverage criterion and evidence boundary

Every basic/FA/FE has an observable test outcome, including FE-03 absent from the independent oracle. Controller coverage and flow coverage are checked separately through the mappings above and operation-delta.md. DS-01 is not mechanically exhaustively enumerated: its source checker caps at256 sampled complete paths. Tests use single relevant faults; no simultaneous-failure precedence or arbitrary exhaustive path combinations are promised.

Actual author evidence is in `09-reference-implementation/evidence/`: **15 unittest methods**, including **one method with 30 independent CP subcases**, each run twice. CP-31–CP-44 index the remaining 14 methods. Shared policy vectors are finite evidence, not proof of universal LSP or correctness. Python 3.9.6 and 3.14.7 were actually run; no other interpreter/platform is claimed tested.

The preserved first red run is an import failure before the package existed, not thirty individually observed behavioral regressions. Subsequent green runs exercise actual assertions. Independent CDR must inspect the tests and run them itself. Human/business acceptance, production integration, concurrency, persistence, authentication and excluded negative-minimum policy remain unverified/out of scope.
