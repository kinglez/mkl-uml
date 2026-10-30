# Runnable reference implementation

This small, standard-library-only Python implementation supplements the eight UML stages. It realizes fictional **CU-01 Quote cart** with a trusted in-memory catalog and no web server, database or external account.

From the **repository root**:

```bash
python3 -B examples/order-pricing/09-reference-implementation/run_example.py
python3 -B examples/order-pricing/scripts/verify.py
```

The example prints main-cart payable amounts **25500, 22500, 22950 and 0 cents**, plus unknown-Coupon and exact-expiry refusals. All monetary calculations use integer CNY cents. The aggregate verifier runs the UML validators, declaration comparison and reference checks without requiring a renderer. Add `--render` to regenerate SVG/PNG when local PlantUML is available.

To run the implementation tests and extension directly:

```bash
cd examples/order-pricing/09-reference-implementation
python3 -B -m unittest discover -s tests -v
python3 -B extension_demo.py
```

Use the Python executable available on your system if it is named `python` instead of `python3`. No `pip install` step is needed. The extension CLI creates local `evidence/extension.json`; that generated file is not part of the published source baseline.

## Responsibilities

| File | Responsibility |
|---|---|
| [pricing/core.py](pricing/core.py) | Cart/CartLine/Product/Coupon/PriceQuote values, quantity/total rules, Coupon eligibility and result invariants. No adapter or I/O dependency. |
| [pricing/policies.py](pricing/policies.py) | Pure DiscountPolicy contract, no/fixed/percentage algorithms and registry resolution. Construction validates algorithm configuration; calculation does not own expiry/minimum eligibility. |
| [pricing/service.py](pricing/service.py) | Three narrow application-owned collaborator contracts and the quote coordinator. It depends on abstractions rather than the local adapter or default registrations. |
| [pricing/adapters.py](pricing/adapters.py) | Deep-copied trusted catalog, untrusted-request adapter and composition/wiring. Caller input cannot replace the server's catalog. |
| [extension_demo.py](extension_demo.py) | Demonstration-only `capped_half` algorithm, trusted fixture and registration. Default wiring does not register this rule. |
| [tests/test_pricing.py](tests/test_pricing.py) | Independent literal oracle, shared policy contracts and focused interface/eligibility/invariant checks. |

The request adapter reads Product code/quantity fields and ignores additional presented prices. This explicit demo convention is tested; it is not a production API compatibility promise. Product/Coupon lookup returns detached values, while `snapshot()` returns a copy for verification. No order writer, redemption operation, persistence dependency or network/file call exists on the pricing path. Before/after checks inspect actual available state rather than a fake empty Order repository.

## Expected evidence

- **15 unittest methods**, including one that executes all **30 independently authored CP subcases**, each twice. Each compares literal results and complete request/fixture/catalog state. Thirty subcases are not thirty test methods.
- Shared vectors at subtotal **0, 333 and 25500** for NoDiscount, fixed3000, percentage1000 and fixed50000. Result bounds, integer type, repeatability, policy state and common invalid-input preconditions are checked.
- Focused tests for invalid Product data (FE-03), invalid Coupon configuration (FE-07), invalid time (FE-01), zero-subtotal eligibility, authoritative prices, detached catalog state, immutable results, no calculation after refusal and defensive rejection of broken policy output.
- `capped_half` computes `min(subtotal // 2, 2000)`: expected discounts are **0, 166 and 2000**; the main Cart's payable is **23500 cents**. The added strategy and registration use unchanged core/workflow source. This supports one extension point and finite substitution behavior, not universal OCP/LSP or a historical Git-diff claim.

The original local review actually ran Python **3.9.6** and **3.14.7** successfully. That history is summarized in the [independent code audit](../08-cdr/CODE-AUDIT-01.md); fresh publication checks belong to [VALIDATION.json](../VALIDATION.json), and local reruns write new logs. The publication adapts documentation/paths rather than claiming the original review's byte identity.

## Contract limits

`POLICY_CONTRACT_VIOLATION` is a defensive technical refusal for invalid strategy output, outside the business oracle's category set. Request-shape checks and reason spellings are explicit adapter choices. Arbitrary exceptions from out-of-contract third-party implementations are not normalized.

Negative Coupon-minimum acceptance/refusal, simultaneous-failure precedence, production time authority, authentication, integrations, tax/shipping and persistence remain outside the verified business scope. No test pretends to settle the negative-minimum policy.

The [CDR](../08-cdr/CDR-01.md) is the separate independent design review. This reference implementation provides technical evidence; it does not approve formal human/business acceptance or production deployment.
