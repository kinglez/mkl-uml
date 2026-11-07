<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# MKL UML Skills

**Turn requirements into architecture and UML models, review the design, and trace it to tests.**

Nine independently usable skills cover analysis, C4 high-level architecture, detailed design and reviews. Use the skill needed for your question or connect their outputs into a workflow. Requirements can come from any supplied evidence: conversations, tickets, documents, images, contracts or an existing system. No PRD or input filename is required. Diagrams use PlantUML; specifications and review records use Markdown.

The nine-skill tutorial follows one example: **quote a shopping cart with an optional coupon**. The completed [order-pricing example](examples/order-pricing/README.md) includes requirements, diagrams, review findings, Python code and tests.

[Quick start](#quick-start) · [Run the finished example](#run-the-finished-example) · [Workflow](#workflow) · [Stage outputs](#stage-outputs) · [Documentation](#documentation)

## What does this help you do?

| When you need to… | Use the skills to… |
|---|---|
| Understand requirements before coding | Agree on business concepts, actors and user goals. |
| Work out success and failure behavior | Specify flows and show how responsibilities collaborate. |
| Choose a high-level architecture | Link functional and quality requirements to system boundaries, applications, data stores and design trade-offs. |
| Explain a design | Connect class state and operations to requirements and interactions. |
| Keep documents and tests consistent | Review the links between artifacts and record gaps or corrections. |

<a id="how-to-use"></a>

## Quick start

### 1. Get the example and install the skills

Run in your **terminal**. This checkout supplies the example files used below:

```bash
git clone https://github.com/kinglez/mkl-uml.git
cd mkl-uml
```

Choose your agent. These commands install the skills available in the published
GitHub revision into this project. Version 1.1.0 includes all nine skills:

```bash
# Codex
npx skills@latest add kinglez/mkl-uml -a codex --skill '*' -y

# Claude Code
npx skills@latest add kinglez/mkl-uml -a claude-code --skill '*' -y
```

To install directly from a local checkout:

```bash
npx skills add . -a codex --skill '*' -y
```

The Skills CLI needs Node.js 22.20+ and Git. Python 3.9+ runs the validators and executable example. To install into your own project, run the installation command there instead; the example files come from this checkout. See [installation options](docs/INSTALLATION.md).

### 2. Create the first model

Open this checkout in your agent. Paste the following into the **agent chat**:

```text
$mkl-uml-domain-modeler
Read examples/order-pricing/00-input/requirements.md and
examples/order-pricing/00-input/ACCEPTANCE_ORACLE.md.
Create a conceptual domain model for CU-01 Quote cart.
Save domain.puml and glossary.md under uml/order-pricing/01-domain/.
Explain the business concepts, relationships and unresolved assumptions.
Keep implementation services and discount strategies for detailed design.
Leave the completed examples/order-pricing reference files unchanged.
Run the applicable validator and report its actual result and limits.
```

For Claude Code, replace the first line with `/mkl-uml-domain-modeler`.

**Check the result:** your new folder contains `domain.puml` and `glossary.md`. The model explains concepts such as Cart, CartLine, Product, Coupon and PriceQuote. Compare it with the [completed domain model](examples/order-pricing/01-domain/domain.png).

### 3. Continue one stage at a time

Follow the **[nine-stage tutorial](docs/EXAMPLES.md)**. Each stage explains its purpose, names its inputs, gives a copyable prompt, and links to a completed result. It uses `uml/order-pricing/` for your work and leaves the published example available for comparison.

You can stop after the artifact you need. For your own project, replace the teaching requirements with your requirements and use your existing IDs.

<a id="complete-worked-example-order-pricing"></a>

## Start with your own architecture

Install just the architecture skill with the standard command:

```bash
npx skills add kinglez/mkl-uml --skill mkl-uml-c4-architecture
```

Then provide your actual sources in chat:

```text
$mkl-uml-c4-architecture
Read the sources supplied in this conversation and the current analysis artifacts.
Identify confirmed functional requirements, applicable quality requirements and open
architecture-changing questions. Create the C4 views needed for this scope using
C4-PlantUML. Explain alternatives and trade-offs, render locally if available, and
hand the decisions, quality scenarios and constraints to detailed design.
Do not invent missing targets or a system around a bounded module.
```

Use **[the C4 guide](docs/C4_ARCHITECTURE.md)** for view selection, stage inputs/outputs and verification. A request for one diagram does not require the complete workflow. The command above discovers the published GitHub revision. Use the [local installer](docs/INSTALLATION.md#python-installer-and-windows) for a checkout or the [pinned installation](docs/INSTALLATION.md#pinned-source-or-bundled-npx-installer) for v1.1.0.

## Run the finished example

You can inspect and execute the committed example before generating any models. From the repository root:

```bash
python3 examples/order-pricing/09-reference-implementation/run_example.py
python3 examples/order-pricing/scripts/verify.py
```

The cart contains two CNY 120.00 books and one CNY 15.00 pen: **CNY 255.00**. The demo prints these results, plus unknown and expired coupon refusals:

| Coupon | Discount | Payable |
|---|---:|---:|
| None | CNY 0.00 | CNY 255.00 |
| SAVE30 | CNY 30.00 | CNY 225.00 |
| TENOFF | CNY 25.50 | CNY 229.50 |
| BIGSAVE, capped at the subtotal | CNY 255.00 | CNY 0.00 |

JSON amounts are integer cents: `22500` means CNY 225.00. Quoting creates no order and leaves the inputs unchanged. No live service or Python dependency installation is needed.

The verifier checks the **committed reference example**, including its reviewed source baselines, validators, headers and tests. It does not check your newly generated `uml/order-pricing/` folder. A successful run ends with `Result: PASS`; its separate formal-acceptance status remains `NOT FULLY VERIFIED` because no human/business approval is claimed.

Read the **[guided example tour](examples/order-pricing/README.md)** to follow the results back to their requirements and diagrams. Pre-rendered images are included. Add `--render` to the verifier only if you have PlantUML installed and want to regenerate them.

## Workflow

![MKL UML workflow: analysis and PDR, C4 architecture, detailed design, review and feedback](docs/assets/workflow.svg)

Connect the stages through their outputs:

| Stage | Reads | Produces for the next stage |
|---|---|---|
| Requirements and analysis | Supplied evidence in any medium | Concepts, use cases, behavior, BCE responsibilities and PDR findings |
| High-level architecture — `mkl-uml-c4-architecture` | Confirmed requirements, relevant quality scenarios and current analysis/PDR | Selected C4 views, decisions, trade-offs, data ownership and detailed-design constraints |
| Detailed design | Architecture handoff and specified behavior | Sequence diagrams, class model, contracts, lifecycle design where needed and test plan |
| CDR and implementation handoff | Current architecture, detailed design and applicable test evidence | Findings, verified corrections, remaining blockers and implementation constraints |

**PDR (Preliminary Design Review)** checks analysis consistency. **CDR (Critical Design Review)** checks detailed-design consistency. When architecture is in scope, CDR also needs a labeled semantic comparison against its decisions and views; its existing CLI does not parse C4 automatically. An upstream change reopens the affected downstream checks.

The [official C4](https://c4model.com/) zoom is **system context → containers → components → code**. The code view uses a scoped UML class model of a component; sequence diagrams complement it with behavior. Context and container views normally explain a system-level design. Component and deployment views answer additional questions when needed. C4-PlantUML is the drawing library; it does not choose an architecture or prove quality targets. Rendering, semantic review and formal approval are separate evidence.

The maintained order-pricing example now includes a dated C4 architecture replay between PDR and detailed design. It retains the frozen business requirements and runnable implementation, then checks the new architecture against them. Formal review remains an explicit scope; automated checks alone establish neither formal approval nor SOLID conformance. See the [workflow guide](docs/MKL_METHODOLOGY.md).

<a id="what-each-stage-produces"></a>

## Stage outputs

These are **existing files** in the completed example. The tutorial creates corresponding working outputs under `uml/order-pricing/`.

```text
examples/order-pricing/
├── 00-input/
│   ├── requirements.md          Business rules and scope
│   └── ACCEPTANCE_ORACLE.md     Independently derived expected results
├── 01-domain/
│   ├── domain.puml              1. Business concepts and relationships
│   └── glossary.md
├── 02-use-cases/use-cases.puml   2. Shopper and CU-01 Quote cart
├── 03-spec/CU01-quote-cart.md    3. Success, alternative and exception flows
├── 04-robustness/
│   ├── robustness.puml          4. Boundary, control and entity analysis
│   └── correspondence.md
├── 05-pdr/PDR-01.md             5. Analysis findings and design handoff
├── architecture/               6. C4 views, decisions and quality scenarios
│   ├── context.puml
│   ├── container.puml
│   ├── component.puml
│   ├── code.puml                   Scoped UML code view
│   ├── architecture-brief.md       Constraints consumed by detailed design
│   ├── architecture.json           Requirement / decision / view links
│   └── component-code-map.json     Actual component-to-code allocation
├── 06-interactions/
│   ├── sequence.puml            7. Collaborations and guarded branches
│   ├── operation-delta.md          Operations allocated to their receivers
│   ├── test-plan.md                Observable expected behavior
│   └── DESIGN_DECISIONS.md
├── 07-class-model/
│   ├── classes.puml             8. Typed state, operations and relationships
│   ├── provenance.md               Why each member belongs in the design
│   └── SOLID.md                    Evidence and limits for design principles
├── 08-cdr/CDR-01.md             9. Detailed-design findings and readiness
├── handoffs/                   Reviewed snapshots used by the next stage
│   ├── analysis.json               Analysis -> architecture input
│   ├── architecture.json           Architecture -> detailed-design input
│   └── design.json                 Reviewed design/code source set
└── 09-reference-implementation/ Additional executable code and tests
```

Existing numbered paths are retained for link compatibility; `architecture/` is consumed after `05-pdr/` and before `06-interactions/`. Implementation is a subsequent task; this example includes it as executable evidence. The [traceability guide](examples/order-pricing/TRACEABILITY.md) connects requirement IDs to behavior, design members and tests.

## Documentation

Start with the **[documentation reading guide](docs/README.md)**. Read only the material needed for your task:

| Your next task | Read |
|---|---|
| Design architecture from your own sources | [C4 architecture guide](docs/C4_ARCHITECTURE.md) |
| Follow all nine skills using order pricing | [Step-by-step tutorial](docs/EXAMPLES.md) |
| Inspect the already completed result | [Example tour](examples/order-pricing/README.md) |
| Choose another installation method | [Installation](docs/INSTALLATION.md) |
| Understand the workflow and review stages | [Workflow guide](docs/MKL_METHODOLOGY.md) |
| Look up input requirements, IDs or review states | [Operating contract](docs/OPERATING_CONTRACT.md) |
| Inspect actual checks, limits or version changes | [Validation record](docs/VALIDATION.md) · [Release notes](docs/RELEASE_NOTES.md) |

## Development and license

From the repository root, run `python3 -m unittest discover -s tests -v` for the regression suite or `python3 tools/package_skill.py` to build the per-skill archives. [Distribution details](docs/INSTALLATION.md#offline-skill-archives) explain the archive format.

**kingle.zhuang** · <kinglezhuang@vip.qq.com> · **mkl** · Copyright **2026**.

[Apache-2.0](LICENSE). [NOTICE](NOTICE) contains upstream attribution and project guidance. MKL is this edition's branding for the adapted workflow; [bibliography](docs/BIBLIOGRAPHY.md) and [source notes](docs/THIRD_PARTY_SOURCES.md) retain the original authors' attribution. This edition was translated and adapted with AI assistance; AI tools are not coauthors.
