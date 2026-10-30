# Change impact and controlled replay

This example uses real corrections and a bounded strategy extension to exercise source tracing, stable identities, reinspection and handoff. This publication normalizes the relevant historical illustrations under `review-history/`; it does not reproduce a machine-specific audit archive or claim those adapted files retain historical local byte hashes.

## 1. PDR: remove an unsupported business rule

The analysis author required rejection of a negative Coupon minimum in the glossary, FE-07 and CA-13. The requirements had not decided that policy, and the independent oracle explicitly excluded it from its accepted business cases.

| Artifact/evidence | Actual impact and disposition |
|---|---|
| Business baseline and independent oracle | Preserved. Expected results were not changed to fit the analysis. |
| Glossary, interface contract and use case specification | Removed the invented sign policy, retained integer-cent type checks and made the unresolved scope explicit. |
| CU/FA/FE/CA identities | Preserved; renumbering did not hide the correction. |
| Robustness analysis | No added/removed responsibility or domain concept; relationships were unchanged. |
| Initial PDR | PDR-01-F01 was Open and prevented transition to detailed design. |
| Reinspection | Four analysis validators and PDR were rerun; a separate reviewer checked the affected text and flow equivalence. |
| Handoff | F01 Closed; the technical demonstration could enter stage 6. Formal human/business acceptance remained unverified. |

Read the [initial specification illustration](review-history/pdr-initial-specification.md), [initial glossary](review-history/pdr-initial-glossary.md), [correction details](03-spec/pdr-corrections.md), [PDR](05-pdr/PDR-01.md) and [analysis handoff](handoffs/analysis.json).

Ten PDR diagnostics about absent alternative/exception behavior were a separate format issue. The compact rows already had triggers, actions and exits; equivalent numbered steps made them recognizable to the supported parser. They were not ten newly discovered missing business flows. Five conceptual attribute warnings were examined through the glossary and actual data paths, rather than silenced by adding implementation attributes to the conceptual view.

## 2. Interactions: correct break scope and coverage

The [initial sequence](review-history/sequence-initial.puml) placed `break` inside `loop`/`opt` while its legend claimed whole-quote termination. Explanatory text cannot enlarge a UML fragment's scope: a refusal could still be followed by the outer interaction's success behavior.

The author obtained nested lookup/check results first, then used outer, guarded breaks to propagate refusal and terminate the quote. Product/Coupon adapters may refuse selected malformed setup; Cart also validates values returned by a replacement catalog. These paths were reconciled with actual code.

Independent CDR then found that the [intermediate frames](review-history/sequence-before-frame-correction.puml) still rendered too narrowly. The maintained [DS-01](06-interactions/sequence.puml) has twelve top-level terminating breaks, each covering all nine current lifelines through an accurate note over the actual first/last participants. No fictitious call is added.

The local PlantUML 1.2026.7 exercise encountered a rendering failure with `note across` in these fragments; explicit endpoint notes rendered successfully. PriceQuote is represented as an internally constructed completion value and successful reply, without a separate result lifeline. Its constructor invariants remain in the model, decisions and code. Former explicit creation-message ID **DS-01-M10 is retired and not reused**; construction was not recast as an ordinary method.

Affected scope: DS-01 fragment organization, exception replies, lifecycle explanation and their provenance/test links. Business RF/RN, CU/FA/FE, DR-01, domain vocabulary and independent monetary expectations remain unchanged. Recheck sequence notation, operation allocation, CDR and the actual refusal-to-completion paths. Rendering success alone does not establish those semantics.

Background: [IBM's sequence-diagram explanation](https://developer.ibm.com/articles/the-sequence-diagram/) describes the direct enclosing scope of a nested break; [OMG's Break definition](https://www.omg.org/spec/UML/ISO/19505-2/PDF) also specifies enclosing-fragment/lifeline coverage. The example's final judgment is recorded in [CDR](08-cdr/CDR-01.md).

## 3. CDR: align multiplicity with shared immutable values

Independent review found that `Cart "1" --> "0..*" CartLine` required each CartLine instance to relate to exactly one Cart, contradicting the declared sharing of immutable line values and actual Python object reuse. Plain association does not remove a multiplicity constraint.

The [corrected model](07-class-model/classes.puml) uses `Cart "0..*" --> "0..*" CartLine`: a line value may be unused or referenced by multiple Carts. A prevalidation Cart may be empty; `Cart.validate` enforces the nonempty valid-input condition. Code behavior and immutability remain unchanged.

The correction affects MC-01's association end, its explanation and generated inspection declarations. It changes no business algorithm, CU/DR/DS identity or oracle amount. The reviewer examined the [initial model illustration](review-history/classes-initial.puml), successfully exercised two Carts sharing one line instance, and reinspected model/provenance/headers after correction. See CDR-01-F01 and the [header inspection](08-cdr/header-inspection.md).

## 4. Controlled extension: half off, capped at CNY 20.00

This is an **RNF-01/RNF-04 technical variation probe**. Default registration still supports the specified fixed/percentage Coupons, and the original thirty CP cases still test that baseline. A third Coupon is not silently added to the accepted business scope.

[CappedHalfDiscount](09-reference-implementation/extension_demo.py) calculates `min(subtotal // 2, 2000)`. The exercise adds HALFCAP to a trusted test fixture, copies the default registrations and adds a `capped_half` factory at the composition boundary. QuoteService, Cart, PriceQuote and the existing algorithms do not need to recognize the new kind.

Run from the repository root:

```bash
python3 examples/order-pricing/09-reference-implementation/extension_demo.py
```

| Subtotal, cents | Literal expected discount | Expected payable |
|---:|---:|---:|
| 0 | 0 | 0 |
| 333 | 166 | 167 |
| 25500 | 2000 | 23500 |

The command prints actual results and protected core-file hashes, and writes a local `09-reference-implementation/evidence/extension.json`. It exercises the same core with default and additional registration; its before/after hashes are execution evidence, not proof of a historical Git change set. Shared tests check accepted input domain, integer bounds, repeatability and unchanged policy state for the ordinary strategies and extension.

| Artifact | Impact of this probe |
|---|---|
| Baseline RF/RN, CU-01, DR-01 and independent oracle | Preserved; business acceptance scope is not expanded. |
| DS-01 extension point and MC-01 DiscountPolicy contract | Preserved; the existing abstraction accommodates this pure calculation. |
| Extension code and test setup | New strategy, trusted fixture, factory registration, literal expectations and shared contract vectors. |
| CDR/SOLID assessment | Check strengthened preconditions, result bounds, core edits and unrelated dependencies. |
| A future approved third business Coupon | Requires a revised business baseline/expectations and affected specification/design review. This technical probe does not replace that decision. |

The evidence supports a working extension point for this selected variation. It does not promise zero core changes for every future rule or universal substitutability over all possible inputs.

## 5. Detect stale review inputs

The local exercise copied reviewed analysis materials and their handoff into an isolated temporary directory, changed the copied requirement and invoked the same verifier. It observed **exit 2 / BLOCKED**, identifying the changed requirement before downstream checks began. The actual example sources were unchanged.

The published verifier retains source-baseline checks. [VALIDATION.json](VALIDATION.json) records publication verification; fresh local runs write their own results under `validation/latest/`. A hash establishes file identity, not semantic approval. After a change, analyze impact, correct affected artifacts and obtain genuine affected-scope review before recording replacement handoff hashes.
