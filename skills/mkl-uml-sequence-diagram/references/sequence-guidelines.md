<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sequence-design workflow

This original workflow adapts Rosenberg & Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice* (2007), chapter 8, and the model/test design discussions in Rosenberg, Stephens & Collins-Cope (2005). The historical countdown is retained for cross-reference, with independent operational wording.

| Guideline | Action |
|---|---|
| **10 — Choose a design question** | Use the interaction to decide and explain responsibility allocation among collaborating objects. |
| **9 — Cover the selected use case** | Include its basic and specified alternative/exception behavior together, or link explicitly scoped supporting interactions. |
| **8 — Start from available evidence** | Use supplied actors, interfaces, domain concepts and scenario text; in MKL workflow mode, inspect the PDR handoff before relying on the reviewed analysis. Record missing origins without inventing predecessor artifacts. |
| **7 — Realize required behavior** | Treat supplied robustness Controllers as a behavior worklist and show which collaborators perform each responsibility. |
| **6 — Reconcile text and interaction** | Trace actor actions and system responses to messages and observable outcomes, then inspect significant messages for an origin. |
| **5 — Use activations purposefully** | Omit them by default under this style profile; include requested activations and verify each execution path. Presence alone is not a UML error. |
| **4 — Allocate as you draw** | Classify each message and assign Operation calls to the receiving classifier. Replies, Signals and lifecycle messages require their own provenance. |
| **3 — Maintain the static model** | Update significant operations, necessary state and collaboration relationships while making allocation decisions. |
| **2 — Compare alternatives before coding** | Refine responsibility distribution while preserving required behavior and recording meaningful decisions. |
| **1 — Reconcile before CDR** | Resolve known interaction/class inconsistencies and report outstanding evidence before formal readiness assessment. |

## Construct the interaction

1. Identify the selected scenario steps and required observable results.
2. Establish participants and their roles from domain/interface/architecture evidence.
3. Allocate each required behavior to collaborators, preserving traceable names and local flow IDs.
4. Reconcile operations/state with the design class model and derive tests for required outcomes.

Participants and annotations can be scaffolded mechanically; responsibility allocation requires judgment. See [behavior-allocation.md](behavior-allocation.md) and [test-derivation.md](test-derivation.md).

## Consume the PDR handoff

Apply this check when continuing a full MKL workflow or relying on a preliminary-review recommendation:

1. Read the actual PDR record and select the CU/DR/flow scope it examined. Match its source versions to the current specification, robustness and domain evidence. Use the project's available revision or snapshot references; hashes are optional.
2. Inspect the finding ledger, including open/deferred actions, affected behavior and closure evidence. Recheck changed or unresolved analysis before treating the affected design input as settled. Preserve finding IDs and earlier evidence; a new chat or a clean validator run does not close a finding.
3. Record the PDR basis in the design rationale: record/version, scope used, verified corrections, carried constraints and missing evidence. Continue unaffected work within the requested scope and existing authorization. If an indispensable handoff input is absent, report the dependent transition as unverified or blocked rather than inventing approval.

A scoped technical recommendation and a formal gate decision are separate. A teaching exercise can have a justified technical basis to continue while formal human/business acceptance remains **Not fully verified**. A formal transition still needs its applicable decision evidence. Standalone sequence work does not acquire a PDR prerequisite merely because this handoff procedure exists.

## Transform robustness behavior

A robustness Controller denotes logical behavior, not automatically a software class or one method. It may map to multiple collaborating calls, to existing object behavior or to a justified coordinator. The historical approximate 80% allocation statement is practitioner context, not a required distribution; no fixed remaining percentage needs controller classes.

Introduce a service, adapter or coordinator when its technical responsibility is justified. Repeated controller/service names for every entity do not prove good allocation. Check the actual state, invariants and dependency contracts.

## Keep problem and solution evidence distinct

A new technical collaborator is a legitimate detailed-design result when marked and justified. A new problem-domain concept requires domain reconciliation. Record operation/state/relationship origins and significant assumptions in the design delta rather than silently adding them to business use cases.

## Check the right semantics

Use [notation-rules.md](notation-rules.md) as the authoritative message-sort reference. A classified Operation call supports a receiving-class operation; a reply returns outputs to the original synchronous caller; asynchronous completion uses a separate callback call or Signal. Lifecycle messages trace creation/destruction. Unresolved sorts, signatures and receivers remain gaps.

The method requires selected-scope provenance and coverage. It does not assert that every classifier operation must appear in one interaction or that lexical matching proves realization. Class-model asymmetry, centralized work or many self-calls are investigation clues, not sufficient proof of incorrect design.
