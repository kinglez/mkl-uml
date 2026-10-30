# Quote request port: analysis-level interface evidence

This is the named local machine interface used by CU-01. It is not a GUI, web deployment, authentication scheme or a commitment to a particular implementation signature. Its source is [baseline 1](../00-input/requirements.md), especially RF-01, RF-06–RF-10 and RN-01–RN-08.

## Inputs and trust

| Input source | Data admitted to the quote goal | Trust and validation responsibility |
|---|---|---|
| Shopper through Quote request port | A sequence of Product-code/quantity pairs; requested currency; zero or one Coupon code; explicit evaluation instant | Untrusted request values. Validate a nonempty Cart, integer quantity 1–99 excluding booleans, CNY currency, at most one Coupon code, and timezone-aware UTC evaluation instant before quote calculation. |
| Trusted server-side demo catalog snapshot, configured within Order Pricing | Product code → authoritative unit cents and CNY; Coupon code → rule kind/value, minimum cents, expiry UTC | Trusted provenance does not excuse invalid configuration. Resolve codes against this snapshot, validate Product price and the selected Coupon configuration, then calculate. No external service or persistence is required. |

The Shopper request has no authoritative unit-price field. A presented or transport-supplied price cannot change Product prices or the lookup result; an adapter must build the quote request from Product codes and quantities. The reference implementation must expose this boundary in its input contract and tests. Catalog setup is an application responsibility outside this Shopper goal, not a second Shopper argument that may override prices.

Evaluation time is explicit for this deterministic demo. Accepting a valid instant from the caller is a teaching assumption, not a production authorization/time-source policy. Selecting a production clock, permission model or catalog refresh protocol remains outside scope.

## Successful result and refusal

Success returns one PriceQuote containing CNY subtotal cents, discount cents and payable cents. All are integers; `0 <= discount <= subtotal`, `payable = subtotal - discount`. Fixed discounts cap at subtotal; percentage discounts use `subtotal * basisPoints // 10000`.

A refusal returns a reason distinguishable from a PriceQuote. It carries no successful PriceQuote. The reason categories below describe meaning, not mandatory wire spelling or exception class names:

| Category | Condition | Flow |
|---|---|---|
| Invalid request | Empty Cart; invalid quantity; unsupported currency; multiple Coupon codes; missing, naive or non-UTC evaluation instant | FE-01 |
| Unknown Product | A CartLine Product code has no catalog entry | FE-02 |
| Invalid catalog Product | Unit price is negative or not integer cents, or Product currency is unsupported | FE-03 |
| Unknown Coupon | Supplied Coupon code has no catalog entry | FE-04 |
| Expired Coupon | Evaluation instant equals or exceeds expiry | FE-05 |
| Minimum not reached | Subtotal is below the known unexpired Coupon minimum | FE-06 |
| Invalid Coupon configuration | Unsupported rule, invalid fixed cents/basis points, noninteger minimum, invalid expiry instant or monetary/currency configuration | FE-07 |

One refusal reason is sufficient if multiple faults coexist; the baseline does not prescribe an ordering among simultaneous invalid conditions. The step anchors describe normal detection responsibilities, not a guaranteed priority of error messages. Retry requires a new request after correcting request/configuration data; the failed invocation terminates without automatically retrying or charging full price.

## Representation interpretations

- Coupon minimum must be integer cents. Whether a negative minimum is accepted or rejected is outside the bounded baseline; this example assigns neither outcome and excludes that policy from acceptance tests.
- Integer monetary values and basis points exclude booleans; these are amounts/counts rather than truth values. This operationalizes integer cents in RN-01 and the explicit quantity restriction in RN-02.
- A missing Coupon code means no Coupon. A supplied code uses exact catalog identity. Normalization or empty-string handling is not a supported discount rule; an unknown supplied code refuses under RF-06.
- A trusted Product snapshot must identify one authoritative price for each resolved Product code during an invocation. The demo's snapshot is stable for that invocation. This is the boundary needed by RNF-02, not a claim of transactional catalog integration.
- Separate repeated Product-code lines each contribute to the subtotal. Deduplication, merging or Cart mutation is unnecessary under RF-02 and RF-10.
- No quote result reserves stock, spends/redeems a Coupon, creates an Order or represents payment success.

These interpretations are local demo assumptions/contract clarification. They are not human-approved production policies. None changes the stated numerical examples or the failure/no-mutation baseline.
