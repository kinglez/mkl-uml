<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Documentation guide

MKL UML has eight skills for moving from requirements to a reviewed design. All introductory examples use **order pricing**: a Shopper asks for a shopping-cart quote with an optional coupon.

You do not need to read every document before starting. Use this order:

1. **[Project README](../README.md#quick-start)** — install the skills and create your first model.
2. **[Step-by-step tutorial](EXAMPLES.md)** — follow eight short prompts, each with inputs, outputs and a checkpoint.
3. **[Completed example tour](../examples/order-pricing/README.md)** — compare your work with the committed diagrams, reviews, code and test results.

## Choose the document for your question

| Your question | Document | What it gives you |
|---|---|---|
| How do I install or select skills? | [Installation](INSTALLATION.md) | One recommended method, then alternatives for local/offline installs and Claude web. |
| What do I send to the agent at each stage? | [Tutorial](EXAMPLES.md) | Eight copyable order-pricing prompts and concrete completion checks. |
| Why are there eight stages, and what do PDR/CDR mean? | [Workflow guide](MKL_METHODOLOGY.md) | The purpose of each stage and how findings lead to corrections. |
| Which files does a skill need, and how do I preserve IDs? | [Operating contract](OPERATING_CONTRACT.md) | Reference rules for inputs, coverage, handoffs and identifiers. Consult it when those details matter. |
| What has actually been tested? | [Validation record](VALIDATION.md) | Recorded executions and their limits. This is evidence, not the getting-started procedure. |
| What changed in a version? | [Release notes](RELEASE_NOTES.md) | Version history and distribution details. |
| Where do the modeling rules come from? | [Bibliography](BIBLIOGRAPHY.md) · [Third-party sources](THIRD_PARTY_SOURCES.md) | Original sources, attribution and what was or was not verified. |

## Find your way around the example

| What you want to inspect | Start here |
|---|---|
| Business problem and literal expected amounts | [Requirements](../examples/order-pricing/00-input/requirements.md) · [Acceptance oracle](../examples/order-pricing/00-input/ACCEPTANCE_ORACLE.md) |
| A specific stage's finished output | [Eight-stage artifact table](../examples/order-pricing/README.md#eight-stage-artifacts) |
| One rule followed through the whole design | [Traceability](../examples/order-pricing/TRACEABILITY.md) |
| Corrections found by the reviews | [Example tour](../examples/order-pricing/README.md#what-the-reviews-actually-caught) · [Change history](../examples/order-pricing/CHANGE_IMPACT.md) |
| SOLID reasoning and its actual evidence | [Scoped SOLID review](../examples/order-pricing/07-class-model/SOLID.md) |
| Maintenance of the published review baselines | [Advanced replay procedure](../examples/order-pricing/HOW_TO_REPLAY.md) |

The repository contains the complete example. Installing skills into another project copies the skills, not these project artifacts. From an offline skill package, [open the example on GitHub](https://github.com/kinglez/mkl-uml/tree/main/examples/order-pricing) or clone the repository to follow the tutorial.

Older implementation plans under `docs/superpowers/plans/` record development work. They are not steps that a skill user needs to execute.

## A few terms used in the tutorial

| Term | Meaning in this example |
|---|---|
| Artifact | A file produced or reviewed at a stage: a diagram, specification, test plan or review record. |
| Use case | A user goal. `CU-01 Quote cart` describes the Shopper's request and the system's response. |
| Robustness / BCE | Analysis using boundary (interaction interface), control (behavior responsibility), and entity (domain concept) objects. |
| PDR | Preliminary Design Review: check the analysis before detailed design. |
| CDR | Critical Design Review: check detailed design before implementation handoff. |
| Traceability | Explicit links that let you follow a requirement into behavior, design and tests. |

Passing automated checks gives evidence about the checks performed. The review record also explains semantic findings, missing evidence and any outstanding decisions.
