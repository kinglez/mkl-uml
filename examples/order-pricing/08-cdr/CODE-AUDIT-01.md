# CODE-AUDIT-01 — reference implementation review

**Historical code-only result: no actionable contradiction with the selected baseline was found.** An independent technical reviewer (AI), different from the reference implementation author (AI), performed this examination on 2026-10-29. The later [CDR](CDR-01.md) completed the cross-model review.

This is a publication adaptation of that actual examination, with portable paths and role labels. It is not a byte-identical original record or human approval. Machine-specific logs and original execution hashes are excluded; [VALIDATION.json](../VALIDATION.json) records checks of the published edition. Formal human/business acceptance remains **Not fully verified**.

## Examined implementation and execution

The reviewer read the four substantive [pricing modules](../09-reference-implementation/pricing/), [tests](../09-reference-implementation/tests/test_pricing.py), [visible example](../09-reference-implementation/run_example.py), [extension exercise](../09-reference-implementation/extension_demo.py), baseline/oracle and PDR obligations. Review probes did not modify the author's runtime source.

| Original independent execution | Actual observation |
|---|---|
| Python **3.14.7** and Python **3.9.6**, each running `-B -m unittest discover -s tests -v` from the implementation directory | Both exited **0**. Each passed **15 unittest methods**, including **30 independent CP subcases**, each invoked twice. |
| `run_example.py` | Exit **0**. No-Coupon/fixed/percentage/capped results, unknown-Coupon refusal and exact-expiry refusal matched the literal baseline. |
| Imported `extension_demo.exercise()` | Exit **0**. Added capped-half rule returned subtotal 25500, discount 2000 and payable 23500; inputs and protected source bytes were unchanged during execution. Importing avoided the CLI's intentional evidence-file write. |
| [Independent code probes](independent_code_probes.py) | Exit **0**. Narrow Product/Coupon/resolver substitutes worked, request-injected catalog data remained nonauthoritative and business state was preserved. No file-write/socket audit event was observed during the selected repeated quotes. |

The test method count is distinct from its subcases. Original compatibility evidence applies to the two interpreters actually used, not every later Python version. The runtime imports use only the standard library.

## Semantic examination

| Obligation | Code evidence and adjudication |
|---|---|
| Exact quantities and money | Cart validation, policy input checks and algorithm constructors exclude booleans and require exact integers. Product prices may be zero but not negative. Fixed discounts use `min`; percentage discounts use integer multiplication and floor division. Monetary calculation uses no binary floating point. |
| Result bounds | The service refuses noninteger, negative or excessive policy output before subtraction/result creation. PriceQuote separately enforces CNY, nonnegative subtotal, `0 <= discount <= subtotal` and `payable = subtotal - discount`. A broken-policy refusal exposes no successful monetary fields. |
| Trusted prices and Coupons | InMemoryCatalog deep-copies trusted setup and returns detached values/copies. The port admits Product code/quantity fields and never forwards client prices or catalog dictionaries as authority. Independent Coupon-injection probes still received SAVE30's trusted 3000-cent discount. |
| Explicit time | Parsing requires an explicit aware zero-offset instant. Pricing reads no hidden current clock. Coupon expiry refuses when evaluation is equal to or later than expiry. Repeated calls use the same instant and stable snapshot. |
| Checks before calculation | Factory construction validates fixed/rate parameters; Coupon validates common configuration and eligibility before calculation. A spy-policy test observes zero calculation calls when eligibility refuses. Unknown/invalid Coupons never trigger automatic full-price fallback. |
| Read-only behavior | Every oracle invocation compares the entire request, fixture data and actual catalog snapshot before/after each of two calls. Frozen values and detached setup are also tested. Source inspection finds no order/redemption writer or persistence/network capability on the pricing path. The empty audit-event list supports the selected probes, not universal absence of side effects. |
| Common policy contract | Shared 0/333/25500 vectors exercise no discount, fixed3000, percentage1000 and fixed50000 with literal results, integer bounds, repeated results and policy-state equality. Built-in and extension algorithms share invalid subtotal/currency preconditions. These are finite substitution checks. |
| Extension point | QuoteService has no kind-specific discount branch. An external strategy, trusted fixture and factory registration produce the new result without changing core arithmetic/workflow. Same-run source hashes demonstrate nonmutation; the actual external registration supplies the architectural evidence. This is not a historical zero-edit Git-diff proof. |
| Dependency direction | Core uses only standard-library business/value support. The service depends on domain values and the DiscountPolicy contract and declares three narrow collaborator protocols. It imports no concrete adapter, default registry or concrete discount algorithm. Adapters depend inward and own wiring. |
| Replaceable client contracts | Independent substitutes implement only Product lookup, Coupon lookup or resolution. They need neither concrete adapter inheritance nor unrelated setup/snapshot methods. Literal no-Coupon/SAVE30 results and unchanged stores support runtime replaceability. |
| PDR-01-F01 | No special negative-minimum sign rejection is added. Tests leave that policy undefined. Incidental execution for an out-of-scope input is not promoted to an approved business rule. |

No code correction was made by this reviewer and no finding quota was used. The review does not settle case normalization, duplicate-line policy, simultaneous-fault precedence or other unspecified business conventions. Arbitrary exceptions from out-of-contract third-party collaborators are not promised normalized refusals.

## Relationship to the CDR

This code-only phase did not approve then-in-progress class/sequence artifacts or generate their headers. The subsequent [CDR-01](CDR-01.md) examined the stable detailed design, verified its multiplicity/fragment corrections and inspected declarations against this implementation. [Header inspection](header-inspection.md) records the conversion limits.

Actual AI implementation and independent execution support bounded technical feasibility. They do not supply missing human/customer/business acceptance or production release authority.
