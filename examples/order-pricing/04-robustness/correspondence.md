# DR-01 / CU-01 behavior correspondence and discovery

Sources: [CU-01 text](../03-spec/CU01-quote-cart.md), [domain glossary](../01-domain/glossary.md), [interface evidence](../03-spec/interface-contract.md). This is preliminary design. Controls denote analysis responsibilities, not a requirement to create seven controller classes. There are no operations, sequence ordering or infrastructure classes in this view.

## Stable local element registry

These are first allocations in this new example. They remain stable if labels/layout change. DR-01 is the diagram identity; syntax aliases do not replace trace identities. Sequence/test destinations are handoff obligations, not claims of generated or passing tests.

| ID | Alias / name | Origin | Downstream responsibility / test obligation |
|---|---|---|---|
| ACT-01 | ACT_Shopper / Shopper | CU-01 primary actor and actor diagram | External participant |
| B-01 | B_Quote / Quote request port | Interface contract; basic 1, 7; all refusals | Local request/result interaction; input trust and response shape tests |
| C-01 | C_CheckRequest / Check Cart request | Basic 2, FE-01 | Request validation behavior; CA-09, CA-12, CA-15 |
| C-02 | C_ResolveCatalog / Resolve trusted catalog values | Basic 3; FA-01, FA-02 lookup; FE-02, FE-03, FE-04 | Authoritative Product/Coupon lookup; CA-10, CA-11, CA-14, CA-17 |
| C-03 | C_Total / Total Cart lines | Basic 4, FA-03 | Integer subtotal from every line; CA-01, CA-06 |
| C-04 | C_CheckCoupon / Check Coupon eligibility | Basic 5, FA-01, FA-02, FE-05–FE-07 | Configuration before eligibility/calculation; exact expiry/minimum/rate bounds; CA-07, CA-08, CA-13 |
| C-05 | C_Discount / Apply selected discount | Basic 5, FA-01, FA-02, FA-03 | Common calculation contract; no Coupon/fixed/percentage; CA-01–CA-06, CA-18; shared contract tests later |
| C-06 | C_Complete / Complete PriceQuote | Basic 6–7, all success paths | Result invariant and CNY; CA-01–CA-06, CA-16, CA-18 |
| C-07 | C_Refuse / Return refusal | FE-01–FE-07 | Distinguishable reason and no quote/full-price fallback; CA-07–CA-15; unchanged inputs on failures |
| E-01 | E_Cart / Cart | Domain Cart; basic 1–2 | Cart value; no mutation |
| E-02 | E_CartLine / CartLine | Domain CartLine; basic 1–4 | Product reference and bounded quantity |
| E-03 | E_Product / Product | Domain Product; basic 3–4 | Trusted authoritative cents/CNY |
| E-04 | E_Coupon / Coupon | Domain Coupon; FA-01, FA-02 | Trusted definition, no consumption or state mutation |
| E-05 | E_PriceQuote / PriceQuote | Domain PriceQuote; basic 6–7 | Success-only monetary result |

## Sentence-to-responsibility map

| Text anchor | Represented responsibility / communication | Input/output covered | Requirement |
|---|---|---|---|
| Basic 1 | Shopper ↔ Quote request port ↔ Check Cart request | Product codes/quantities, CNY, absent Coupon, explicit UTC instant | RF-01, RF-10; RN-01, RN-05 |
| Basic 2 | Check Cart request ↔ Cart / CartLine; failure ↔ Return refusal | Nonempty collection, quantity type/range, currency, instant, Coupon cardinality | RF-01, RF-09, RF-10; RN-01, RN-02, RN-05 |
| Basic 3 | Check Cart request ↔ Resolve trusted catalog values ↔ Product | Codes resolve to authoritative nonnegative integer cents and CNY; client price cannot override | RF-01, RF-09 |
| Basic 4 | Resolve trusted catalog values ↔ Total Cart lines ↔ CartLine / Product | Quantity × authoritative unit cents summed as integer subtotal | RF-02; RN-01 |
| Basic 5 | Total Cart lines ↔ Check Coupon eligibility ↔ Apply selected discount | Absent Coupon selects zero; alternative branches below | RF-03; RN-06, RN-08 |
| Basic 6 | Apply selected discount ↔ Complete PriceQuote ↔ PriceQuote | Subtotal, bounded discount, difference payable and CNY | RF-08; RN-01, RN-03, RN-08 |
| Basic 7 | Complete PriceQuote ↔ Quote request port ↔ Shopper | One successful PriceQuote result | RF-08; RN-07 |
| FA-01 | Resolve trusted catalog values ↔ Coupon; Check Coupon eligibility ↔ Coupon; Apply selected discount ↔ Complete PriceQuote | Fixed definition, configuration/expiry/minimum checks, capped fixed cents; resumes at basic 6 | RF-04, RF-06, RF-07; RN-03, RN-05, RN-06 |
| FA-02 | Same Coupon lookup/eligibility responsibilities; Apply selected discount ↔ Complete PriceQuote | Percentage basis points, integer floor; resumes at basic 6 | RF-05–RF-07; RN-01, RN-04–RN-06 |
| FA-03 | Total Cart lines ↔ Check Coupon eligibility ↔ Apply selected discount ↔ Complete PriceQuote | Nonempty zero subtotal remains valid; zero result only when Coupon absent/eligible; minimum failure remains FE-06 | RF-01, RF-04, RF-05, RF-07–RF-09 |
| FE-01 | Check Cart request ↔ Return refusal ↔ Quote request port | Invalid Cart/quantity/currency/instant/Coupon cardinality reason; terminates without quote | RF-01, RF-09, RF-10; RN-01, RN-02, RN-05, RN-07 |
| FE-02 | Resolve trusted catalog values ↔ Product; ↔ Return refusal ↔ Quote request port | Unresolved Product code; terminates | RF-09; RN-07 |
| FE-03 | Resolve trusted catalog values ↔ Product; ↔ Return refusal ↔ Quote request port | Invalid authoritative unit cents/CNY; terminates | RF-01, RF-09; RN-01, RN-07 |
| FE-04 | Resolve trusted catalog values ↔ Coupon; ↔ Return refusal ↔ Quote request port | Unknown supplied Coupon code; terminates without ignoring it | RF-06; RN-07 |
| FE-05 | Check Coupon eligibility ↔ Coupon; ↔ Return refusal ↔ Quote request port | Evaluation instant ≥ expiry, including equality; terminates | RF-06; RN-05–RN-07 |
| FE-06 | Check Coupon eligibility ↔ Coupon; ↔ Return refusal ↔ Quote request port | Subtotal below minimum, including zero subtotal when minimum >0; terminates | RF-07; RN-06, RN-07 |
| FE-07 | Check Coupon eligibility ↔ Coupon; ↔ Return refusal ↔ Quote request port | Invalid definition before applying a rule; terminates | RF-09; RN-01, RN-05–RN-08 |
| All paths / postconditions | Every control uses read-only input semantics; only Complete PriceQuote emits a successful PriceQuote | No Cart/catalog mutation, Coupon redemption or order creation; repeated identical inputs are deterministic | RF-10; RNF-02 |

Every behavior-bearing basic-flow row and every local FA/FE row maps here. Every BCE element has a textual origin above. Policy substitution, dependency direction, Python compatibility and executable proof of no mutation are later design/test checks; they are not established by this analysis table.

## Data correspondence

| Interface or trusted input | Domain/value correspondence | Responsible control |
|---|---|---|
| Shopper Product code and quantity | CartLine.Product reference and quantity | Check Cart request; Resolve trusted catalog values |
| Shopper currency / evaluation instant / optional Coupon code | Request-level values; Coupon lookup identity and eligibility instant | Check Cart request; Check Coupon eligibility |
| Trusted Product unit cents and currency | Product price/currency | Resolve trusted catalog values; Total Cart lines |
| Trusted Coupon kind/value, minimum cents and expiry UTC | Coupon definition/eligibility values | Resolve trusted catalog values; Check Coupon eligibility; Apply selected discount |
| Success subtotal/discount/payable/CNY | PriceQuote values | Complete PriceQuote |
| Refusal category / offending value | Interface-only result data, not a new domain entity | Return refusal |

No entity discovery delta remains: Cart, CartLine, Product, Coupon and PriceQuote all exist in the supplied domain model. Boundary-only/request-only fields do not require new domain classes.

## Local semantic check and remaining limits

- All actor links reach a boundary. All boundary/entity communication reaches controls. The diagram uses undirected communication links consistently.
- The trusted catalog is internal, so Product/Coupon resolve directly as domain entities through a control. No fictitious external catalog actor or technical repository entity is added.
- Alternative-only Return refusal and Coupon are colored. Other controls/entities are shared with the basic success flow and remain uncolored.
- The control cluster expresses this one goal's analysis responsibilities. Its number of links may trigger a heuristic warning. It does not prescribe a manager class or excuse one; sequence/class design must allocate the responsibilities explicitly.
- Interface syntax is defined locally; no existing GUI/protocol was supplied. Source evidence is fictional baseline plus explicit demo interface interpretation.
- Independent PDR and executable checks remain pending. This author check is not formal human/business acceptance or proof of UML/ISO conformance.
