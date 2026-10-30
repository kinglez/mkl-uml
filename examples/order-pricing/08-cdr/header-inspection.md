# CDR-01 — generated-declaration inspection

This publication adaptation summarizes the independent technical reviewer (AI)'s actual inspection on 2026-10-29 and final correction check on 2026-10-30. It preserves the review meaning while normalizing paths and presentation; it is not an original-byte or human-signed inspection record. Current publication checks are recorded in [VALIDATION.json](../VALIDATION.json).

**Historical technical coverage: checked, with the conversion limits below. Human header inspection and formal organizational acceptance remain unverified.**

The actual MKL generator exited **0** and produced [headers.java](headers.java) from [MC-01](../07-class-model/classes.puml). The reviewer compared the declarations with the model, interactions, [member provenance](../07-class-model/provenance.md) and [Python implementation](../09-reference-implementation/README.md). The generator's “No typing gaps” message was not treated as a fidelity guarantee.

## Model → declaration → implementation

| Inspected content | Result and interpretation |
|---|---|
| Classifiers | All **17** modeled classifiers are represented once. Interfaces remain interfaces; three policy, two catalog and one resolver realizations produce six appropriate `implements` relationships. No test harness or extra domain entity is invented. |
| Explicit attributes | All **25** retain their intended name, type and visibility. Python's private leading underscores map to UML visibility, rather than requiring duplicate fields. |
| Cart association | The one target collection becomes `List<CartLine> linesCartLine`, with multiplicity in a comment. This synthetic role-plus-target name maps to Python `lines: Tuple[CartLine, ...]`; it is one collection, not extra storage. After F01, both association ends are `0..*`. |
| Ordinary operations | All **16** significant declarations are retained: two on Cart, Coupon eligibility, four interface contracts, three policies, QuoteService.quote, QuoteRequestPort.handle, three InMemoryCatalog operations and RegistryPolicyResolver.resolve. Parameter order, individual types, nested Map/Optional forms and result types were compared. |
| Receiving contracts | DS-01 M01–M09 and DS-02 calls map to receivers or their realizations. Lookup returns Optional values, resolution returns DiscountPolicy, totaling/calculation return integer cents, quote returns PriceQuote and handle/snapshot return maps. `validate` and `check_eligibility` return void/None; narrative validated/eligible replies acknowledge status rather than returning extra objects. |
| Lifecycle and replies | Internal PriceQuote construction and `__post_init__` enforce the documented invariant; they do not require an invented ordinary `PriceQuote()` operation. Former explicit creation message DS-01-M10 is retired. Replies and Refusal labels do not create reverse receiver methods. |
| Nonstored dependencies | Cart's Product use and PriceQuote's Cart/Coupon origin dependencies do not become fabricated object-reference fields. The actual result stores its four observable values. |
| Derived meaning | Payable is a completed stored value constrained to subtotal minus discount, not a modeled derived-property accessor. Its arithmetic and validation come from the constructor contract/code, not an empty field declaration. |

The final historical regeneration followed the stable author handoff and exited **0**. Compared with the initial output, only Cart's source-multiplicity comment changed from `1` to `0..*`; signatures and classifier membership were unchanged. The retained [initial model illustration](../review-history/classes-initial.puml) explains that correction. Machine-specific generation logs and the original header snapshot are not part of this publication.

## Conversion limits

- `DateTime` is a documented alias for an aware zero-offset Python `datetime`; `PolicyFactory` means `Callable[[Coupon], DiscountPolicy]`. The declarations do not implement these types.
- Java-like `String`, `Optional`, `Map` and `List` forms correspond to Python `str`, `Optional`, `Mapping` and tuple storage. Imports, constructors, wiring and usable method bodies are intentionally absent.
- Java `int` does not preserve Python's arbitrary precision or exclusion of booleans. Exact integer and monetary-domain checks belong to the reference implementation.
- Generated public fields do not enforce UML `{readOnly}`, frozen dataclasses, detached snapshots or tuple/read-only mapping behavior. Those properties were checked in the actual code/tests.
- `Map<String,Object>` request/configuration declarations depend on the supplied schema and validation contracts; generic containers alone do not establish business semantics.
- Python Exception inheritance, propagation and constructor validation are language behavior beyond this declaration view. Refusal's generated header is not a working Python exception implementation.

These declarations support completeness and dependency inspection. They are **not executable production Java**, a universal model-to-code conversion proof or evidence of human acceptance. The [CDR record](CDR-01.md) preserves the independent technical conclusion and its boundary.
