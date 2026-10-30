<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Scoped SOLID evidence review

Use this procedure when the user requests a SOLID assessment or when an in-scope extensibility, substitution, client-contract or dependency claim needs examination. It supplements the [CDR checks](cdr-rules.md); it does not add a universal gate to every class diagram or define extra UML conformance rules.

## Scope the claim before checking it

Name the affected use case, classifiers/contracts, relevant requirement or design decision, and the proposed change or replacement. Fix the artifact revisions. If a full SOLID assessment is requested, account for all five principles; otherwise select those relevant to the actual claim and explain the scope.

Use model evidence for modeled intent, source evidence for actual dependencies, and executed evidence for observed behavior. A supplied test plan is not a test execution. Class counts, interface arrows, pattern names, keyword matches and a successful validator do not establish the claims below. Required code or contract evidence that is unavailable remains a gap; calling it out of scope does not verify that claim.

## Examine the five principles

| Principle | Evidence to inspect | Concrete challenge |
|---|---|---|
| **S — Single responsibility** | Responsibility and state ownership, the stakeholder/policy that can change them, and collaborator roles. | Trace two plausible changes, such as a pricing rule and catalog representation. Identify which elements each must change and whether unrelated decisions are coupled. A value object or cohesive coordinator can be valid; one method per class is not the criterion. |
| **O — Open/closed** | The specific variation to protect, its stable contract, current clients, and permitted integration changes. | Add or reason through one justified variant. Inspect the required source/model changes and retained behavior. Distinguish new implementation and registration/wiring from edits to the protected workflow. State what is outside this extension axis. Runtime hashes alone do not establish a historical no-edit change. |
| **L — Liskov substitution** | Common accepted input domain, pre/postconditions, result and state invariants, error semantics and observable effects for each replacement. | Apply the same contract cases to each implementation, including domain edges and relevant failures. Check strengthened preconditions, weakened guarantees, extra effects and history/state constraints. Record literal expected results and actual execution. Finite cases support the sampled contract; implementation arrows or a test name do not prove universal substitution. |
| **I — Interface segregation** | The capabilities each actual client uses and the contracts it must depend on. | Inspect client calls/types and replace a collaborator with a minimal implementation of only its required capabilities. Confirm that unrelated setup, mutation or administrative operations are unnecessary. One adapter may implement several small contracts; splitting every class into interfaces is not the objective. |
| **D — Dependency inversion** | The high-level policy, contract owner, concrete adapters, source imports/references and composition/wiring location. | Follow source dependencies and substitute an adapter without changing the protected policy. A runtime call to an injected collaborator does not by itself establish contract ownership or import direction. With models but no source, report the modeled dependency intent and keep source-level claims unverified. |

Separate configuration/eligibility rules from the calculation contract when those are different responsibilities. For example, a workflow can refuse a Coupon below its threshold while every configured calculation policy still accepts every nonnegative subtotal. Otherwise a workflow precondition may accidentally be used to excuse a substitution defect.

When implementation or execution is outside the selected scope, inspect the available design and specify the missing probe. Distinguish a planned check from an executed result.

## Record coverage and outcome separately

Use the existing review/finding IDs and keep one concise record with the CDR or requested assessment. A separate file is useful only when the user or project needs it. The following fields are a reusable format, not a required machine schema:

```text
Scope and revision: CU / classifiers / contracts / requirement or decision
Principle and claim: the responsibility, change, replacement, client or dependency
Evidence: exact model/member, source, contract, test and reviewed revision
Challenge and result: inspected change or executed command/case; expected vs observed
Coverage: checked | partial | blocked | not applicable, with a reason
Outcome: supported in the reviewed scope | finding | unverified
Limits and action: unsampled domain, missing evidence, finding ID, affected artifact
```

- **Checked** means the declared examination was completed against sufficient evidence for that bounded claim. It can produce a **finding**; it is not a synonym for passing.
- **Partial** means an applicable layer or portion is missing, such as source imports or execution. Preserve any demonstrated finding and identify the unverified remainder.
- **Blocked** means the target or indispensable contract for the requested assessment is unavailable. Continue unrelated checks.
- **Not applicable** needs a reason tied to the chosen scope or design obligation. It cannot replace missing evidence for an asserted property.

For a finding, identify the conflicting contract/location and practical consequence, then use the normal CDR severity and correction protocol. For an unverified claim, name the evidence or test needed; missing execution alone does not demonstrate a violated principle. For support, state the actual scope and evidence limits. Do not aggregate these results into a SOLID score, percentage, certificate or automatic formal acceptance.

## Review examples

These examples specify how to judge evidence; they are not claims that a test was executed for the user's project.

| Supplied evidence | Appropriate assessment |
|---|---|
| A class diagram shows three implementations of a policy interface, with no common contract or behavior evidence. | Record the modeled implementation relationships. L's behavioral comparison is **blocked / unverified** until its indispensable contract is known; continue the separate UML/model checks and name the missing replacement evidence. |
| The common policy contract accepts nonnegative CNY subtotals. An executed shared case shows a fixed-3000 policy refusing subtotal 333, although its contract requires capping the discount. | L is **checked / finding** for that counterexample: the replacement strengthens the precondition. Record expected discount 333, actual refusal, the implementation and test evidence. Other inputs remain outside this finite result. |
| A new policy and registration produce the specified result; inspection shows no new case in the protected coordinator. | O is **supported in the reviewed extension scope** when the change evidence establishes that boundary. This does not verify unrelated variation axes, L or the other principles. |
| No source code is supplied, but model dependencies and contract ownership are explicit. | Assess the model's dependency design. D's source-import and runtime replacement layers remain **partial**, rather than inferred from the diagram. |

The repository's [order-pricing SOLID record](https://github.com/kinglez/mkl-uml/blob/main/examples/order-pricing/07-class-model/SOLID.md) and [shared contract tests](https://github.com/kinglez/mkl-uml/blob/main/examples/order-pricing/09-reference-implementation/tests/test_pricing.py) provide a concrete, bounded worked example. They are optional reading, not runtime dependencies of an installed standalone skill; the review format above is self-contained.

## Handoff and reinspection

During detailed design, collect the declared responsibility/change axes, replacement contracts, client capabilities and dependency ownership alongside normal member provenance. At CDR, inspect those claims against the actual evidence and retain unresolved actions. After a correction, repeat the affected challenge and check its links to requirements, interactions, classes and tests.

Keep this scoped SOLID outcome separate from the mechanical validator result, general CDR coverage and formal disposition. Strong bounded design evidence does not supply absent human participation or organizational acceptance; a green CLI does not fill an unverified SOLID layer.
