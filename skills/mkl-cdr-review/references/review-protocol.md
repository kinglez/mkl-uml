<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Formal CDR protocol

Apply this protocol when a formal technical review is requested. Ordinary scoped work reports the selected checks, evidence and limitations without requiring a meeting or the whole MKL pipeline. The instructions below are independently worded procedures informed by IEEE Std 1028-2008 clause 5; selected inspection concepts from clause 6 are declared adaptations. They are not the standard's text or a claim of compliance certification.

## Scope, inputs and authorization

Record the review objective, the exact artifacts/revisions, the selected use cases, prior findings and the checks to perform. For a full release review, expect sequences for each selected use case and a class model reflecting assigned operations. Confirm that actual required inputs are readable and substantive. A supplied empty file is not evidence.

Missing target material blocks its review. Missing applicable supporting material leaves those checks **Not fully verified** while independent checks continue. Out-of-scope optional evidence is recorded as a scope limit. A partial technical assessment must not become full-package acceptance simply because missing layers were listed.

`SKILL.md` is the authoritative authorization rule: a review-only request produces findings and proposed changes; an authorized review-and-fix request applies supported corrections, rechecks affected artifacts, and records what changed. Organizational assignment and sign-off are recorded separately from execution of already authorized work.

Sources: IEEE 1028 §5.1, §5.3, §5.4.2; Rosenberg & Stephens (2007), chapter 9.

## Participants and actual identities

| Role | Responsibility in this workflow |
|---|---|
| Decision maker | Provides organizational acceptance when that is requested and within their authority. |
| Review leader | Sets the objective, selects checks, coordinates examination and issues the review record. |
| Recorder | Preserves findings, decisions, action status and evidence. |
| Technical reviewers | Supply the relevant architecture, design, integration and implementation expertise. |

Record who actually performed each role. One agent can prepare and record a technical assessment; it must not impersonate absent participants or organizational sign-off. Include customer/product expertise when an unresolved requirement or observable outcome needs it. Implementer evidence is necessary for formal Rule 4; lack of it remains an explicit gap. Meeting and role formality should match the requested review.

Source: IEEE 1028 §5.2. Customer participation is context-dependent, not prohibited by the standard.

## Examination agenda

1. Check evidence availability and compare the target with its selected requirements and interfaces.
2. Apply the ten checks in [cdr-rules.md](cdr-rules.md), recording actual coverage and findings.
3. Check changed areas and their affected links against the prior baseline.
4. Assess whether remaining uncertainties affect implementation, integration, schedule or scope.
5. Identify relevant unresolved decisions and recommend an action with a reason.
6. Complete the record before reporting a formal disposition.

For requested SOLID review or material extension/substitution/client/dependency claims, use [solid-evidence.md](solid-evidence.md) during examination. Scope each claim, challenge its actual evidence and distinguish a supported result, demonstrated finding and unverified layer. Record this coverage separately; no SOLID score or validator result supplies a formal disposition.

The record supports assessment of completeness, applicable constraints, suitability and readiness. Matters outside the technical scope are assigned to organizational follow-up with ownership left explicit. Sources: IEEE 1028 §5.5.6, §5.6–5.7.

## Findings

Each finding needs a verifiable location, supporting requirement/rule, consequence and severity. Keep the category separate from severity. The category names below are retained as technical vocabulary from IEEE 1028 §6.8.2; their operational descriptions are local wording.

| Category | Use when |
|---|---|
| Missing | Required information or behavior is absent. |
| Extra | An element has no justified purpose in the selected scope or contracts. |
| Ambiguous | Multiple materially different interpretations remain. |
| Inconsistent | Artifacts or elements make incompatible statements. |
| Not conforming to standards | A specified applicable rule is demonstrably violated. |
| Risk-prone | A supported design concern exists without proving the design incorrect. |
| Incorrect | Available evidence contradicts the modeled result or relationship. |
| Unachievable | Stated constraints prevent implementation as designed. |
| Editorial | Presentation or wording obstructs use without changing intended behavior. |

Use the package severity scale: **Critical** blocks the selected design; **Major** leaves required behavior or artifact consistency broken; **Moderate** identifies a supported design risk; **Minor** covers bounded wording or presentation defects. Calibrate severity to the actual effect. These design-readiness levels are a local convention; they are not equivalent to the operational hazard examples in IEEE 1028 §6.8.3.

## Evidence first, then disposition

| Proposed formal result | Required basis |
|---|---|
| **Not fully verified** | Any applicable check lacks sufficient evidence, including checks that require actual human participation. Report demonstrated defects independently. |
| **Reinspection required** | Verified blocking defects or unmet entry/quality criteria remain. |
| **Accepted with rework verification** | Applicable checks have evidence; only bounded agreed rework remains, with owner, due date and verification criteria. Acceptance remains conditional until the specified verification is complete. |
| **Accepted** | Applicable evidence is complete, blocking findings are closed, and any required verification is recorded. |

The inspection disposition vocabulary in IEEE 1028 §6.5.6.5 informs this local technical-review scale. Missing evidence is not minor rework and cannot satisfy an acceptance condition.

When independent rework verification is required, record the actual correction author and actual verifier. A rerun by the correcting agent is a **self-check**, even if it invokes another skill. Keep independent verification pending until a distinct reviewer supplies evidence; a skill switch or repeated self-audit is not independence.

## Record content

Keep one review record containing:

- Objective, scope, artifact paths/revisions and available/missing evidence.
- Actual participants and roles, performed checks and their limits.
- Findings with category, consequence, severity and supporting location.
- Action status, actual owner, target/completion date and verification evidence.
- Unresolved technical and management issues, recommended action and rationale.
- Proposed technical disposition and any separate organizational decision.
- Applicable SOLID claims, evidence, actual checks, coverage, outcomes and unresolved actions.
- Measured material size and session assumptions when a formal budget is useful.

This is a local record structure informed by IEEE 1028 §5.7 and the material-size field of §6.7. It does not reproduce those clauses.

## Preparation, follow-up and process learning

Prepare before convening a team review, consolidate evidence in the meeting, apply authorized rework, and verify the affected links. Use [session-budget.md](session-budget.md) for a stated estimate rather than a mandatory duration. Wiegers & Beatty, *Software Requirements* (3rd ed.), chapter 17 informs this sequence; the tool covers part of preparation rather than replacing review judgment.

Review recurring defect patterns and unhelpful checklist items against actual outcomes. Zero findings is valid. Assess examination coverage and seeded negative cases before inferring that a check is ineffective. IEEE 1028 §6.9 motivates process analysis; it supplies neither an expected finding quota nor a repeated self-review requirement.
