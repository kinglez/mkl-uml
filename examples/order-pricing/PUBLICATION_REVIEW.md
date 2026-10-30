# English publication review

> The original 1.0.2 publication review is retained below. Current runtime and workflow maintenance is recorded in the final integration note and VALIDATION.json.

Review date: **2026-10-30**. Reviewer role: independent publication reviewer (AI), separate from the English-documentation and repository-adaptation authors.

**Technical disposition: Ready for repository publication as a bounded teaching example.** The one located publication defect was corrected and rechecked. No unresolved material publication finding remains. Formal human/customer/business acceptance remains **Not fully verified**.

## Scope and preservation checks

This review examined the English example, its verification/reader helpers, the root README entry, the generic stage-6 PDR handoff prompt and the example's CI configuration. It compared the publication with the completed local reference example; it did not repeat or relabel that earlier PDR/CDR as a new human review.

| Check | Actual result |
|---|---|
| Business baseline, independent oracle and pricing core | The eight files identified in [ORIGIN.json](ORIGIN.json) match the original bytes and recorded SHA-256 values. Requirements, expected monetary results and core behavior were preserved. |
| Entry-point and test changes | Direct comparison confirmed that the three recorded changes are explicit UTF-8 text I/O only. They do not change the pricing algorithm, test expectations or case selection. |
| Maintained UML models | All six PlantUML bodies match the original maintained models after comment lines are excluded. IDs, guards, associations, operations and completion behavior were preserved. |
| English and portable references | Scanned the maintained publication text and normalized history: no Chinese prose, machine-specific home paths or internal session/agent identifiers remained. Local Markdown targets resolve; the generated publication summary is [VALIDATION.json](VALIDATION.json). |
| Historical evidence boundaries | PDR/CDR records explicitly describe publication adaptations. They retain actual findings and technical conclusions without claiming the original byte hashes, signatures or formal human acceptance. Historical illustrations are marked superseded. |
| Documentation and workflow | The guide has runnable repository commands, eight-stage artifacts and rendered previews. Replay stage 6 explicitly reads PDR. The corrected break/multiplicity findings, retired DS-01-M10 and undefined negative-minimum policy remain visible. |
| Verification portability | Repository location is inferred from the script; execution does not depend on the caller's working directory. Text hashes and header comparison normalize checkout line endings. Child Python processes explicitly use UTF-8. Rendering is optional and requires local PlantUML only when requested. |
| GitHub and installation boundaries | The [root README](../../README.md#complete-worked-example-order-pricing) links to the reference example. Markdown and PNG previews are GitHub-readable; the HTML reader is identified as a local/offline artifact. Skill installation is not presented as copying the example project. |
| CI | The [workflow](../../.github/workflows/validate-skills.yml) includes example changes in its triggers and adds verifier jobs for Ubuntu and Windows. Configuration inspection does not claim those remote jobs have already completed. |

## Actual execution

The publication reviewer copied the current edition into a temporary directory whose path contained spaces and Unicode, then executed it from an unrelated working directory with `--skill-root` pointing to the repository. This isolated the review's execution outputs from the coordinator's render run.

| Execution and owner | Observed result |
|---|---|
| Independent reviewer: current `scripts/verify.py`, default mode | **Exit 0; all 13 checks passed.** The reference suite passed 15 unittest methods, including 30 independent oracle subcases. The tested verifier SHA-256 was `6bc16e0d6c31f871512f298d443eb10709d6537c8458e65eecf9147917ac424b`. |
| Independent reviewer: changed-requirement probe after that PASS | **Exit 2 / BLOCKED.** Changing the copied requirement made the analysis baseline stale before downstream checks. The result replaced the previous PASS rather than retaining a misleading success. |
| Independent reviewer: retained code probes | **Exit 0.** Minimal Product/Coupon/resolver substitutes worked; request data could not replace the trusted catalog; state was preserved; no write/socket audit event was observed in the selected quote calls. |
| Coordinator: current verifier with `--render` | **Exit 0; all 16 checks passed**, including source/header checks, reference tests and regeneration of all six SVG/PNG diagrams. |
| Coordinator: complete-checkout CRLF probe | **Exit 0; all 13 default checks passed**, with 15 test methods, after conversion of 466 text files to CRLF in an isolated checkout containing spaces and Unicode and execution from an unrelated directory. This is line-ending/path evidence, not an actual Windows OS run. |
| Coordinator: existing repository regression suite | The actual output reported **206 tests, OK**. This includes standalone distribution/link behavior; the example remains repository material rather than being added to every installed skill payload. |

The [published validation summary](VALIDATION.json) records the coordinator's publication executions and applicable environment limits. Local reruns generate fresh logs under `validation/latest/`; omitted historical machine logs are not reconstructed as original evidence.

## Located finding

**PUB-01 — broken historical interface-contract link, Minor: Closed.** The normalized `review-history/pdr-initial-specification.md` originally linked to `interface-contract.md` in its own directory, where that file did not exist. The repository adaptation corrected it to `../03-spec/interface-contract.md`. The reviewer rechecked the target and the complete local Markdown-link scan. The publication source checksum was refreshed after that editorial correction.

This conclusion supports publication of the reviewed English reference example. Finite execution and model-preservation checks do not provide universal SOLID/UML conformance, production readiness or missing formal business approval.

## Maintainer integration note — 1.0.3

The validator snapshot now identifies source commit `24170e513586012a22c55d76b38544d8e3e61abb`. Requirements, independent expected results, pricing core and six UML model bodies are unchanged. The maintained example adds the reusable PDR handoff and an explicit scoped SOLID evidence record; its reader obtains the validator version from SKILL_SOURCE.json. Publication checksums are updated only after examining those changes, not presented as a replacement for review.

Separate independent AI reviews consumed the updated handoff/SOLID instructions in four scenarios and examined the PDR/CDR parser changes. Two additional reference/placeholder false greens were reproduced through the CLI, corrected and independently rechecked. All 240 repository tests passed, including 31 new PDR and 3 CDR regressions; all eight metadata checks, archive generation and plugin validation passed. The current example execution is recorded in VALIDATION.json. These are maintenance evidence, not a new signature on the original publication record or missing human/business acceptance.

## Documentation maintenance — 2026-10-30

The project README, documentation guide and introductory tutorial now use this order-pricing example throughout. This example's README presents the scenario, execution, expected amounts and stage artifacts before optional evidence/history. HOW_TO_REPLAY.md retains its advanced maintained-baseline procedure and points first-time users to the tutorial, which writes separate working outputs under `uml/order-pricing/`.

An independent AI editorial reviewer compared the guides with the unchanged requirements, specification and executable example. The review checked the no-Coupon, fixed/percentage, zero-subtotal and refusal behavior, source/output paths, earlier-stage inputs, retained tutorial anchors, installation boundaries and review-evidence claims. No unresolved concrete documentation finding remained. The actual example run produced the six documented JSON results. All eight standalone payloads included the new documentation navigation and retained valid local links.

Only the changed reader-facing guides and this maintenance note receive refreshed entries in `handoffs/design.json`, after that affected-scope review. Requirements, independent oracle, models, pricing code, validator runtime and historical review conclusions are unchanged. This editorial review does not repeat the original semantic PDR/CDR or supply formal human/business acceptance. Fresh local aggregate results are written to `validation/latest/`; the earlier VALIDATION.json remains the historical publication execution record.
