<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Methodology: the MKL pipeline

## What is MKL?

MKL is a use-case-driven software development process that occupies a middle ground between RUP, with its many disciplines and artifacts, and lightweight agile approaches that may leave the bridge between requirements and design implicit. Its defining feature is **dynamic traceability**: concrete, verifiable rules connect successive artifacts. Domain concepts become nouns in use case text; robustness objects inform sequence interactions; operation-invoking messages inform class operations; signals, replies and lifecycle messages retain their own semantics.

Primary sources: Rosenberg, D., & Stephens, M. (2007), *Use Case Driven Object Modeling with UML: Theory and Practice*, Apress; and Rosenberg, D., Stephens, M., & Collins-Cope, M. (2005), *Agile Development [abbreviated title]*, Apress. See the [Consolidated Bibliography](BIBLIOGRAPHY.md).

## The pipeline, artifact by artifact

| # | Skill | Output | Inputs | Gate |
|---|---|---|---|---|
| 1 | `mkl-uml-domain-modeler` | Domain model (`.puml`): conceptual problem vocabulary | Business description / requirements | — |
| 2 | `mkl-uml-use-case-diagram` | Use case diagram (`.puml`): actors, scope, relationships | Domain model + business description | — |
| 3 | `mkl-use-case-specifier` | Textual specification (`.md`): basic and alternative courses in event/response style | Use case diagram + domain model | — |
| 4 | `mkl-uml-robustness-diagram` | Robustness diagram (`.puml`): boundary/control/entity objects | Specification + domain model | — |
| 5 | `mkl-pdr-review` | Preliminary Design Review verdict and review record | All preceding artifacts together | Gate 1 |
| 6 | `mkl-uml-sequence-diagram` | Sequence diagram (`.puml`), operation delta, and test cases | Robustness + specification + domain | — |
| 7 | `mkl-uml-design-class-model` | Design class model (`.puml`) | Domain + sequence diagram(s) + specification | — |
| 8 | `mkl-cdr-review` | Critical Design Review verdict and record; optional code headers | Classes + sequences + robustness diagrams + specifications + domain + requirements + test plan | Gate 2 |

The two gates are deliberate: MKL reviews analysis before commitment to detailed design, and detailed design before commitment to implementation. Each gate uses a three-state verdict: accepted, accepted with rework verification, or reinspection required. The result is more informative than a binary approval.

## Backward traceability

The chain is maintained by checking that domain concepts in use case text belong to the domain model; actors and use case relationships agree with the use case diagram; robustness objects are grounded in specification text; sequence messages realize robustness control responsibilities; and class operations trace to operation calls, contracts, requirements or justified design decisions. An inconsistency in any of these links is a finding, not merely a stylistic variation.

## Standalone and formal workflow modes

Standalone assistance is the default. The pipeline table describes the explicit MKL workflow and does not impose its full input set on a standalone artifact request. See [Operating contract](OPERATING_CONTRACT.md) for minimum inputs, coverage states and stable IDs. Formal PDR/CDR sessions are opt-in. Run the checks that can be automated and **explicitly disclose** omitted checks. Undisclosed omissions make a review incomplete, rather than lightweight.

The same evidence discipline applies to bibliographic sources: each skill's `references/sources-and-methods.md` or equivalent distinguishes what was verified from what remains unverified. Report both completed verification and its limitations.

## Skill locations

Each pipeline stage corresponds to a directory under [`skills/`](../skills/). Its `README.md` documents purpose, methodological basis, concrete inputs and outputs, installation, validation, and the sources specific to that stage.
