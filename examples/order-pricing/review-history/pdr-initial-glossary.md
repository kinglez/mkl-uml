> Historical illustration, normalized for publication. Superseded; use the maintained stage artifact for current behavior.

# Domain vocabulary and scope

Source: [baseline 1](../00-input/requirements.md). This is fictional demo vocabulary. No customer or human decision maker has approved it.

The conceptual profile deliberately has no attributes, operations or drawn multiplicities. The following data meanings retain the information needed for analysis; omitting a multiplicity on the diagram does not mean one.

| Concept | Meaning and relevant values | Relationship / constraint | Source |
|---|---|---|---|
| Cart | The Shopper's supplied collection of CartLine values for this quote | A successful quote requires at least one CartLine. Quoting does not mutate it. | RF-01, RF-09, RF-10 |
| CartLine | One requested Product code and quantity | One Product per line; integer quantity 1–99 inclusive, excluding booleans. Repeated Product codes may occur on separate lines; each supplied line contributes to the sum, with no merge or mutation required. | RF-01, RF-02, RN-02; line-by-line sum interpretation |
| Product | A catalog item with a stable Product code, authoritative unit cents and currency | Price may be zero, must be nonnegative integer cents; supported currency is CNY. Product data originates from the trusted server-side snapshot, not the CartLine. | RF-01, RF-02, RF-09, RN-01 |
| Coupon | An optional named offer: code, rule kind, rule value, minimum subtotal cents, expiry instant | Fixed cents are nonnegative; percentage basis points are 0–10000 inclusive. Minimum is nonnegative integer cents. Expiry and evaluation instant are timezone-aware UTC. A PriceQuote has zero or one applied Coupon. | RF-04–RF-07, RF-09, RF-10, RN-01, RN-05, RN-06 |
| PriceQuote | An immutable-in-meaning result containing subtotal cents, discount cents, payable cents and CNY | Describes the submitted Cart at the supplied catalog snapshot and evaluation instant; zero or one Coupon. `0 <= discount <= subtotal`; `payable = subtotal - discount`. No result survives as a successful quote after a failure. | RF-08, RF-10, RN-03, RN-07 |

Money and evaluation instant are values described here, not separately identified business entities. Fixed and percentage offers are Coupon rule configurations; no solution Strategy, Repository, Controller or algorithm class belongs in this conceptual view. Coupon expiry is a property condition, not a tracked lifecycle entity in this bounded scenario.

## Other vocabulary origins

| Term | Classification | Origin |
|---|---|---|
| Shopper | External actor role, with no independently tracked profile in this demo | User goal and boundary in baseline 1; ACT-01 in the use case view |
| Quote request port | Named local machine interface, not a domain class or invented GUI | [interface contract](../03-spec/interface-contract.md) |
| Trusted catalog snapshot | Trusted input provenance for Product/Coupon values inside the system boundary | Baseline 1 trusted server-side demo data |
| Failure reason | Interface result information, with no independent business identity/lifecycle | RF-06, RF-07, RF-09, RN-07 |
| DiscountPolicy | Future design-contract vocabulary; deliberately absent from the domain model | RNF-01, RNF-04; allocation deferred until detailed design |

## Modeling decisions and limits

- The four plain associations express evidenced conceptual relations. Composition is unnecessary because deletion/exclusive part lifetime is not part of this quote goal.
- Shopper is an actor only here. Actor names need not become domain classes when no separate business state requires them.
- The result references a Cart concept without asserting storage, object identity, persistence or a later order lifecycle.
- The specification and robustness analysis introduce no missing domain concept. Domain delta for this scope: none.
- New diagram aliases are local syntax. CU-01 comes from the baseline; no existing trace identifier has been renumbered.
