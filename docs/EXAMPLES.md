<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Usage examples

Install the skills, then open your target project in Codex or Claude Code. Send these prompts in the agent chat. They are **not terminal commands**. Codex uses `$skill-name`; Claude Code uses `/skill-name`. For example, replace `$mkl-uml-domain-modeler` with `/mkl-uml-domain-modeler` and keep the rest of that prompt.

The prompts below use one technical support desk scenario. Output paths under `uml/` are example paths the prompts ask the agent to create, not files already created in your project. Run each relevant step after its inputs exist. You can also paste or attach your own requirements and diagrams instead of using these paths. Skill installation does not run the examples.

For a completed reference with all eight stages, rendered diagrams, PDR/CDR correction records and executable tests, read the [order-pricing example](../examples/order-pricing/README.md) and its [replay prompts](../examples/order-pricing/HOW_TO_REPLAY.md). The complete example is also [available on GitHub](https://github.com/kinglez/mkl-uml/tree/main/examples/order-pricing).

## 1. Domain model

Start with business behavior; no existing diagrams are required.

```text
$mkl-uml-domain-modeler
Create a conceptual PlantUML domain model for a technical support desk.
Requirements:
- RF-01: A Requester registers an Incident with a Category and description.
- RF-02: The due date is calculated from that Category's current ServiceAgreement.
- RF-03: A requester not authorized for the category must be rejected.
- RNF-01: Deadline policy can change independently of the Incident.
An Incident has a description, registration date, due date and business reference.
Save these requirements to uml/requirements.md and the model to uml/domain.puml.
Explain assumptions and unresolved multiplicities. Keep implementation classes
out of this conceptual view.
```

Expected: requirements and a domain model with `Requester`, `Incident`, `Category` and `ServiceAgreement`. The independent deadline policy requirement becomes an input to later design; it does not automatically make a policy class a domain entity.

## 2. Use case diagram

```text
$mkl-uml-use-case-diagram
Read uml/requirements.md and uml/domain.puml. Model the "Incident service"
system boundary and its Requester actor. Use CU-07 for "Register incident".
Save the PlantUML diagram to uml/use-cases.puml. Keep authorization and due-date
calculation within the registration behavior unless the requirements justify
separate user goals. Explain any proposed additional actors or goals.
```

Expected: a system boundary, the Requester actor and the registration goal. Internal processing steps are not automatically separate use cases.

## 3. Use case specification

```text
$mkl-use-case-specifier
Read uml/requirements.md, uml/domain.puml and uml/use-cases.puml.
Specify CU-07 Register incident in uml/register-incident.md.
The requester is already authenticated. The system checks the category,
checks authorization, obtains the current agreement, calculates the due date,
registers the incident and returns its identifier and due date.
Include a basic flow, FA-01 unauthorized requester, FA-02 unknown category,
preconditions, postconditions and acceptance criteria. Both rejection paths
terminate without creating an incident. Preserve CU-07 and map RF-01 to RF-03.
```

Expected: actor/system behavior with explicit success and rejection outcomes, suitable for analysis and test derivation.

## 4. Robustness analysis

```text
$mkl-uml-robustness-diagram
Analyze CU-07 from uml/register-incident.md using uml/domain.puml.
Create DR-07 in uml/robustness.puml with boundary/control/entity notation.
Cover the basic flow, FA-01 and FA-02. Distinguish the Incident Form boundary,
analysis responsibilities and domain entities. Explain any missing domain
concepts before introducing them.
```

Expected: the interaction boundary, control responsibilities and grounded domain entities, with both rejection flows represented.

## 5. PDR preparation

```text
$mkl-pdr-review
Review uml/requirements.md, uml/domain.puml, uml/use-cases.puml,
uml/register-incident.md and uml/robustness.puml as scoped PDR preparation.
Check vocabulary closure, BCE relationships and basic/alternative-flow coverage.
Save located findings, coverage limits and proposed corrections to uml/pdr-review.md.
Distinguish automated checks from semantic inspection and human acceptance.
```

Expected: actionable findings and coverage, not an automatic formal approval. Resolve findings that affect detailed design before continuing. For a formal MKL PDR, request that scope explicitly and provide the applicable review evidence and decision makers.

## 6. Sequence diagram and tests

```text
$mkl-uml-sequence-diagram
Read uml/pdr-review.md first and resolve any findings that block detailed design.
Read uml/register-incident.md, uml/robustness.puml, uml/domain.puml and
uml/requirements.md. Create DS-07 in uml/sequence.puml for CU-07.
Include the authorized flow, FA-01 and FA-02, with explicit guards.
Distinguish operation calls, replies and any lifecycle messages.
Document a DeadlinePolicy design responsibility justified by RNF-01.
Save the receiver-operation mappings to uml/operation-delta.md and derive
success/rejection tests in uml/test-plan.md. Preserve the existing CU/DR/FA IDs.
```

Expected: the interaction, a traceable operation delta, and tests with meaningful conditions and outcomes. Replies and object creation do not automatically create ordinary class operations.

## 7. Design class model

```text
$mkl-uml-design-class-model
Read uml/domain.puml, uml/sequence.puml, uml/operation-delta.md,
uml/register-incident.md and uml/requirements.md.
Create MC-07 in uml/classes.puml with types, visibility and complete signatures.
Trace operations to calls or explicit contracts. Distinguish DeadlinePolicy as
a solution design class. Explain relationships and any new design decisions.
```

Expected: a design view with justified operations and solution classes, distinct from the earlier conceptual domain model.

## 8. CDR preparation

```text
$mkl-cdr-review
Review uml/classes.puml and uml/sequence.puml against uml/domain.puml,
uml/robustness.puml, uml/register-incident.md, uml/requirements.md and
uml/test-plan.md. Perform scoped CDR preparation.
Save findings and coverage to uml/cdr-review.md. Check operation provenance,
flow coverage, signature consistency and meaningful test coverage.
Identify unresolved design decisions and missing human review evidence.
```

Expected: a detailed-design consistency review and remaining actions. A formal CDR disposition requires its applicable evidence and designated decision maker; passing a script does not establish acceptance.

## Review or change an existing diagram

Provide the existing file and the evidence relevant to your request. You can invoke a single skill without generating the preceding pipeline stages:

```text
$mkl-uml-sequence-diagram
Review uml/sequence.puml for message-sort mistakes, missing branches and
activation imbalance. Compare it with uml/register-incident.md if available.
Report each finding with its location and impact. Apply corrections to the
diagram, preserve CU/DS/FA/CP IDs, and report the checks actually run.
```

Here the paths refer to your existing project files; replace them or attach the corresponding files. Missing comparison sources limit verification coverage. To request Chinese explanations, append `Explain the result in Chinese; keep code identifiers unchanged.`

## Complete worked artifacts

The repository already contains a coherent support-desk fixture set. Open the files below to inspect actual inputs and outputs; these links do not require you to generate anything first. The filenames retain compatibility with the existing tests; their contents are English.

| Artifact | Existing example |
|---|---|
| Requirements | [requisitos.md](https://github.com/kinglez/mkl-uml/blob/main/tests/fixtures/pipeline/requisitos.md) |
| Conceptual domain model | [dominio.puml](https://github.com/kinglez/mkl-uml/blob/main/tests/fixtures/pipeline/dominio.puml) |
| Actors and use cases | [casos_uso.puml](https://github.com/kinglez/mkl-uml/blob/main/tests/fixtures/pipeline/casos_uso.puml) |
| CU-07 specification | [especificacion.md](https://github.com/kinglez/mkl-uml/blob/main/tests/fixtures/pipeline/especificacion.md) |
| DR-07 robustness analysis | [robustez.puml](https://github.com/kinglez/mkl-uml/blob/main/tests/fixtures/pipeline/robustez.puml) |
| DS-07 sequence | [secuencia.puml](https://github.com/kinglez/mkl-uml/blob/main/tests/fixtures/pipeline/secuencia.puml) |
| MC-07 design classes | [modelo_clases_diseno.puml](https://github.com/kinglez/mkl-uml/blob/main/tests/fixtures/pipeline/modelo_clases_diseno.puml) |
| Derived tests | [plan_pruebas.md](https://github.com/kinglez/mkl-uml/blob/main/tests/fixtures/pipeline/plan_pruebas.md) |

These are regression fixtures used by the eight validator contracts, not a formal human approval record or a universal design template. Generated answers can differ from these fixtures. The fixtures support the profile checks described in [Validation](VALIDATION.md).
