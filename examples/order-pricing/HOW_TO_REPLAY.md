# Replay the eight-stage example

Read the [business baseline](00-input/requirements.md) and [independent acceptance expectations](00-input/ACCEPTANCE_ORACLE.md), then send the prompts below to an agent **in chat**. They are not terminal commands. Start from a repository checkout with the skills available; the prompts identify their repository source paths explicitly.

Each prompt uses `examples/order-pricing` as the example root. Paths such as `01-domain/domain.puml` are relative to that root. When adapting this template for a new project, replace the example root consistently and retain the required input relationships. The [source snapshot](SKILL_SOURCE.json) records the validator baseline used by this example.

Preserve valid IDs, material findings and missing evidence. A separate reviewer must actually perform the work before a record calls it independent review. AI technical review supports the local demonstration; formal human/business acceptance needs real participation and decision evidence.

## 1. Conceptual domain model

```text
$mkl-uml-domain-modeler
Follow skills/mkl-uml-domain-modeler/SKILL.md; keep the skill source unchanged.
Example root: examples/order-pricing. All following artifact paths use that root.
Read 00-input/requirements.md and 00-input/ACCEPTANCE_ORACLE.md.
Create the conceptual model for CU-01 Quote cart in 01-domain/domain.puml;
record concept meanings, value constraints and unresolved policy in glossary.md
in the same directory. Separate business concepts from implementation classes.
Preserve existing IDs and the declared business input domain. Run the relevant
validator, render and inspect when a renderer is available, and report actual
checks and limits. Write the explanation in English; edit only example artifacts.
```

## 2. Actors and use cases

```text
$mkl-uml-use-case-diagram
Follow skills/mkl-uml-use-case-diagram/SKILL.md; keep the skill source unchanged.
Example root: examples/order-pricing. All following artifact paths use that root.
Read 00-input/requirements.md, 01-domain/domain.puml and 01-domain/glossary.md.
Create 02-use-cases/use-cases.puml with the Order Pricing boundary, Shopper and
CU-01 Quote cart. Record actor/goal/source mappings in actor-goal-map.md in that
directory. Model externally meaningful goals and genuine participating roles.
Preserve the CU identity, run the relevant checks and inspect the rendered view;
record actual results and semantic judgments in English.
```

## 3. Textual use case specification

```text
$mkl-use-case-specifier
Follow skills/mkl-use-case-specifier/SKILL.md; keep the skill source unchanged.
Example root: examples/order-pricing. All following artifact paths use that root.
Read 00-input/requirements.md, 00-input/ACCEPTANCE_ORACLE.md, the 01-domain
artifacts and 02-use-cases/use-cases.puml. Complete 03-spec/CU01-quote-cart.md
and 03-spec/interface-contract.md. Define basic, alternative and exception
behavior with triggers, system actions and explicit resumption/termination.
Make results observable. Preserve CU/FA/FE/RN/CA identities, trusted-price origin,
read-only behavior and unresolved policy. Run the specification checks and
record format compatibility adjustments separately from meaning changes.
```

## 4. Robustness analysis

```text
$mkl-uml-robustness-diagram
Follow skills/mkl-uml-robustness-diagram/SKILL.md; keep the skill source unchanged.
Example root: examples/order-pricing. All following artifact paths use that root.
Read the 03-spec and 01-domain artifacts and 02-use-cases/use-cases.puml.
Complete 04-robustness/robustness.puml, preserving DR-01. Map text steps,
control responsibilities, data origins and branches in correspondence.md in
that directory. Use a named machine boundary and BCE analysis responsibilities;
allow implementation responsibilities to be allocated later. Run the validator,
inspect the rendering and correspondence, and report uncovered evidence and
reasoned dispositions of tool diagnostics.
```

## 5. PDR preparation and independent review

```text
$mkl-pdr-review
Follow skills/mkl-pdr-review/SKILL.md; keep the skill source unchanged.
Example root: examples/order-pricing. All following artifact paths use that root.
Compare the 01-domain, 02-use-cases, 03-spec and 04-robustness artifacts with
00-input/requirements.md and 00-input/ACCEPTANCE_ORACLE.md. In 05-pdr/PDR-01.md,
record reviewed versions, vocabulary/data/behavior correspondence, actual
mechanical results, located findings and the technical conditions for detailed
design. Correct affected example artifacts and reinspect before advancing when
a finding blocks that transition; retain the initial issue and its resolution.
Identify the real author and reviewer roles. Formal human/business acceptance
remains Not fully verified when that evidence is absent.
After actual review, maintain handoffs/analysis.json with the roles, disposition,
human_approval:false and inputs_sha256 for reviewed relative source paths and
the PDR record. Updating hashes alone is not a replacement for review.
```

## 6. Interactions, operation allocation and test design

```text
$mkl-uml-sequence-diagram
Follow skills/mkl-uml-sequence-diagram/SKILL.md; keep the skill source unchanged.
Example root: examples/order-pricing. All following artifact paths use that root.
FIRST read 05-pdr/PDR-01.md and its reinspection decision. Check findings and
conditions affecting detailed design. Read 00-input requirements/expectations,
the 01-domain and 03-spec artifacts, and 04-robustness/robustness.puml plus
correspondence.md. Resolve blocking analysis issues before detailed design.
Complete 06-interactions/sequence.puml for CU-01; record receiver/operation/source
allocation in operation-delta.md, observable tests in test-plan.md and rationale
in DESIGN_DECISIONS.md, all in 06-interactions. Distinguish calls, replies, signals
and lifecycle behavior. Give branches real actions and valid exits, including
the correct enclosing-fragment scope and lifeline coverage of terminating breaks.
Maintain sequence-scope.json: schema_version 1, with sequences keyed by filename
and containing id, scope, use_cases, requirements and reason. DS-01 has use-case
scope for CU-01. An optional contract-observation.puml is a technical-probe for
RNF-02 and does not claim business branch coverage. Preserve IDs; run applicable
checks and inspect the actual render. Record meaningful limits and findings.
```

The explicit PDR input preserves the analysis decision when stages run in different chats. Test design specifies expected behavior; executed tests supply a separate evidence layer.

## 7. Detailed design class model

```text
$mkl-uml-design-class-model
Follow skills/mkl-uml-design-class-model/SKILL.md; keep the skill source unchanged.
Example root: examples/order-pricing. All following artifact paths use that root.
Read the 00-input requirements, 01-domain and 03-spec artifacts, and all scoped
06-interactions sources, operation-delta.md, test-plan.md and DESIGN_DECISIONS.md.
Complete 07-class-model/classes.puml, provenance.md and SOLID.md. Allocate typed
state and operations through the collaboration; give added technical classes,
ports and strategies an explicit responsibility or constraint origin. Check
association-end multiplicities against actual ownership/sharing semantics.
Assess reasons for change, extension scope, shared behavior contracts, client
capabilities and source dependency ownership. Use concrete evidence beyond
interface notation. Run cross-artifact checks, inspect rendering, and synchronize
affected interactions and provenance when correcting the design.
```

## 8. CDR preparation and independent review

```text
$mkl-cdr-review
Follow skills/mkl-cdr-review/SKILL.md; keep the skill source unchanged.
Example root: examples/order-pricing. All following artifact paths use that root.
Review the 07-class-model artifacts and all 06-interactions sources/decisions/
operation/test documents against 00-input, 01-domain, 03-spec, 04-robustness and
05-pdr/PDR-01.md. In 08-cdr/CDR-01.md record reviewed versions, scenario/branch/
operation/signature/test evidence, findings and dispositions. If the reference
implementation exists, inspect and execute it; keep unexecuted behavior unverified.
Generate 08-cdr/headers.java as a review aid and compare it with the model and
implementation; record the actual inspection in header-inspection.md. Preserve
findings and actual author/reviewer roles. Recheck affected links after corrections.
Give an evidence-backed technical recommendation while retaining Not fully
verified for missing formal human/business acceptance.
After actual review, maintain handoffs/design.json with roles, disposition,
human_approval:false and inputs_sha256 for reviewed source inputs, prior handoff,
CDR and declaration inspection. Exclude the handoff itself and changing run logs
from its own hash list. Refresh the record only after affected-scope review.
```

The [reference implementation](09-reference-implementation/README.md) is additional executable design evidence. Its existence does not replace PDR/CDR correspondence and semantic checks.

## Run verification and replay a change

From the repository root:

```bash
python3 examples/order-pricing/scripts/verify.py
python3 examples/order-pricing/scripts/verify.py --render
```

The second command also requires local PlantUML. The [published record](VALIDATION.json) describes publication checks; a rerun writes current logs under the example's `validation/latest/`. A stale source hash blocks the reviewed handoff. Identify the affected semantics and review them before recording a replacement baseline.

For a controlled change, replace the first line of this prompt with the intended rule and literal expected outcomes:

```text
Replay this change in examples/order-pricing: [state the selected change and
its independently justified expected outcomes]. Fix the before-change baseline.
Map affected RF/RN/RNF, CU/FA/FE, DR, DS, MC and CP identities. Preserve unaffected
IDs and retain retired identities. Record the impact and old review's limits in
CHANGE_IMPACT.md. Update affected requirements, models, interactions, members and
tests; recheck their semantic links and applicable validators. Obtain expected
values independently of the implementation. After genuine affected-scope review,
update the relevant handoff record, run scripts/verify.py, and report actual
results, unresolved scope and missing formal acceptance evidence.
```

Validators check supported syntax/profiles and selected heuristics; rendering checks a different layer. Neither supplies exhaustive business verification, OMG certification or universal SOLID proof. See [the workflow assessment](WORKFLOW_REVIEW.md) and the [actual change exercise](CHANGE_IMPACT.md).
