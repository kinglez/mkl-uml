<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Tutorial: design an order-pricing feature

This exercise connects all nine skills. If you need only one result, start with the
[single-skill examples](../README.md#examples). To inspect the finished work, use the
[example tour](../examples/order-pricing/README.md).

## Before you start

1. [Install the skills](INSTALLATION.md), then open a checkout of this repository.
2. Send the prompts below **one at a time in agent chat**.
3. Write new work under `uml/order-pricing/`; leave `examples/order-pricing/` unchanged.
   If that output folder is occupied, choose a new prefix and use it consistently.

```bash
git clone https://github.com/kinglez/mkl-uml.git
cd mkl-uml
```

Prompts use Codex's `$skill-name`; Claude Code uses `/skill-name`.
At each step, inspect the result, keep unresolved questions visible and ask the agent
to run applicable checks against **your generated files**. Save previews when a local
renderer is available. Reuse existing IDs; preserve their meaning across revisions.

## The scenario

A Shopper requests a cart price quote, optionally using one Coupon. Prices come from
a trusted catalog. Return subtotal, discount and payable amount, or an explicit refusal.
Quoting changes no cart/Coupon state and creates no Order.

Use the [requirements](../examples/order-pricing/00-input/requirements.md) and
[independent expected results](../examples/order-pricing/00-input/ACCEPTANCE_ORACLE.md)
for all rules and edge cases. Amounts are integer cents. For example, the CNY 255.00
cart with SAVE30 has CNY 225.00 payable. No new rule is implied by an unanswered case.

## What you will produce

All paths below are relative to `uml/order-pricing/`:

| Step | Main result |
|---|---|
| 1. Domain | `01-domain/domain.puml`, `glossary.md` |
| 2. User goals | `02-use-cases/use-cases.puml` |
| 3. Behavior | `03-spec/CU01-quote-cart.md`, `interface-contract.md` |
| 4. Responsibilities | `04-robustness/robustness.puml`, `correspondence.md` |
| 5. PDR | `05-pdr/PDR-01.md` |
| 6. Architecture | Selected views and `architecture/architecture-brief.md` |
| 7. Interaction | `06-interactions/sequence.puml`, operation/test notes |
| 8. Classes | `07-class-model/classes.puml`, provenance/SOLID notes |
| 9. CDR | `08-cdr/CDR-01.md` |

<a id="1-domain-model"></a>

## 1. Name the business concepts

```text
$mkl-uml-domain-modeler
Read the requirements and ACCEPTANCE_ORACLE.md in examples/order-pricing/00-input.
Work under uml/order-pricing/01-domain; leave reference files unchanged.
Create domain.puml and glossary.md for CU-01 Quote cart. Explain the concepts,
relationships, confirmed constraints and open policy; keep implementation classes out.
```

**Check:** Cart, CartLine, Product, Coupon and PriceQuote have clear meanings.
An algorithm is not automatically a business entity.
Compare the [domain model](../examples/order-pricing/01-domain/domain.png).

<a id="2-use-case-diagram"></a>

## 2. Identify the user goal

```text
$mkl-uml-use-case-diagram
Read the source requirements and my uml/order-pricing/01-domain output.
Create uml/order-pricing/02-use-cases/use-cases.puml for CU-01 Quote cart.
Show the Shopper and system boundary. Keep internal lookup/calculation inside
the goal; the trusted in-process catalog is not a separate external actor.
```

**Check:** the goal is a quote, not checkout, payment or order creation.
Compare the [use case view](../examples/order-pricing/02-use-cases/use-cases.png).

<a id="3-use-case-specification"></a>

## 3. Specify success and refusal behavior

```text
$mkl-use-case-specifier
Read the source requirements/oracle and my generated domain/use-case files.
Under uml/order-pricing/03-spec, write CU01-quote-cart.md and interface-contract.md.
Specify the basic flow, discount alternatives and all required refusals, including
their conditions, system response and continuation/termination. Keep prices trusted,
amounts in integer cents and the operation read-only. Leave undefined policy open.
```

**Check:** every specified result has an observable outcome; invalid input is handled
rather than silently excluded by a precondition.
Compare the [specification](../examples/order-pricing/03-spec/CU01-quote-cart.md).

<a id="4-robustness-analysis"></a>

## 4. Connect behavior to responsibilities

```text
$mkl-uml-robustness-diagram
Read my uml/order-pricing/01-domain through 03-spec files.
Create robustness.puml and correspondence.md under uml/order-pricing/04-robustness.
Identify boundaries, controls and entities; map basic, alternative and exception
behavior to responsibilities and data. Explain any proposed domain-model addition.
```

**Check:** a boundary is an interaction interface, a control coordinates behavior,
and an entity holds business information. These are analysis roles, not fixed services.
Compare the [robustness view](../examples/order-pricing/04-robustness/robustness.png).

<a id="5-pdr-preparation"></a>

## 5. Review the analysis: PDR

PDR means **Preliminary Design Review**: check that the analysis agrees.

```text
$mkl-pdr-review
Review my uml/order-pricing/01-domain through 04-robustness files against the
source requirements and oracle. Save uml/order-pricing/05-pdr/PDR-01.md.
Locate findings, correct affected working files and recheck them. End with reviewed
inputs, correction evidence, remaining constraints and the technical basis for
architecture/design. Record only actual reviewer participation.
```

**Check:** resolve issues that change the next design choice; a closed finding needs
correction evidence. Formal approval is separate from this technical recommendation.
Compare the [PDR record](../examples/order-pricing/05-pdr/PDR-01.md).

<a id="6-c4-architecture"></a>

## 6. Choose the high-level architecture

```text
$mkl-uml-c4-architecture
Read my reviewed analysis/PDR under uml/order-pricing and the source requirements.
Under uml/order-pricing/architecture, create the C4 views useful for this local
program and architecture-brief.md. Explain responsibilities, data ownership,
alternatives and quality constraints for detailed design. Reuse the local runner
and in-process catalog; do not invent services, databases or numeric quality targets.
```

**Check:** architecture choices answer the real constraints. Context/container views
normally explain the overview; add further views only for a useful question.
Compare the [architecture brief](../examples/order-pricing/architecture/architecture-brief.md).

<a id="6-sequence-diagram-and-tests"></a>

## 7. Allocate calls and derive tests

```text
$mkl-uml-sequence-diagram
Read my current architecture/architecture-brief.md, PDR and analysis under
uml/order-pricing. Recheck changed inputs or unresolved blocking findings.
Under uml/order-pricing/06-interactions, create sequence.puml for all specified paths.
Also save operation-delta.md, test-plan.md and DESIGN_DECISIONS.md. Allocate calls
to their receivers, distinguish replies/events, and derive expected results from
the source oracle rather than the proposed implementation.
```

**Check:** refusals terminate without a successful quote; no-Coupon behavior needs
no Coupon lookup. The test plan describes expected tests, not executed results.
Compare the [sequence](../examples/order-pricing/06-interactions/sequence.png).

<a id="7-design-class-model"></a>

## 8. Build the design class model

```text
$mkl-uml-design-class-model
Read my current domain, specification, architecture and interaction outputs under
uml/order-pricing. Create 07-class-model/classes.puml, provenance.md and SOLID.md.
Define typed state, complete operation contracts and justified relationships.
Explain member origins, discount-extension/substitution seams and dependency ownership.
Keep source/runtime claims unverified when implementation or execution is unavailable.
```

**Check:** responsibilities and contracts are justified by behavior or design decisions.
Interface arrows alone do not prove SOLID. An optional C4 code zoom maps a selected
component to its relevant classes; it is not required for every class model.
Compare the [class model](../examples/order-pricing/07-class-model/classes.png).

<a id="8-cdr-preparation"></a>

## 9. Review the detailed design: CDR

CDR means **Critical Design Review**: compare the detailed design and its behavior.

```text
$mkl-cdr-review
Review my uml/order-pricing class/interaction models against the current architecture,
analysis/PDR, source requirements/oracle and test plan. Save uml/order-pricing/08-cdr/CDR-01.md.
Check operation allocation, signatures, failure coverage, dependencies and expected
results. Correct affected working files and recheck them. Record located findings,
actual checks, remaining actions and missing implementation/execution evidence.
Keep formal approval separate from this technical review.
```

**Check:** the review states what was examined and what remains unknown.
Compare the [CDR record](../examples/order-pricing/08-cdr/CDR-01.md).

## Check your results

Review the files you generated under `uml/order-pricing/` against the requirements
and checkpoints. Different names/layouts can be valid when their behavior is justified.

To run the **maintained reference**, use the terminal from the repository root:

```bash
python3 examples/order-pricing/09-reference-implementation/run_example.py
python3 examples/order-pricing/scripts/verify.py
```

These commands check the committed reference, **not your generated files**.
Maintenance details are in [HOW_TO_REPLAY.md](../examples/order-pricing/HOW_TO_REPLAY.md).

## Apply this to your project

Replace the requirements and expected outcomes, choose one output folder, preserve
existing IDs and request only the stages you need. The [workflow overview](MKL_METHODOLOGY.md)
explains how outputs connect. Append `Explain the result in Chinese; keep identifiers
unchanged.` when you want Chinese explanations.
