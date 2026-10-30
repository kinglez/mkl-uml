# Order pricing demonstration requirements — baseline 1

This is a fictional, bounded teaching scenario selected for the user's local full-workflow example. These decisions are demo assumptions, not claims about an existing business. Source skill suite: MKL UML v1.0.2, commit `fb519f3bb2c0aff48dc655be4a15ddeb56ec60d4`.

## User goal and boundary

A Shopper requests a price quote for a shopping cart, optionally supplying one coupon code. The Order Pricing system reports the item subtotal, discount and payable item amount, or a clear refusal. This is **CU-01 Quote cart**. It does not place an order or change the cart.

Product prices and coupon definitions come from trusted server-side demo catalog data. A client cannot make a submitted price authoritative. The demo can use an in-memory adapter; external catalog integration, persistence and web-server deployment are not required.

Currency is CNY only. All money is represented as integer cents. Tax, shipping, payment, stock reservation, stacking coupons and production authentication are outside this example's scope. Payable means payable **item** amount within that scope.

## Functional requirements

- **RF-01** — A Shopper quotes a nonempty cart whose lines identify catalog Products and a quantity from 1 through 99. The authoritative unit price is a trusted Product price; it may be zero but cannot be negative.
- **RF-02** — The system computes subtotal as the sum of each unit price multiplied by its quantity.
- **RF-03** — With no coupon, discount is zero and payable equals subtotal.
- **RF-04** — A fixed-amount Coupon discounts its configured cents when the subtotal reaches its minimum. The discount is capped at the subtotal.
- **RF-05** — A percentage Coupon discounts `subtotal * basisPoints // 10000`, rounded down to a cent. Its configured rate is between 0 and 10000 inclusive and its minimum must be reached.
- **RF-06** — An unknown or expired coupon refuses the quote with a reason; it is not silently ignored. A coupon is expired when evaluation time is equal to or later than its expiry instant.
- **RF-07** — A known unexpired coupon whose minimum is not reached refuses the quote without producing a successful quote.
- **RF-08** — A successful PriceQuote reports subtotal, discount, payable and currency. Always `0 <= discount <= subtotal` and `payable = subtotal - discount`.
- **RF-09** — An empty cart, unknown Product, invalid quantity, unsupported currency or invalid coupon configuration yields an explicit failure with no successful PriceQuote.
- **RF-10** — Quoting is read-only: it does not change cart lines, catalog data or coupon state and does not create an order. At most one coupon code is accepted.

## Business rules

- **RN-01** — CNY integer cents are the sole monetary unit; binary floating point is not used.
- **RN-02** — Quantity is an integer in `[1, 99]`; booleans are not quantities.
- **RN-03** — Fixed discounts are capped; payable is never negative.
- **RN-04** — Percentage discounts round down after the integer calculation.
- **RN-05** — Evaluation time must be explicit and timezone-aware UTC for deterministic expiry checks.
- **RN-06** — Coupon conditions are checked before applying the selected discount rule.
- **RN-07** — Failure produces no successful quote and does not fall back to the full price automatically.
- **RN-08** — Input/coupon validation is separate from the discount calculation contract; adding a discount algorithm must preserve the common contract.

## Quality and design constraints

- **RNF-01** — The pricing calculation supports adding another discount algorithm without editing the core quote workflow or monetary arithmetic. Registration/wiring may change; zero-change integration everywhere is not promised.
- **RNF-02** — Repeated calls with the same cart, catalog, coupon and evaluation instant give the same result and preserve inputs.
- **RNF-03** — The local reference implementation and tests use only Python's standard library and support Python 3.9+. No live service, installation or external account is needed.
- **RNF-04** — Replacing a supported DiscountPolicy preserves its accepted subtotal domain, result bounds, currency, determinism and absence of input mutation. Demonstrate this with shared contract tests rather than inheritance arrows alone.
- **RNF-05** — Demo collaborators should be replaceable in tests through small contracts. Do not introduce a pattern, service, repository or interface without naming the responsibility/constraint that requires it.

## Demonstration data

Prices are authoritative demo catalog snapshots; example inputs supply Product codes and quantities, not editable prices.

| Product | Unit cents | Quantity in the main cart |
|---|---:|---:|
| BOOK-001 | 12000 | 2 |
| PEN-002 | 1500 | 1 |

Main-cart subtotal: **25500 cents = CNY 255.00**.

All positive coupon definitions below expire at `2030-01-01T00:00:00Z`; the normal evaluation instant is `2026-10-29T00:00:00Z`.

| Coupon code | Rule | Minimum subtotal | Main-cart expected discount / payable |
|---|---|---:|---:|
| no coupon | no discount | 0 | 0 / 25500 |
| SAVE30 | fixed 3000 cents | 20000 | 3000 / 22500 |
| TENOFF | 1000 basis points | 10000 | 2550 / 22950 |
| BIGSAVE | fixed 50000 cents | 0 | 25500 / 0 |

Additional required checks: 333 cents at 10% gives 33 cents discount and 300 payable; below-minimum rejection; exact-expiry rejection; zero-priced nonempty cart; negative/boolean/excess quantity rejection; unknown Product/coupon; unsupported currency; unchanged inputs. These are independent expected values, not values computed from the implementation under test.

## Evidence and acceptance boundary

The example may receive real AI author/reviewer checks and execute mechanical tests. No customer, human implementer, architect or decision maker has approved these fictional policies. PDR/CDR records must distinguish technical demo review from formal business/human acceptance. Proceeding with the local teaching example is authorized; formal production release remains unverified.
