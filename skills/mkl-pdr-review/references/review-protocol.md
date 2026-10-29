<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Conducting a preliminary-design review

Use the full procedure for a requested formal package review. For an ordinary scoped check, use the available relevant artifacts, report findings and scope limits, and continue independent checks. This is original operational wording informed by IEEE Std 1028-2008 clauses 5–6 and Wiegers & Beatty, *Software Requirements* (3rd ed.), chapter 17. The selected procedure is an MKL adaptation, not a claim that every PDR is a standards-conforming inspection.

## Prepare

Record objectives, scope, artifact versions, applicable criteria, prior findings and current evidence. Run applicable validators and examine their findings before a team meeting. Confirm required inputs contain usable evidence. An unavailable target blocks that target; missing applicable support leaves the affected layer unverified. Prior approval by every upstream skill is not a prerequisite for a standalone check.

Use [pdr-guidelines.md](pdr-guidelines.md) to examine the material and [pdr-metrics.md](pdr-metrics.md) for formal measurements. A metric's lexical result does not replace the semantic highlighter review.

## Assign real roles

| Role | Practical responsibility |
|---|---|
| Author | Explains the design and supplies context. |
| Leader/moderator | Defines scope, organizes examination and follows unresolved issues. |
| Reader | Restates behavior and model meaning so ambiguity can be discussed. |
| Recorder | Preserves evidence, findings, decisions and action status. |
| Reviewers | Assess technical and relevant business/product concerns. |

Identify actual people or agents and any combined roles. A formal requirement for independent rework verification needs a distinct verifier; switching skill names does not satisfy it. Record absent product/customer interpretation or other applicable human checks as missing evidence.

Keep participation suited to the decision. Protect a technical review's purpose from personnel evaluation. Team size and meeting duration are project planning decisions; no fixed headcount creates sufficient coverage.

## Examine and decide

Prepare individually, consolidate findings, resolve supported factual questions and record unresolved decisions. Classify demonstrated errors separately from design-risk candidates. Follow the user's authorized scope: report proposed corrections for review-only work, or apply and verify supported corrections when review-and-fix is authorized.

For formal disposition, assess evidence coverage before findings and metrics. Missing applicable evidence, including unperformed human checks, yields **Not fully verified**. Verified blocking defects require reinspection. Conditional acceptance with rework is available only after applicable checks have evidence and the remaining rework is bounded, agreed and assigned. Full acceptance requires completed applicable checks and closed blocking findings.

## Record and follow up

The record identifies the objective, exact material, actual reviewers, performed/missing checks, findings with locations and consequences, recommended actions, actual decisions and rationale. Add action ownership, due/completion dates and verification evidence. Separate the technical recommendation from organizational acceptance where applicable.

Use observed volume and a stated project rate for scheduling. The upstream IEEE 1028 §6.5.2 notes cite **3–4 pages/hour** for preliminary design; this is inherited planning guidance rather than a mandatory pace or a newly verified source transcription. The inherited source-code row has a page/line unit inconsistency and is not a usable header estimate. Wiegers' requirements-review discussion informs preparation and fatigue considerations, not a measured design-review guarantee.

A clean review is valid. Evaluate examination coverage and effective negative regressions, rather than expecting a finding quota or repeating unchanged reviews. If a repeated review stalls, identify the concrete missing information, defect or scope problem.

## Source boundaries

IEEE 1028 supplies review-process concepts; IEEE Std 1016-2009 §3.2.3 and §4.4 supply design-description verification, completeness and consistency context. ISO/IEC/IEEE 29148:2018 supplies requirements-quality context. Historical primary/secondary status is retained in [sources-and-methods.md](sources-and-methods.md). These references do not reproduce the standards or establish independent certification.
