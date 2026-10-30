# Independent acceptance oracle — baseline 1

This finite oracle was derived directly from `requirements.md`, without consulting an implementation or design model. All expected monetary values are literal, independently hand-checked values. It is evidence for this fictional teaching example, not exhaustive proof, customer approval or a production release decision.

## File and adapter conventions

`acceptance-oracle.json` contains 30 workflow cases, `CP-01` through `CP-30`, plus three shared discount-policy vectors. Monetary values are integer CNY cents except deliberately invalid fixture data in CP-23. Request field names, fixture merge syntax and `reasonCategory` spellings are proposed technical demo conventions. An implementation may adapt its native API to this file; these names are not separately approved business requirements.

The schema is intentionally small:

| Field | Meaning |
| --- | --- |
| `schemaVersion` | Identifies this oracle format. |
| `fixtures.products` | Trusted server-side product definitions keyed by product code. `unitPrice` is authoritative; the request supplies no price. |
| `fixtures.coupons` | Trusted coupon definitions keyed by coupon code. |
| `cases[].caseID`, `scenario`, `refs` | Stable CP identifier, description and baseline requirement/rule references. |
| `cases[].input` | Complete request: `cart` line array, `currency`, nullable `couponCode`, and explicit UTC `evaluatedAt`. |
| `cases[].fixtureOverrides` | Optional map changes applied to a fresh deep copy of base fixtures for this case. Merge nested maps by key; replace scalar values. Never carry changes to another case. |
| `cases[].expected` | Literal successful amounts, or `ok: false` with a refusal category. |
| `contractAssertions` | Repetition and read-only checks applied to every workflow case. |
| `policyContract` | Shared pure-discount vectors and assertions applied to every listed policy. |

A successful expectation has exactly `ok`, `subtotal`, `discount`, `payable` and `currency`. A failure expectation has `ok: false` and `reasonCategory`; it has no successful quote or successful monetary fields. The adapter must verify that a refusal did not also produce a successful quote. Human-readable error wording and native exception/result types are unconstrained by this oracle.

For CP-30 only, `couponCode` deliberately contains an array with two codes. This is a request-boundary probe using a proposed malformed-request representation. The business requirement is that at most one coupon is accepted. A typed native interface may use an adapter to demonstrate the refusal at its public request boundary.

## Independently checked successful amounts

| Cases | Check | Subtotal / discount / payable |
| --- | --- | ---: |
| CP-01 | Two books at 12000 plus one pen at 1500: 24000 + 1500 | 25500 / 0 / 25500 |
| CP-02, CP-09 | SAVE30 subtracts 3000 when valid | 25500 / 3000 / 22500 |
| CP-03 | 10% of 25500 is 2550 | 25500 / 2550 / 22950 |
| CP-04 | Configured 50000 is capped at 25500 | 25500 / 25500 / 0 |
| CP-05 | 10% of 333 is 33.3 cents; floor to 33 | 333 / 33 / 300 |
| CP-07 | Exactly 20000 reaches SAVE30 minimum | 20000 / 3000 / 17000 |
| CP-10 | One zero-priced product still makes a nonempty cart | 0 / 0 / 0 |
| CP-11 | 99 pens: 1500 × 99 = 148500 | 148500 / 0 / 148500 |
| CP-25 | Zero basis points is an allowed rate | 25500 / 0 / 25500 |
| CP-26 | 10000 basis points is the entire subtotal | 25500 / 25500 / 0 |
| CP-28 | Exactly 10000 reaches TENOFF minimum; 10% is 1000 | 10000 / 1000 / 9000 |

CP-05 changes TENOFF's minimum to zero in trusted fixtures so that the 333-cent rounding case exercises the calculation. It does not bypass the original minimum in the normal fixtures. CP-06 and CP-27 use trusted catalog snapshots priced one cent below their respective coupon minima.

CP-08 evaluates at `2030-01-01T00:00:00Z` and must refuse because equality means expiry. CP-09 evaluates at `2029-12-31T23:59:59.999999Z`, one microsecond before expiry, and remains eligible. Both instants are explicitly UTC.

## Failure categories and coverage

The category semantics below follow the indicated rules; their uppercase spellings are only the oracle's adapter vocabulary.

| Category | Cases | Evidence |
| --- | --- | --- |
| `COUPON_MINIMUM_NOT_REACHED` | CP-06, CP-27 | RF-07: known, unexpired coupon below its minimum refuses. |
| `EXPIRED_COUPON` | CP-08 | RF-06: evaluation time equal to expiry is expired. |
| `INVALID_QUANTITY` | CP-12–CP-16, CP-29 | RF-09 / RN-02: reject 0, 100, -1, true, 1.5 and false. Quantity 1 is accepted in CP-05; 99 in CP-11. |
| `EMPTY_CART` | CP-17 | RF-01 / RF-09. |
| `UNKNOWN_PRODUCT` | CP-18 | RF-09. |
| `UNKNOWN_COUPON` | CP-19 | RF-06; no silent full-price fallback. |
| `INVALID_COUPON_CONFIGURATION` | CP-20–CP-23 | Negative fixed discount violates RF-08 / RN-03; rates -1 and 10001 violate RF-05; fractional-cent fixed amount violates RN-01. RF-09 requires explicit failure for invalid configuration. |
| `UNSUPPORTED_CURRENCY` | CP-24 | RF-09 / RN-01: only CNY is supported. |
| `MULTIPLE_COUPONS_NOT_ALLOWED` | CP-30 | RF-10 permits at most one coupon; exact request/error representation is proposed. |

The malformed decimal in CP-23 is validation input, not an authorized use of binary floating point in monetary calculations. Validation must refuse it before applying a discount.

## Repetition, mutation and substitution evidence

For **every workflow case**, start with fresh fixtures, snapshot the entire request (including cart), catalog, coupon definitions and any coupon state, and run the same request twice at the exact same evaluation instant. Compare both results to the same literal expectation and to each other. Verify that all snapshots are unchanged after each invocation and that no order was created. Observe this through available collaborators or state snapshots; the oracle does not prescribe an order repository or any other architecture. Refused requests are subject to the same checks.

The separate `policyContract` vectors apply the same subtotal/currency inputs to all four supported policy configurations. Expected discounts are:

| Subtotal | None | Fixed 3000 | 1000 basis points | Fixed 50000 |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 |
| 333 | 0 | 333 | 33 | 333 |
| 25500 | 0 | 3000 | 2550 | 25500 |

These vectors concern pure discount calculation **after** input validation and coupon eligibility checks, as RN-08 requires. In this layer, the 3000 fixed policy may accept subtotal 333 even though the real SAVE30 coupon's minimum would reject a workflow quote for that subtotal. Apply the shared checks for integer-cent results, `0 <= discount <= subtotal`, currency preservation, identical repeated results, unchanged inputs and unchanged policy state to every listed policy. A different native return shape may express currency preservation through its common input/output contract.

The shared vectors provide finite evidence for RNF-04 policy substitution. Workflow golden cases alone do not establish substitution, and these three vectors do not prove every possible nonnegative subtotal. RNF-01's core-workflow stability when adding a policy still needs design/code evidence; this file does not claim to prove it.

## Deliberately unresolved baseline details

- No case establishes validation precedence when several inputs are invalid at once; failures use a single relevant fault.
- The baseline does not define whether a negative coupon minimum is intrinsically invalid. This oracle therefore does not invent that rejection rule.
- Duplicate cart lines, whitespace/case normalization, malformed timestamps, catalog corruption, and exhaustive configuration-field validation need separate contract decisions if brought into scope.
- An unknown future discount kind may become supported through registration. This oracle does not treat every currently unlisted kind as permanently invalid.
- No case compares a caller-supplied price with the catalog. Prices come exclusively from trusted fixture catalog data; any public extra-field policy requires a separate adapter decision.

Passing these examples supports the bounded demo's technical verification. It does not replace a complete test strategy, formal business acceptance, production integration or a universal correctness proof.
