<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Resolving design-review decisions

Use this reference when a finding leaves a real scope, business or risk decision unresolved. Report completed technical findings immediately and carry out supported, already authorized corrections. The authoritative editing rule is in `SKILL.md`; an optional formal decision discussion does not revoke it.

## Make the decision concrete

Group related findings by affected artifact or responsible team and order them by consequence. For each group, provide the observed condition, verifiable location, applicable rule, impact and recommended action. State whether the concern is a demonstrated error or a design risk.

A useful decision record identifies the issue, feasible alternatives, evaluation criteria, preferred option, actual decision/authorization, rationale and assumptions. This locally worded workflow is informed by IEEE Std 1028-2008 §5.1, §5.2.1, §5.5.6–5.7 and ISO/IEC/IEEE 12207:2017 §6.3.3.

## Select relevant actions

| Action | Appropriate case | Evidence to retain |
|---|---|---|
| Correct in scope | A supported correction is authorized and its intended behavior is clear. | Changed artifacts, affected links and verification result. |
| Revisit an upstream artifact | The inconsistency originates in requirements, vocabulary or an interaction. | The originating gap and why a local patch would conceal it. |
| Defer with accepted risk | A bounded concern can proceed under an authorized risk decision. | Consequences, decision owner, mitigation and review date. Missing acceptance evidence and blocking defects remain visible. |
| Dismiss a candidate | Additional context demonstrates that the candidate is not a defect. | The evidence and reason for dismissal. |

These are examples, not a fixed menu. Ask for a decision only when its answer changes work beyond existing authorization. ISO/IEC/IEEE 90003:2018 §8.3.4.1 informs the practice of understanding and agreeing the consequences of proceeding with known deficiencies; it does not authorize risk acceptance on the user's behalf.

## Headers and verification

Generate headers when requested or already included in scope. Inspect unresolved signatures and translation limits; headers are review aids, not production implementation. Use the actual volume and a stated estimate if inspection effort matters.

Report author and verifier identities. Self-checks support correction quality; they cannot fulfill a requirement for an independent reviewer. Organizational acceptance remains distinct from the technical assessment.

## Close the record

Record the recommendation, actual decision, rationale, assumptions, assigned actions and open questions. A review-only request ends with review findings and proposed work. A review-and-fix request includes completed supported changes and their recheck. Remaining schedule, resource or scope decisions belong in the management issues portion of the formal record.

Avoid repeating unchanged reviews to reach a quota or weakening a disposition because the session is long. If a review is no longer productive, identify the concrete missing information, unresolved defect or scope boundary. Wiegers & Beatty, *Software Requirements* (3rd ed.), chapter 17 informs preparation and reviewer-fatigue considerations; no fixed repetition count establishes correctness.
