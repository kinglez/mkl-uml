<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CDR review candidates

Use these independently worded checks to locate evidence, then establish the actual defect before proposing a correction. They adapt concerns from Rosenberg & Stephens (2007), chapter 9; course Session 09; IEEE Std 1028-2008 §6.8.2; and the review-process sources in [sources-and-methods.md](sources-and-methods.md). A structural warning is a candidate, not proof of poor design.

| # | Candidate and consequence | Review/correction |
|---|---|---|
| 1 | Scenario and interaction disagree, leaving required behavior or output unexplained. | Trace steps and significant messages both ways; fix the artifact whose evidence is incomplete. Lexical matching is partial. |
| 2 | A specified alternative/exception has no implementing behavior. | Check the branch within its own CU, including trigger and outcome. Labels or mentions alone do not implement it. |
| 3 | An operation's demonstrated call receiver differs from its owning class. | Confirm message sort, signature, receiver and responsibility; correct the proven mismatch. Asymmetric APIs alone prove nothing. |
| 4 | A significant operation lacks an origin within the selected scope. | Check other scenarios, interface/framework contracts and design deltas before reporting it unsupported. |
| 5 | A requirement has no realization, or a design element has no justified origin. | Report the two directions separately; architecture/configuration can realize nonfunctional obligations. |
| 6 | Domain state and state-dependent behavior are separated without a clear contract reason. | Review the architectural style and responsibility allocation before calling the model anemic. |
| 7 | Unrelated responsibilities accumulate in one class. | Inspect the required knowledge and change reasons; split only when that improves the demonstrated design. Cohesion needs judgment. |
| 8 | A modeled class has state but no visible behavior. | Check whether it is a value object, contract/data carrier or an omitted allocation. |
| 9 | An Entity has no modeled state. | Inspect actual domain data and scope before adding fields or reporting an incomplete entity. |
| 10 | A wrapper repeats a contained object's state and delegates all behavior. | Inspect framework, security and boundary contracts. Remove only if its distinct purpose is unsupported. |
| 11 | A lifeline has no incoming or outgoing interaction. | Determine whether its messages are missing or the participant is unnecessary in this scenario. |
| 12 | One class is much larger or more connected than its peers. | Inspect responsibility distribution; numeric warning thresholds are local heuristics. |
| 13 | A significant effect occurs without any modeled collaboration or declared contract. | Add the supported interaction or record the unresolved design gap. |
| 14 | Infrastructure is mixed with domain concepts without a technical origin. | Mark the solution role and record the actual architecture/contract rationale. A stereotype alone is insufficient. |
| 15 | Parameter/result types leave a material contract undecided. | Resolve each parameter and result from evidence; a generic type can be legitimate if its contract is deliberate. |
| 16 | Generic operation names conceal their responsibility. | Name the actual action or clarify the contract. Naming alone is normally editorial. |
| 17 | An association lacks multiplicity needed for validation or faithful header interpretation. | Obtain evidence or mark the uncertainty. CDR may need detail legitimately deferred by conceptual modeling. |
| 18 | Presentation work consumes attention while known content gaps remain. | Resolve supported findings before polishing layout. |
| 19 | Planned volume exceeds what the recorded examination actually covered. | Record the uncovered material and split work using actual complexity/capacity. Size alone does not prove a failed review. |
| 20 | A review result lacks demonstrated examination coverage. | Check the coverage record and effective negative regressions. **Zero findings is valid**, including for large mature packages; historical defect density cannot invalidate it. |
| 21 | Repeated unchanged review provides no new evidence. | Identify the concrete defect, missing input or scope problem; change the review question or reviewer when useful. No fixed cycle count proves correctness. |

## Severity and automation

Use categories to distinguish missing/extra/inconsistent information from supported design risks. Keep category separate from consequence-based severity. Scripts can check names, counts and supported structural correspondences; responsibility, feasibility and semantic realization still need judgment. See [cdr-rules.md](cdr-rules.md) for evidence requirements and [review-protocol.md](review-protocol.md) for formal disposition.

Accessor exemptions cover conventional `getX`, `setX`, `isX` and `hasX` names. Ordinary business verbs such as `issue` or `settle` still need provenance. ALL CAPS conventions may require explicit review because broad case-insensitive matching can exempt unrelated verbs. The current implementation and tests define the precise accepted spelling.
