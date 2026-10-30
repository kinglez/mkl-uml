# MC-01 element provenance and Python mapping

Maintained with DS-01/DS-02 and the actual reference code. All five problem concepts preserve the frozen domain vocabulary. Stable class IDs below are local model identities; class names and PlantUML aliases are separate. No ID is retired or reused in this example.

| ID | Class | State / member source and Python mapping |
|---|---|---|
| MC-01.C01 | Cart | The lines association maps to `Cart.lines: Tuple[CartLine,...]`, read-only; zero lines may represent an invalid request before validate(). Validate/subtotal come from DS-01-M03/M05; RF-01/02/09. |
| MC-01.C02 | CartLine | `productCode`, `quantity`: submitted identity/quantity, interface contract and RN-02. Immutable value; its cart-wide validation belongs to Cart. |
| MC-01.C03 | Product | `code`, `unitPrice`, `currency`: trusted Product identity/price/currency; RF-01 and glossary. Immutable data, no independent mutable lifecycle or unrelated operations. |
| MC-01.C04 | Coupon | `code`, `kind`, `minimumSubtotal`, `expiresAt`, `currency`, `config`: trusted definition and eligibility values from interface/glossary. config is a detached read-only top-level Mapping of configured scalar rule data (AD-04/06), not another domain entity. Typed expiry is decoded by the adapter; deliberately bad config can be refused before calculation. check_eligibility comes from M08. |
| MC-01.C05 | PriceQuote | subtotal/discount/payable/currency from RF-08 and all successful postconditions; constructor/`__post_init__` enforces bounds/arithmetic. It stores a completed value; it does not require synthetic getters or an ordinary create method. |
| MC-01.C06 | ProductCatalog | Application-owned lookup-only Protocol from AD-02, RNF-05; M04. Optional means absent code; Refusal means malformed selected trusted data. |
| MC-01.C07 | CouponCatalog | Separate lookup-only Protocol from AD-02, RNF-05; M06. |
| MC-01.C08 | PolicyResolver | Application-owned selection contract from AD-03/04; M07. |
| MC-01.C09 | DiscountPolicy | Pure calculation Protocol from RN-08, RNF-04; M09; same accepted input/result contract for every supported replacement. |
| MC-01.C10 | NoDiscount | Explicit no-Coupon strategy; RN-03/RF-03; realizes C09. No configuration state. |
| MC-01.C11 | FixedDiscount | amount: configured fixed cents (RF-04), checked at construction; cap operation realizes C09. |
| MC-01.C12 | PercentageDiscount | basisPoints: configured rate (RF-05), checked at construction; integer-floor operation realizes C09. |
| MC-01.C13 | QuoteService | product_catalog/coupon_catalog/policy_resolver are constructor-injected references. Python fields have a leading underscore (`_product_catalog`, etc.); UML visibility carries privacy. quote from M02, AD-01/02/09. No catalog or order mutation API. |
| MC-01.C14 | Refusal | reasonCategory: explicit failure output from every FE, mapped by boundary; AD-07. Python Exception subclass is a technical language choice, not domain generalization. |
| MC-01.C15 | QuoteRequestPort | service reference maps to `_service`; handle from M01/DS-02; AD-05/07. |
| MC-01.C16 | InMemoryCatalog | products/coupons map to `_products`/`_coupons`: detached trusted setup maps, AD-06. Lookup methods realize C06/C07; snapshot from DS-02 and RNF-02. snapshot returns a detached copy; read-only quoting never consumes a Coupon. |
| MC-01.C17 | RegistryPolicyResolver | registrations maps to `_registrations`: copied kind→factory map, AD-04. resolve realizes C08. Factory functions live at the composition root; a callable is not fabricated as a domain class. |

## Relationships and significant state

- Cart → CartLine is the named `lines` association, multiplicity `0..*` at both ends: an immutable line value may be unused or shared across Cart values, and the target permits the representable prevalidation input; after validate(), at least one line. It maps to one tuple field, not duplicate storage. Ordinary navigation allows immutable line values to be shared; exclusive composition ownership is not asserted.
- CartLine's Product identity is implemented with productCode; its dependency expresses resolution semantics, not a stored Product pointer. Cart uses Product values for subtotal: that **technical operation dependency** derives from M05/AD-01, rather than a new conceptual business relationship.
- PriceQuote depends on the Cart and optional Coupon it summarizes. It stores the four observable values, no persistent Cart/Coupon object association or lifecycle ownership is invented.
- QuoteService's typed private fields are its three stored references. Dashed dependencies expose their use without generating duplicate association fields. QuoteRequestPort likewise has one `_service` field and a use dependency.
- Catalog/registry/policy realizations express structural contracts. They do not establish behavioral substitution by the arrow alone; see shared tests and SOLID.md.
- Hidden directional links are layout constraints only, not additional dependencies or association properties.

Independent CDR F01 corrected the initial Cart end of the lines association from `1` to `0..*`. Ordinary association alone did not permit sharing while its explicit opposite-end multiplicity still required exactly one Cart. Both ends now allow unused/shared immutable line values, matching the Python representation and stated design. A normalized initial model illustration is retained in `../review-history/classes-initial.puml`; the target `0..*` before validation and valid-Cart nonempty rule remain unchanged.

All modeled attributes/state have the grouped sources above. No technical requirement is added to CU text merely so its class field matches a word-search heuristic. Read-only dataclass fields and the supported Coupon scalar configuration do not claim arbitrary recursively immutable external Python objects.

## Language and generated-header limits

String→str; int excludes bool at relevant validation points; DateTime→aware datetime with zero UTC offset; Optional<T>→typing.Optional[T]; Map<K,V>→typing.Mapping[K,V]; the lines collection→Tuple[CartLine,...]; void→None; PolicyFactory→Callable[[Coupon],DiscountPolicy]. UML signatures express validated contracts. Malformed public requests/configuration are input to explicit checks, not proof that Python annotations validate data.

Generated Java headers are inspection aids for an implementation-neutral model. They cannot by themselves enforce Python immutable dataclasses, tuples, MappingProxyType, integer/non-Boolean validation, aware UTC, callable factories or exception propagation. The independent header inspection must preserve such translation limits and compare the significant operations; generated placeholders are not an executable production implementation.

## Remaining source-profile warnings

Data-only CartLine/Product are deliberate immutable values; Cart uses their state for cart rules. PriceQuote has constructor invariants implemented in `__post_init__`, rather than a fabricated domain operation. The heuristic's anemia warning is therefore not accepted without a demonstrated misplaced responsibility. The Cart→Product dependency is M05/AD-01 technical use. Field-name mismatches such as expiresAt/config are supported by actual interface semantics and AD-04/06; a lack of literal spelling in the CU is not missing state provenance. Independent CDR must confirm these adjudications against actual code.
