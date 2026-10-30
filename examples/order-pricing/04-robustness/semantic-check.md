# Analysis semantic check — author evidence, 2026-10-29

Scope: fictional baseline 1 → conceptual domain → actor goal → CU-01 textual flows → DR-01 BCE responsibilities. This is an actual local author check, not an independent PDR or formal human acceptance.

| Check | Result | Evidence / practical limit |
|---|---|---|
| Source/boundary | Checked | CU-01 retains the supplied goal and read-only scope. Trusted Product/Coupon snapshot stays within Order Pricing; client prices cannot become authoritative. |
| Domain vocabulary | Checked | Five problem concepts; no operations, solution classes, technical repository/entity, premature pattern, unsupported inheritance or exclusive-deletion assertion. Values are in the glossary. |
| Actor/goal | Checked | One external Shopper, one user goal CU-01; every participation has an association. No invented authentication/checkout/CRUD goal or external catalog actor. |
| Basic behavior | Checked | Seven text steps each have a BCE responsibility/link in correspondence.md. Request, success and refusal cross the named Quote request port. |
| Alternatives | Checked | Three local FA identities: fixed cap, percentage floor, nonempty zero subtotal. Shared Coupon lookup/configuration/eligibility precedes calculation, and every branch declares resumption or termination. |
| Failures | Checked | Seven local FE identities cover request validity, unknown/invalid Product, unknown/expired/below-minimum/invalid Coupon. All return a reason and no successful quote, with no full-price fallback. |
| Data coverage | Checked | Product code/quantity, trusted unit cents/CNY, optional Coupon code, rule/minimum/expiry, explicit UTC instant, result amounts/currency and refusal values have identified origins/responsibilities. |
| Requirement links | Checked | All ten RF, eight RN and five RNF identities are retained; RNF design/runtime obligations are explicitly pending. Eighteen acceptance criteria use independent baseline expectations. |
| Entity closure | Checked | Cart, CartLine, Product, Coupon and PriceQuote all resolve to the domain model. No pending entity delta; actor/interface/request-only fields do not need domain classes. |
| BCE local profile | Checked | Four source CLI validators exit 0; robustness has 14 elements and 20 connections. All actor links reach boundaries, and boundary/entity links pass through controls. |
| Rendering | Checked | Installed PlantUML 1.2026.7/Graphviz 15.1.1 produced SVG and PNG offline; author viewed the three PNGs and shortened/wrapped robustness labels to improve readability. The full robustness SVG remains a wide zoomable communication view. |
| Artifact links | Checked | A local Markdown-link existence pass reported zero missing local targets in the four stage folders. |
| Independent review | Partial | Independent PDR and any formal human/business approval are not part of this author check. |
| Runtime/SOLID | Partial | No code, tests, operations, sequence allocation or detailed class design has been created by this agent. Analysis shapes alone prove none of those properties. |

## Initial findings, corrections and retained warnings

The original local run retained its initial and corrected diagnostics. This publication summarizes current execution in `../VALIDATION.json`; rerunning the verifier writes fresh exact commands and diagnostics under `../validation/latest/`.

| Finding | Disposition |
|---|---|
| Text profile counted the prose line beginning `FA-01 and FA-02 ...` as a second FA-01 definition | Changed the prose to `The FA-01 and FA-02 calculations ...` so the local definition marker is unambiguous. Flow identities and behavior are unchanged. Final specification validator: zero errors/warnings. |
| Unknown Coupon classification was implicit in the first author draft's successful branch wording | Made the common supplied-Coupon lookup/check prefix explicit before either fixed/percentage branch; failure anchors now say supplied-Coupon lookup/configuration/eligibility at step 5. No baseline behavior changed. |
| Coupon was alternative-only and uncolored | Colored it light blue, as a real alternative-only data concept. Return refusal remains light coral. |
| A label combining a basic step and an FA marker caused shared Check Coupon eligibility/PriceQuote to appear alternative-only to a lexical heuristic | Restated shared-edge labels as basic behavior and retained FA coverage on the actual alternative edges and correspondence map. Their shared status is now unambiguous. |
| Domain validator suggests CartLine may specialize Cart | Retained and rejected the heuristic inference: a CartLine is a member of a Cart, not a substitutable Cart. Adding inheritance would corrupt the business model. Stable `Cart -- CartLine : lines` is correct here. |
| Robustness validator reports eight control-to-control connections | Retained with review: the controls are this goal's explicit logical responsibilities (request validation, trusted resolution, totaling, eligibility, calculation, result completion, refusal). Each maps to source behavior and test obligations. This preliminary decomposition does not prescribe a manager class; later allocation must decide actual classes/contracts. |

No source validator or fixture was edited. No business baseline was changed to satisfy a heuristic. No downstream design or PDR was performed by this stage-author agent.

## Independent PDR correction round

- **Semantic F01 (real author defect):** the first glossary asserted nonnegative Coupon minimum and the first FE-07/CA-13 included negative-minimum refusal, although baseline/oracle leave that sign policy outside this bounded example. Removed that restriction and refusal criterion. Minimum still requires integer cents; negative-minimum acceptance/refusal is now explicitly unspecified/excluded. Product-price/fixed-discount constraints and percentage range remain unchanged. Baseline/oracle were not edited.
- **Format compatibility, not missing behavior:** all three FA and seven FE summaries already contained guards, system actions and exits. Their compact table form exceeded the PDR parser's supported behavior extraction. Added the published numbered FA/FE substep tables with the same actions, guards and continuations; no new business path or flow ID was introduced by this formatting change. The common failure postconditions are now repeated in detail rows for local readability.
- Normalized initial specification/glossary illustrations are published under `../review-history/`; the adapted independent PDR record is `../05-pdr/PDR-01.md`. Author rerun of the PDR CLI only verifies the supported mechanical profile and does not replace the independent reviewer's semantic equivalence check.
