# CU-01 — Quote cart

## Document control and evidence

| Field | Value |
|---|---|
| Document | DOC-CU-01, version 1.0, 2026-10-29 |
| Status | Draft teaching baseline; ready for independent technical PDR, without human/business acceptance |
| Author | Codex analysis agent |
| ID | CU-01, preserved from the supplied baseline |
| Name / level | Quote cart / user goal |
| Primary actor | Shopper, ACT-01 |
| Goal | Obtain a read-only item-price result for a Cart, optionally with one Coupon, or an explicit refusal |
| Priority / frequency | Required demo goal / on demand; no production frequency claim |
| Source | [requirements baseline 1](../00-input/requirements.md) |
| Domain | [domain.puml](../01-domain/domain.puml) and [glossary](../01-domain/glossary.md) |
| Actor view | [use-cases.puml](../02-use-cases/use-cases.puml) |
| Interface evidence | [Quote request port contract](interface-contract.md) |
| Downstream analysis | DR-01 in [robustness.puml](../04-robustness/robustness.puml); detailed design and executable tests pending |

The local demo is authorized. All business policies are fictional teaching assumptions. No customer, human implementer, architect or decision maker has signed off this artifact. There are no included, extended or generalized use cases.

## Scope and actors

Shopper supplies CartLine Product codes/quantities, CNY, an optional Coupon code and an explicit evaluation instant through the local Quote request port. Order Pricing resolves authoritative Product/Coupon definitions from its internal trusted server-side catalog snapshot. The catalog is not another external actor for this demo.

The goal covers subtotal, discount and payable item amount. Tax, shipping, checkout, order placement, payment, stock reservation, Coupon redemption, stacking, authentication, external catalog integration and persistence are excluded. Only CNY integer cents are in scope.

## Domain involvement and terminology

| Official domain concept | Values used by this goal | Participation |
|---|---|---|
| Cart | CartLine collection | The supplied subject of the quote; remains unchanged |
| CartLine | Product code, quantity | Each line contributes Product unit cents times quantity |
| Product | Product code, authoritative unit cents, CNY | Trusted lookup input, including zero-priced Products |
| Coupon | Code, rule kind/value, minimum cents, expiry UTC | Optional eligibility and discount configuration; remains unchanged |
| PriceQuote | Subtotal cents, discount cents, payable cents, CNY | Success-only result |

Shopper is an external role and Quote request port is an interface. Neither needs a domain class. Failure reason is interface output without a tracked lifecycle. DiscountPolicy is a downstream design constraint from RNF-04; it is not a conceptual domain entity. The analysis discovers no missing domain concept.

## Preconditions

| ID | Required existing state | Verification |
|---|---|---|
| PRE-01 | The local Order Pricing quote capability and a trusted demo catalog snapshot are available | Inspect local demo setup; no network service is required |

Validity of Cart, quantities, prices, Coupon and evaluation time is not a precondition: CU-01 must handle invalid values explicitly.

## Trigger

The Shopper invokes Quote request port to request a quote for the supplied Cart. For the basic flow no Coupon code is supplied. The baseline example evaluation instant is `2026-10-29T00:00:00Z`.

## Basic flow

| Step | Responsible party | Observable behavior and result | Domain / interface | Rules |
|---:|---|---|---|---|
| 1 | Shopper | Submits the CartLine Product codes and quantities, CNY, no Coupon code and explicit evaluation instant | Cart, CartLine; Quote request port | RN-01, RN-05 |
| 2 | System | Checks that the Cart is nonempty, each quantity is valid, currency is CNY, evaluation instant is timezone-aware UTC and at most one Coupon code appears | Cart, CartLine; Quote request port | RN-01, RN-02, RN-05 |
| 3 | System | Resolves each Product code against the trusted catalog snapshot and checks authoritative unit cents and currency; no client price can replace the catalog price | Product | RN-01 |
| 4 | System | Computes the Cart subtotal from every authoritative unit price times its CartLine quantity | CartLine, Product | RN-01 |
| 5 | System | Recognizes the absent Coupon and sets discount to zero | Coupon absence | RN-06 |
| 6 | System | Produces a PriceQuote with subtotal, discount, payable and CNY, subject to the common monetary invariants | PriceQuote | RN-01, RN-03, RN-07, RN-08 |
| 7 | System | Returns the PriceQuote through Quote request port to the Shopper; the invocation ends successfully | PriceQuote; Quote request port | RN-07 |

All steps preserve the supplied Cart, catalog Product/Coupon values and Coupon state. A PriceQuote is a result, with no order or redemption side effect.

## Alternative flows

The local FA identities below are first allocations for CU-01. Their numbers are stable across later editing, not recalculated from display order.

For any supplied Coupon code at step 5, the System first resolves its trusted definition, checks its configuration, then checks expiry and minimum eligibility. An unknown code follows FE-04; invalid/ineligible definitions follow FE-05, FE-06 or FE-07. Only a known, valid and eligible definition reaches the corresponding successful calculation branch below.

| ID | Trigger and anchored behavior | Outcome | Source |
|---|---|---|---|
| FA-01 | At step 5 the supplied code resolves to a valid, eligible fixed-amount Coupon after the shared lookup and checks. System sets discount to the lesser of configured fixed cents and subtotal. | Returns to step 6 with a valid fixed discount; BIGSAVE may yield zero payable. | RF-04, RF-06, RF-07; RN-03, RN-05, RN-06, RN-08 |
| FA-02 | At step 5 the supplied code resolves to a valid, eligible percentage Coupon after the shared lookup and checks. System computes discount as `subtotal * basisPoints // 10000`, with basis points in 0–10000 inclusive. | Returns to step 6 with a cent-rounded-down discount. | RF-05, RF-06, RF-07; RN-01, RN-04–RN-06, RN-08 |
| FA-03 | At step 4 a nonempty Cart contains only zero-priced Products, so subtotal is zero. System retains the valid Cart, derives zero subtotal and continues checking the selected Coupon if any. A positive Coupon minimum still causes rejection. A valid applicable Coupon produces zero discount. | Continues at step 5; may return a zero-valued PriceQuote at step 7, or terminate through the applicable Coupon exception. | RF-01, RF-04, RF-05, RF-07–RF-09; RN-03, RN-06 |

The FA-01 and FA-02 calculations replace only the no-Coupon branch. They do not bypass request/Product validation, produce a full-price fallback or change inputs. Configuration checking is separate from the discount calculation contract.

### Alternate flow FA-01 detail

Guard / anchor: step 5 after the supplied code resolves to a valid, eligible fixed-amount Coupon through the shared lookup/configuration/expiry/minimum checks above.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FA-01.1 | System | Takes the lesser of configured fixed cents and the computed subtotal as discount. | Coupon, Cart | Fixed discount is capped at subtotal, including BIGSAVE. |
| FA-01.2 | System | Returns to basic step 6 with that discount. | PriceQuote | Common completion computes payable; no input or Coupon state changes. |

### Alternate flow FA-02 detail

Guard / anchor: step 5 after the supplied code resolves to a valid, eligible percentage Coupon through the shared lookup/configuration/expiry/minimum checks above.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FA-02.1 | System | Uses the configured integer basis points in 0–10000 and computes `subtotal * basisPoints // 10000`. | Coupon, Cart | Discount rounds down to a cent. |
| FA-02.2 | System | Returns to basic step 6 with that discount. | PriceQuote | Common completion computes payable; no input or Coupon state changes. |

### Alternate flow FA-03 detail

Guard / anchor: step 4, where an already valid nonempty Cart contains only zero-priced Products.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FA-03.1 | System | Retains the valid Cart and derives a zero subtotal from its zero-priced Products. | Cart, CartLine, Product | The nonempty Cart remains quotable. |
| FA-03.2 | System | Continues at basic step 5 and checks the selected Coupon if any. | Coupon | A positive minimum follows FE-06; other invalid/ineligible Coupons follow their existing exception. |
| FA-03.3 | System | For no Coupon or an eligible Coupon, continues through steps 6–7 with zero discount and zero payable. | PriceQuote | Returns a zero-valued successful quote; applicable exceptions instead terminate without a quote. |

## Exception flows

Every exception terminates this invocation with a distinguishable reason through Quote request port, no successful PriceQuote, and unchanged Cart/catalog/Coupon state. Recovery means the Shopper submits a new corrected request, or the trusted setup corrects faulty catalog configuration before a new invocation.

| ID | Anchor and condition | Specific system behavior and refusal reason | Outcome | Source |
|---|---|---|---|---|
| FE-01 | Step 2: empty Cart; noninteger/boolean quantity, quantity below 1 or above 99; unsupported request currency; multiple Coupon codes; missing/naive/non-UTC evaluation instant | Identifies the offending request condition and returns an invalid-request reason. System does not calculate a successful quote. | Terminates; Shopper may correct the input and invoke again. | RF-01, RF-09, RF-10; RN-01, RN-02, RN-05, RN-07 |
| FE-02 | Step 3: a CartLine Product code is absent from the trusted catalog | Returns unknown-Product reason naming the unresolved code. | Terminates; Shopper may correct the Product code and invoke again. | RF-09; RN-07 |
| FE-03 | Step 3: resolved Product has negative/noninteger unit cents or unsupported currency | Returns invalid-catalog-Product reason; a client-supplied substitute price cannot repair it. | Terminates; trusted setup requires correction before invoking again. | RF-01, RF-09; RN-01, RN-07 |
| FE-04 | Supplied-Coupon lookup at step 5: supplied Coupon code has no catalog definition | Returns unknown-Coupon reason. It does not ignore the code or automatically quote the full price. | Terminates; Shopper may remove/correct the Coupon and invoke again. | RF-06; RN-07 |
| FE-05 | Supplied-Coupon eligibility at step 5: evaluation instant is equal to or later than Coupon expiry | Returns expired-Coupon reason, including at the exact expiry instant. | Terminates; Shopper may choose another Coupon or omit it in a new invocation. | RF-06; RN-05–RN-07 |
| FE-06 | Supplied-Coupon eligibility at step 5: known, valid, unexpired Coupon minimum exceeds subtotal | Returns minimum-not-reached reason without a successful PriceQuote. | Terminates; Shopper may change the Cart/Coupon in a new invocation. | RF-07; RN-06, RN-07 |
| FE-07 | Supplied-Coupon configuration check at step 5: unsupported rule, negative/noninteger fixed cents, noninteger minimum, percentage outside 0–10000 or not integer, unsupported monetary currency, invalid expiry instant | Returns invalid-Coupon-configuration reason before applying any discount calculation. | Terminates; trusted setup requires correction before invoking again. | RF-09; RN-01, RN-05–RN-08 |

No priority among simultaneous faults is promised. The first reported reason must identify an actual failure; all paths preserve the failure postcondition.

### Exception flow FE-01 detail

Guard / anchor: basic step 2 and any invalid-request condition listed in the FE-01 summary.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FE-01.1 | System | Identifies the offending empty Cart, quantity, currency, Coupon-cardinality or evaluation-instant condition. | Cart, CartLine; request values | Invalid-request reason identifies the actual failure. |
| FE-01.2 | System | Returns that refusal through Quote request port, with no successful PriceQuote, and terminates this invocation. | PriceQuote absence | Inputs remain unchanged; Shopper may correct the request and invoke again. |

### Exception flow FE-02 detail

Guard / anchor: basic step 3, where a supplied Product code has no trusted catalog entry.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FE-02.1 | System | Identifies the unresolved Product code and selects the unknown-Product refusal reason. | CartLine, Product lookup | No substitute price or Product enters calculation. |
| FE-02.2 | System | Returns the refusal through Quote request port, with no successful PriceQuote, and terminates this invocation. | PriceQuote absence | Inputs remain unchanged; Shopper may correct the Product code and invoke again. |

### Exception flow FE-03 detail

Guard / anchor: basic step 3, where a resolved Product has negative/noninteger unit cents or unsupported currency.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FE-03.1 | System | Identifies the invalid authoritative Product configuration and selects the invalid-catalog-Product refusal reason. | Product | A client-supplied replacement price cannot repair it. |
| FE-03.2 | System | Returns the refusal through Quote request port, with no successful PriceQuote, and terminates this invocation. | PriceQuote absence | Inputs remain unchanged; trusted setup requires correction before a new invocation. |

### Exception flow FE-04 detail

Guard / anchor: supplied-Coupon lookup at step 5, where the supplied Coupon code has no trusted definition.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FE-04.1 | System | Selects an unknown-Coupon refusal reason for the unresolved code. | Coupon lookup | The code is not ignored and no automatic full-price fallback occurs. |
| FE-04.2 | System | Returns the refusal through Quote request port, with no successful PriceQuote, and terminates this invocation. | PriceQuote absence | Inputs remain unchanged; Shopper may remove or correct the Coupon code in a new request. |

### Exception flow FE-05 detail

Guard / anchor: supplied-Coupon eligibility at step 5, where evaluation instant is equal to or later than expiry.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FE-05.1 | System | Selects an expired-Coupon refusal reason, including when evaluation exactly equals expiry. | Coupon | No discount calculation is applied. |
| FE-05.2 | System | Returns the refusal through Quote request port, with no successful PriceQuote, and terminates this invocation. | PriceQuote absence | Inputs remain unchanged; Shopper may choose another Coupon or omit it in a new request. |

### Exception flow FE-06 detail

Guard / anchor: supplied-Coupon eligibility at step 5, where a known, valid, unexpired Coupon minimum exceeds subtotal.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FE-06.1 | System | Selects a minimum-not-reached refusal reason. | Coupon, Cart subtotal | No successful PriceQuote or full-price fallback occurs. |
| FE-06.2 | System | Returns the refusal through Quote request port and terminates this invocation. | PriceQuote absence | Inputs remain unchanged; Shopper may change the Cart or Coupon in a new request. |

### Exception flow FE-07 detail

Guard / anchor: supplied-Coupon configuration check at step 5 and one of the invalid-configuration conditions listed in the FE-07 summary. A minimum's negative sign alone has no prescribed outcome in this bounded baseline.

| Step | Responsible party | Action | Domain concept | Result |
|---|---|---|---|---|
| FE-07.1 | System | Identifies the unsupported rule, invalid fixed cents/basis points, noninteger minimum, unsupported currency or invalid expiry instant and selects an invalid-Coupon-configuration refusal reason. | Coupon | Configuration checking precedes any discount calculation. |
| FE-07.2 | System | Returns the refusal through Quote request port, with no successful PriceQuote, and terminates this invocation. | PriceQuote absence | Inputs remain unchanged; trusted setup requires correction before a new invocation. |

## Postconditions

| Type | Checkable result |
|---|---|
| Success | Shopper receives exactly one PriceQuote with CNY integer subtotal, discount and payable; `0 <= discount <= subtotal`; `payable = subtotal - discount`. |
| Failure | Shopper receives an explicit refusal reason and no successful PriceQuote; no automatic full-price fallback. |
| Read-only effects | CartLine values, catalog data and Coupon state are unchanged. No Order, payment, reservation, redemption or persistent record is created by this goal. |

## Business rules

The rules retain the source identifiers and meanings; these rows define local references for the textual profile.

| ID | Business rule | Source / applicability |
|---|---|---|
| RN-01 | Use CNY integer cents only; no binary floating-point money | Baseline RN-01; steps 1–6, FE-01, FE-03, FE-07 |
| RN-02 | Quantity is an integer in 1–99 inclusive; booleans are not quantities | Baseline RN-02; step 2, FE-01 |
| RN-03 | Cap fixed discounts at subtotal; payable is never negative | Baseline RN-03; FA-01, step 6 |
| RN-04 | Round percentage discount down after integer calculation | Baseline RN-04; FA-02 |
| RN-05 | Require explicit timezone-aware UTC evaluation time | Baseline RN-05; step 2, FE-01, FE-05, FE-07 |
| RN-06 | Check Coupon conditions before applying the selected discount rule | Baseline RN-06; FA-01, FA-02, FE-04–FE-07 |
| RN-07 | Failure has no successful quote and no automatic full-price fallback | Baseline RN-07; step 7, every FE |
| RN-08 | Separate input/Coupon validation from the discount calculation contract; preserve that contract when extending algorithms | Baseline RN-08; step 6, FA-01, FA-02, FE-07; downstream design obligation |

## Special requirements and design obligations

| Source ID | Requirement retained from baseline | Verification destination |
|---|---|---|
| RNF-01 | New discount algorithms should require no edit to core quote workflow or money arithmetic; registration/wiring may change | Detailed design extension seam and an extension exercise; pending |
| RNF-02 | Same Cart, catalog, Coupon and evaluation instant yields same result, preserving inputs | Repeatability and unchanged-input tests; pending |
| RNF-03 | Reference implementation uses only Python standard library, Python 3.9+ | Runtime compatibility and dependency inspection; pending |
| RNF-04 | Replaceable DiscountPolicy preserves accepted subtotal domain, bounds, CNY, determinism and no mutation | Shared executable policy contract tests; pending |
| RNF-05 | Demo collaborators use small replaceable contracts; every interface/pattern needs a named responsibility | Detailed design review and collaborator substitution tests; pending |

These constraints are traceable downstream obligations. The analysis diagrams do not establish SOLID, runtime behavior or substitution merely by their shapes.

## Functional traceability

| Source | Coverage in CU-01 |
|---|---|
| RF-01 | Steps 1–3; FA-03; FE-01, FE-03 |
| RF-02 | Step 4 |
| RF-03 | Step 5, step 6 |
| RF-04 | FA-01, FA-03; FE-06 |
| RF-05 | FA-02, FA-03; FE-06, FE-07 |
| RF-06 | FE-04, FE-05; FA-01, FA-02 |
| RF-07 | FE-06, FA-03 |
| RF-08 | Steps 6–7; success postcondition |
| RF-09 | FE-01–FE-03, FE-07 |
| RF-10 | Request check at step 2; all paths' read-only effects |

DR-01 maps every basic step and local FA/FE in [the robustness correspondence](../04-robustness/correspondence.md). Sequence message and executable test identifiers will be allocated only in those later artifacts; no nonexistent tests are claimed here.

## Acceptance criteria

All expected cents below come from baseline 1, independently of any future implementation. Except exact-expiry checks, known positive Coupons expire at `2030-01-01T00:00:00Z` and evaluation uses `2026-10-29T00:00:00Z`.

| ID | Given / when / then | Flow |
|---|---|---|
| CA-01 | Given BOOK-001 at 12000 cents ×2 and PEN-002 at 1500 ×1, when Shopper requests no Coupon, then subtotal=25500, discount=0, payable=25500 and currency=CNY. | Basic flow |
| CA-02 | Given the main Cart and SAVE30 fixed 3000, minimum 20000, when quoted, then subtotal=25500, discount=3000, payable=22500. | FA-01 |
| CA-03 | Given the main Cart and TENOFF at 1000 basis points, minimum 10000, when quoted, then discount=2550 and payable=22950. | FA-02 |
| CA-04 | Given the main Cart and BIGSAVE fixed 50000, minimum 0, when quoted, then discount=25500 and payable=0. | FA-01 |
| CA-05 | Given subtotal 333 cents and a valid 1000-basis-point Coupon with minimum 0, when quoted, then discount=33 and payable=300. | FA-02 |
| CA-06 | Given a valid nonempty zero-priced Cart, when quoted without a Coupon or with an eligible minimum-0 Coupon, then subtotal=discount=payable=0. | FA-03 |
| CA-07 | Given subtotal 1500 and SAVE30 with minimum 20000, when quoted, then Shopper receives minimum-not-reached refusal and no successful quote. | FE-06 |
| CA-08 | Given evaluation exactly `2030-01-01T00:00:00Z` and SAVE30, when quoted, then Shopper receives expired-Coupon refusal and no successful quote. | FE-05 |
| CA-09 | Given an empty Cart, or quantity -1, true, 0 or 100 in separate cases, when quoted, then Shopper receives invalid-request refusal and no successful quote. | FE-01 |
| CA-10 | Given an unknown Product code, when quoted, then Shopper receives unknown-Product refusal and no successful quote. | FE-02 |
| CA-11 | Given an unknown Coupon code, when quoted, then Shopper receives unknown-Coupon refusal and no successful quote. | FE-04 |
| CA-12 | Given unsupported request currency, when quoted, then Shopper receives invalid-request refusal and no successful quote. | FE-01 |
| CA-13 | Given negative fixed cents, noninteger minimum or out-of-range/noninteger percentage configuration in separate cases, when selected, then Shopper receives invalid-Coupon-configuration refusal. | FE-07 |
| CA-14 | Given a catalog Product with negative/noninteger cents or unsupported currency, when requested, then Shopper receives invalid-catalog-Product refusal. | FE-03 |
| CA-15 | Given a missing/naive/non-UTC evaluation instant or more than one Coupon code in separate cases, when quoted, then Shopper receives invalid-request refusal. | FE-01 |
| CA-16 | Given the same valid inputs and trusted snapshot, when quoted repeatedly, then outputs are equal and Cart/catalog/Coupon values remain equal to their before-call values; failed calls also preserve inputs. | All paths; RNF-02 |
| CA-17 | Given a client-presented price different from the trusted Product price, when the adapter submits Product codes and quantities, then the resulting quote uses the trusted price and the client cannot override the catalog. | Steps 1–4; trust boundary |
| CA-18 | Given valid percentage rates 0 and 10000 in separate cases, when quoted, then discount is respectively 0 and subtotal; fixed 0 and subtotal 0 also preserve the monetary contract. | FA-01, FA-02, FA-03; RNF-04 |

## Review status and pending decisions

The analysis author checked this specification against the fictional baseline and profile validators. Subsequent technical review, detailed design and runtime evidence are recorded in `../05-pdr/PDR-01.md`, `../08-cdr/CDR-01.md` and `../VALIDATION.json`. Formal human/business approval remains unverified. No requirement ambiguity blocks local teaching work; production time authority, authentication, error precedence, catalog refresh and the acceptance/refusal policy for a negative Coupon minimum are outside this bounded baseline. Minimum remains integer cents, but this document prescribes no negative-minimum outcome or acceptance test.
