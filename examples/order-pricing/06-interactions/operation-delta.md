# Operation allocation — DS-01 / DS-02 to MC-01

Scope: CU-01 all specified behavior, plus the explicitly separate RNF-02 observation protocol. Author role: design author (AI). No new business concept, actor, user goal or domain discovery is introduced. New solution collaborators derive from AD-01–AD-09 in `DESIGN_DECISIONS.md`, not invented use-case steps.

## Classified call sources

Stable message IDs are comments immediately before the corresponding DS-01 calls. Repeated failure replies are indexed by their existing local FE identities; their spelling is not an operation allocation.

| Call source | Receiving classifier and significant operation | Required responsibility / source |
|---|---|---|
| DS-01-M01 | QuoteRequestPort.handle(request: Map): Map | Admit the allowed request fields, validate transport-level shape/currency/UTC/cardinality; convert successful quote or refusal to one observable response. Quote request port from analysis; AD-05/07. |
| DS-01-M02 | QuoteService.quote(cart: Cart, currency: String, couponCode: Optional<String>, evaluatedAt: DateTime): PriceQuote | Coordinate this one goal through small collaborator contracts, propagate refusal and create a successful quote only after all checks. AD-01/02. |
| DS-01-M03 | Cart.validate(): void | Nonempty cart; valid Product identity representation and integer non-Boolean quantity 1–99. RF-01/09; RN-02. |
| DS-01-M04 | ProductCatalog.lookup_product(code: String): Optional<Product> | Resolve authoritative Product or absence. Implemented by InMemoryCatalog; malformed selected trusted data may refuse FE-03. RF-01/09; AD-02/06. |
| DS-01-M05 | Cart.subtotal(products: Map<String,Product>, currency: String): int | Sum each Product price × quantity; zero subtotal valid; defensive validation of returned Product values. RF-02; FA-03; AD-01. |
| DS-01-M06 | CouponCatalog.lookup_coupon(code: String): Optional<Coupon> | Resolve Coupon or absence; malformed selected setup, including expiry decoding, refuses FE-07. RF-06/09; AD-06. |
| DS-01-M07 | PolicyResolver.resolve(coupon: Optional<Coupon>): DiscountPolicy | Absent Coupon selects NoDiscount. RegistryPolicyResolver resolves registered factories and validates fixed/rate construction; no workflow minimum/expiry check here. AD-03/04. |
| DS-01-M08 | Coupon.check_eligibility(subtotal: int, evaluatedAt: DateTime, currency: String): void | Common configuration, exact expiry and threshold checks; refusal terminates; no discount calculation. RN-05/06/08; FE-05/06/07. |
| DS-01-M09 | DiscountPolicy.discount(subtotal: int, currency: String): int | Pure common contract; NoDiscount, FixedDiscount and PercentageDiscount implement it. Basic/FA-01/FA-02; RNF-04. |
| DS-02, first/last call | InMemoryCatalog.snapshot(): Map | Return a detached copy for actual before/after state comparisons. RNF-02; AD-06. Technical observation is outside Shopper CU behavior. |
| DS-02, middle call | QuoteRequestPort.handle(request: Map): Map | Reuse the actual request boundary in verification; it adds no new API. |

InMemoryCatalog's two lookup operations implement the catalog Protocol contracts and inherit those call sources. RegistryPolicyResolver.resolve implements PolicyResolver.resolve. The three policies' discount methods implement the same receiving contract; no separate fictitious call to each concrete class is required. Private validation/conversion helpers and ordinary dataclass construction are intentionally omitted from the significant-operation view.

## Lifecycle, returns and absence of signals

- **DS-01-M10 is retired from the explicit message view**, with its original preserved in history. Completion constructs PriceQuote internally with subtotal, discount, derived payable and CNY, then returns it by value. The maintained completion note plus RF-08/AD-01 preserve its constructor/`__post_init__` invariant. There is no result lifeline or ordinary `PriceQuote()` operation in the maintained interaction. This is not an early-created result or a loss of the required creation behavior.
- All `<<reply>>` arrows return to the original synchronous caller. A returned Product, refusal, successful quote or discount does not add a method to that caller.
- No asynchronous operation, Signal/reception, deletion or persistence lifecycle is claimed.

## Analysis responsibility allocation

| DR-01 control | Realized responsibilities |
|---|---|
| Check Cart request | Port.handle plus Cart.validate; direct service inputs are also checked defensively. |
| Resolve trusted catalog values | ProductCatalog/CouponCatalog lookups, InMemoryCatalog decoding; core can use different conforming ports. |
| Total Cart lines | Cart.subtotal over trusted Product values; quantities and zero-priced products preserved. |
| Check Coupon eligibility | Coupon.check_eligibility plus resolver/factory configuration checks, before discount. |
| Apply selected discount | DiscountPolicy.discount with the actual resolved strategy. |
| Complete PriceQuote | QuoteService checks policy result and creates invariant-preserving PriceQuote. |
| Return refusal | Refusal propagates through QuoteService to Port.handle and one unsuccessful result; no quote. |

The named analysis boundary `Quote request port` becomes the software class `QuoteRequestPort`; this is a declared representation mapping, not a missing interface or additional goal. Seven logical controls become cohesive rules, ports and one goal coordinator, not seven Controller classes.

## Corrections and mechanical limits

The initial author sequence is retained in `../review-history/sequence-initial.puml`. The coordinating review identified a real UML issue: a break inside loop/opt does not abort the entire quote. The maintained sequence moves every terminating break to the outer interaction. Product resolution stops after absence/refusal; optional Coupon calls return their status before outer refusal propagation. Independent CDR then identified the remaining narrow-frame coverage issue: every outer break now spans all nine existing lifelines through an accurate explanatory note. No fake message or early result is introduced. These corrections repair interaction semantics, not the business baseline. The implementation's exception behavior was independently read while reconciling the diagram.

The frame correction follows the enclosing-fragment/all-lifeline requirement in [OMG ISO/IEC 19505-2:2012, §14.3.3](https://www.omg.org/spec/UML/ISO/19505-2/PDF), independently checked by the CDR reviewer. Actual installed-renderer `note across` attempts failed with exit 200; the original local run retained those logs. This publication retains the corrected model and normalized historical illustrations. The explicit endpoint note renders correctly. PriceQuote construction is now a completion note and returned value; its former explicit message ID is retired. No class constructor was turned into an ordinary method to work around rendering.

Other initial diagnostics were lexical/profile limits: wrapped DR labels were not recognized by the Controller-word heuristic until actual call/reply labels stated “apply selected discount” / “return failure”; snapshot() has a legitimate RNF-02 contract source but the CLI requires an operation-invoking message. DS-02 records the real observation protocol and receives only applicable scope checks. Neither change invents user behavior. A legend line beginning `Loop` was mistaken for an open fragment; rewording that explanatory sentence preserves its meaning.

Fresh publication checks are summarized in `../VALIDATION.json`; local reruns write diagnostics under `../validation/latest/`. The following author interpretations were independently examined in `../08-cdr/CDR-01.md`:

| Diagnostic | Author adjudication / limit |
|---|---|
| High return proportion | Every returned amount is consumed; repeated exception replies show meaningful refusal propagation and no fallback. These replies establish no reverse operations. |
| QuoteService sends most operation calls | It coordinates a single goal. Validation/arithmetic/eligibility/algorithm rules reside in Cart/Coupon/policies; catalog representation resides in adapters. A call-count threshold does not establish a God Object. |
| 256 path cap | Actual finite sample only; no exhaustive path claim. Semantic flow review and independent literal/runtime tests remain necessary. Mutually inconsistent guards must not be treated as feasible combined scenarios. |
| Boundary name differs | Declared analysis-to-code mapping above. |
| DS-02 has no full CU/support checks | Intentionally technical probe; DS-01 retains all full-CU checks. DS-02 does not discharge business-flow coverage. |

Author verification does not constitute independent CDR or human/business approval.
