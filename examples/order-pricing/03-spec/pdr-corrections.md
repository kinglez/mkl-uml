# PDR correction handoff

This publication summary preserves the corrections made after the initial PDR. The original business requirements and independent oracle were not changed. The retained [initial glossary](../review-history/pdr-initial-glossary.md) and [initial specification](../review-history/pdr-initial-specification.md) are publication-normalized historical illustrations, not original-byte evidence. The actual independent closure is summarized in [PDR-01](../05-pdr/PDR-01.md); current publication checks are recorded in [VALIDATION.json](../VALIDATION.json).

## Semantic correction: PDR-01-F01

| Artifact | Initial problem | Corrected meaning |
|---|---|---|
| Domain glossary, Coupon | Required a nonnegative minimum. | Minimum remains integer cents; the outcome for a negative value is outside the bounded business baseline. |
| Interface contract | A broad invalid-minimum category could imply sign-based rejection. | Noninteger minimum is invalid under the representation contract. Negative-minimum acceptance/refusal is separately identified as undefined. |
| FE-07 | Grouped negative minimum with invalid fixed/rate configuration. | Retains negative/noninteger fixed cents, noninteger minimum and invalid rates; minimum sign alone has no prescribed outcome. |
| CA-13 | Required negative-minimum refusal. | Retains supported fixed/rate/type failures and removes the unsupported sign-policy test. |
| Specification limits | Did not expose the policy gap. | Explicitly excludes negative-minimum acceptance/refusal from the verified policy scope. |

This removes an unsupported analysis assumption. It does not replace it with a requirement to accept negative minima. Nonnegative Product prices, exact integer quantities/cents, percentage bounds/floor, fixed caps, expiry equality, Coupon eligibility and read-only refusal behavior are preserved.

## Representation correction: ten numbered flow details

The compact summaries already stated their guards, actions and exits. To use the PDR parser's supported form, adjacent numbered System-step tables were added without changing the behavior:

| Stable flow | Preserved behavior and exit |
|---|---|
| FA-01 | Use the lesser of configured fixed cents and subtotal; resume basic step 6. |
| FA-02 | Calculate `subtotal * basisPoints // 10000`; resume basic step 6. |
| FA-03 | Keep the valid nonempty zero-priced Cart, derive zero subtotal and continue at step 5. An absent/eligible Coupon can produce a zero quote; an ineligible Coupon still refuses. |
| FE-01 | Identify the invalid request condition, return its refusal and terminate with no quote. |
| FE-02 | Identify the unknown Product, return its refusal and terminate. |
| FE-03 | Identify invalid trusted Product data, refuse and terminate; a caller price cannot repair it. |
| FE-04 | Refuse the unknown Coupon and terminate without ignoring it or falling back to full price. |
| FE-05 | Refuse expiry, including equality, and terminate. |
| FE-06 | Refuse a known valid unexpired Coupon below its minimum and terminate. |
| FE-07 | Refuse invalid configuration before calculation and terminate, with the F01 correction above. |

All CU/FA/FE/RF/RN/RNF/CA IDs, guards, resumes and terminations remain stable. Explicitly repeating common no-quote/no-mutation postconditions is a presentation expansion. The `Alternative flows` heading was aligned with supported parser vocabulary. No domain or BCE relationship changed in this correction.

## Verification and closure

The analysis author (AI) reran all four analysis validators and the PDR CLI. The independent technical reviewer (AI) then compared the corrected text against the retained behavior, reread the unchanged baseline/oracle and reran PDR with all four supported inputs.

- The final historical PDR run exited **0**, with zero behavior errors, zero non-domain entities and zero BCE syntax violations.
- Five no-attribute warnings remained. The reviewer discharged them through the conceptual-view profile, glossary and actual data-correspondence evidence; no attributes were added merely to silence a heuristic.
- The domain CartLine-generalization guess and robustness control-cluster diagnostic were evaluated semantically, rather than treated as automatic requirements to alter the design.
- **PDR-01-F01 was independently closed before detailed design.** The corrected example was technically ready for stage 6; formal human/business acceptance remained **Not fully verified**.

Numbered syntax makes these flows recognizable to the parser. The semantic comparison, source fidelity and data paths establish the bounded technical conclusion; a green score alone does not.
