<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# MKL UML Skills

**Turn requirements into architecture and UML models, review the design, and trace it to tests.**

Nine independently usable skills cover analysis, C4 high-level architecture, detailed design and reviews. Use the skill needed for your question or connect their outputs into a workflow. Requirements can come from any supplied evidence: conversations, tickets, documents, images, contracts or an existing system. No PRD or input filename is required. Diagrams use PlantUML; specifications and review records use Markdown.

The nine-skill tutorial follows one example: **quote a shopping cart with an optional coupon**. The completed [order-pricing example](examples/order-pricing/README.md) includes requirements, diagrams, review findings, Python code and tests.

[Quick start](#quick-start) · [Examples](#examples) · [Use one skill](docs/STANDALONE.md) · [Run the finished example](#run-the-finished-example) · [Workflow](#workflow) · [Stage outputs](#stage-outputs) · [Documentation](#documentation)

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
GitHub revision into this project. Version 1.1.1 includes all nine skills:

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

## Examples

Choose any one of these nine **standalone prompts**. Each includes its own context for
an internal enterprise knowledge base; none requires running another example first.
These are usage illustrations, separate from the completed order-pricing tutorial.
Business examples stay here; the skill instructions and new protocol regressions remain
independent of this application.

Install the selected skill in your target project, replacing the name as needed:

```bash
npx skills add kinglez/mkl-uml --skill mkl-uml-c4-architecture -a codex -y
```

Paste a prompt into **agent chat**. For Claude Code, use `-a claude-code` when installing
and replace `$skill-name` with `/skill-name` in chat. Requirement sources may be
conversation notes, files or attachments. For review prompts, provide the actual targets;
illustrative paths below do not refer to existing files in this repository.

Output trees show proposed files, not already generated deliverables. Save SVG/PNG
previews alongside diagram sources when a local renderer is available; otherwise report
the missing rendering. See [standalone inputs and limits](docs/STANDALONE.md).

<a id="start-with-your-own-architecture"></a>
<details>
<summary><strong>1. C4 architecture — design the high-level structure</strong> — <code>mkl-uml-c4-architecture</code></summary>

```text
$mkl-uml-c4-architecture

Design the high-level architecture of an internal enterprise knowledge base.

Business requirements:
- Employees upload, search for, and read documents.
- Document access is controlled by department; administrators maintain permissions.
- Integrate with the existing single sign-on service.
- Prefer the existing technology stack and databases.

Read the supplied information first. Ask only questions that change an architecture
choice, including the available stack, department-membership source and permission
semantics. Keep unspecified performance, capacity and recovery targets open;
do not invent numbers or treat proposals as confirmed decisions.

Produce:
1. A system context diagram with users, the knowledge base and external dependencies.
2. A container diagram with application/data-store responsibilities and communication.
3. A component view of a core container only if it resolves a real design question.
4. Notes on data ownership, authentication versus authorization, permission boundaries,
   alternatives, trade-offs, quality scenarios and how those scenarios would be verified.

Save editable sources, available local previews and architecture.md under architecture/.
Use C4-PlantUML for the architecture views. Report checks actually run and their limits.
Stop at high-level architecture; leave class models, sequences and code for later.
```

**Expected files:**

```text
architecture/
├── context.puml
├── container.puml
├── component.puml       # Only when useful
└── architecture.md
```

</details>

<details>
<summary><strong>2. Use case diagram — identify actors and goals</strong> — <code>mkl-uml-use-case-diagram</code></summary>

```text
$mkl-uml-use-case-diagram

Create a use case diagram for an internal enterprise knowledge base.

Business requirements:
- Employees upload, search for, and read documents.
- Documents are accessible according to department permissions.
- Administrators maintain access permissions.
- Authentication uses the existing single sign-on service.

Identify the subject boundary, external roles and actor-valued goals. Explain which
external systems actually participate. Separate actor participation from initiation;
use include/extend only where the stated behavior justifies them.

Ask only questions that change the boundary, roles or goals. Keep unknown permission
policies open, including whether administrators have any special reading privileges.

Save use-cases.puml and actors-and-goals.md under analysis/use-cases/.
The notes should map actors and goals to the supplied requirements and list open issues.
Render locally if available and report actual checks and limits.
Only create the use case view; detailed flows, class design and code are outside this task.
```

**Expected files:**

```text
analysis/use-cases/
├── use-cases.puml
└── actors-and-goals.md
```

</details>

<details>
<summary><strong>3. Use case specification — define observable behavior</strong> — <code>mkl-use-case-specifier</code></summary>

```text
$mkl-use-case-specifier

Write a textual use case specification for 'Read a department-protected document'
in an internal enterprise knowledge base.

Known requirements:
- An employee selects a document to read.
- Authentication uses the existing single sign-on service.
- Access depends on department permissions maintained by administrators.
- An unauthorized employee must not receive the document content.

Describe the actor, goal, boundary, trigger, preconditions, numbered basic flow,
alternatives, exceptions, postconditions and observable acceptance criteria.
Anchor each alternative to its triggering step and show its continuation or termination.

Ask only questions that change the behavior: for example, who supplies department
membership, how conflicting permissions are resolved, and what may be disclosed when
access is denied. Keep unsettled behavior and unspecified quality targets open.

Preserve any existing IDs; mark new IDs provisional when no registry is supplied.
Save requirements/read-document.md with rules, acceptance criteria and open questions.
Run available structural checks and report their language/semantic limits.
Only specify this use case; leave diagrams, architecture choices and coding for later.
```

**Expected files:**

```text
requirements/
└── read-document.md
```

</details>

<details>
<summary><strong>4. Domain model — clarify business concepts</strong> — <code>mkl-uml-domain-modeler</code></summary>

```text
$mkl-uml-domain-modeler

Create a conceptual domain model for an internal enterprise knowledge base.

Business requirements:
- Employees upload, search for, and read documents.
- Access is controlled by department; administrators maintain permissions.
- Authentication uses the existing single sign-on service.

Identify business concepts, distinguish entities from values and roles, and explain
the relationships supported by these requirements. Use concepts such as document,
department and access permission only where their meaning is supported.

Ask only questions that change a concept or constraint, such as whether employees
can belong to several departments and whether documents can be shared across departments.
Record unknown cardinality, ownership and policy rather than guessing.

Save domain.puml and glossary.md under analysis/domain/.
Use the default conceptual profile; keep implementation services, controllers,
repositories, database tables and operation signatures for detailed design.
Render locally if available; report actual checks, assumptions and proposed vocabulary.
Only produce the domain model and glossary.
```

**Expected files:**

```text
analysis/domain/
├── domain.puml
└── glossary.md
```

</details>

<details>
<summary><strong>5. Robustness analysis — allocate boundary, control and entity responsibilities</strong> — <code>mkl-uml-robustness-diagram</code></summary>

```text
$mkl-uml-robustness-diagram

Perform robustness analysis for 'Read a department-protected document' in an
internal enterprise knowledge base.

Scenario:
- An authenticated employee selects a document.
- The system evaluates the employee's department access.
- If permitted, it retrieves and presents the document content.
- If denied, it returns a refusal without the document content.
- If the document is unavailable, the employee receives an appropriate failure outcome.
Administrators maintain permissions; authentication uses existing single sign-on.

Identify boundaries, controls and entities. Map the basic, denied and unavailable
flows to their responsibilities and links; explain why each object has its BCE role.
Keep unresolved disclosure/failure behavior explicit and ask only when it changes
this analysis. Controls are responsibilities, not predetermined implementation classes.

Save robustness.puml and behavior-map.md under analysis/robustness/.
Use a supplied domain model for entity closure if available; otherwise report that
comparison as unverified while completing the requested scenario analysis.
Render locally if available and report checks actually run.
Stop before sequence timing, method signatures, architecture decomposition or code.
```

**Expected files:**

```text
analysis/robustness/
├── robustness.puml
└── behavior-map.md
```

</details>

<details>
<summary><strong>6. PDR — review a preliminary design</strong> — <code>mkl-pdr-review</code></summary>

```text
$mkl-pdr-review

Perform a scoped preliminary-design review of an internal enterprise knowledge base.

Known requirements:
- Employees upload, search for, and read documents.
- Department permissions control access and are maintained by administrators.
- Authentication uses the existing single sign-on service.

Review target: analysis/robustness/robustness.puml.
I will provide or identify this existing diagram; the path is illustrative.
Compare with any use case specifications, domain model or interface evidence I also
supply. Ask for an absent review target; do not generate earlier stages to replace it.

Check BCE responsibilities and connections, entity provenance, data flow, permission
decisions, and basic/alternative/exception coverage within the available evidence.
Distinguish confirmed defects, heuristic review candidates and unverified comparisons.

Save reviews/pdr.md with the reviewed inputs/versions, located findings, impact,
recommended corrections, coverage and remaining decisions.
Run applicable checks; make no claim that missing comparisons were executed.
Only review the supplied design. Leave source artifacts unchanged and keep this
scoped technical review separate from formal PDR approval.
```

**Expected files:**

```text
reviews/
└── pdr.md
```

</details>

<details>
<summary><strong>7. Sequence diagram — design one interaction</strong> — <code>mkl-uml-sequence-diagram</code></summary>

```text
$mkl-uml-sequence-diagram

Design the detailed interaction for reading a department-protected document in an
internal enterprise knowledge base.

Behavior to model:
- The employee is already authenticated through existing single sign-on.
- A document-reading boundary receives the request.
- The system evaluates department access before returning any protected content.
- Allowed access retrieves and returns the content.
- Denied access returns a refusal; an unavailable document follows an explicit failure path.

Choose participants and allocate calls to meaningful responsibilities. Distinguish
operation calls, replies and any asynchronous events. Show justified guards and
the outcome of every modeled branch. Keep transport/error conventions open unless supplied.

Ask only questions that change this interaction. Use existing interfaces and design
constraints when available; mark new technical participants as proposed design choices.
Missing upstream diagrams should limit their comparisons, not require a full workflow.

Save read-document.puml and interaction-notes.md under design/interactions/.
Explain operation ownership and open contracts in the notes. Render locally if available
and report actual checks and coverage. Only design this interaction; no code or class model.
```

**Expected files:**

```text
design/interactions/
├── read-document.puml
└── interaction-notes.md
```

</details>

<details>
<summary><strong>8. Design class model — define cohesive contracts</strong> — <code>mkl-uml-design-class-model</code></summary>

```text
$mkl-uml-design-class-model

Design a class model for the document-reading module of an internal enterprise
knowledge base.

Requirements:
- Employees are authenticated by existing single sign-on.
- Department permissions must be evaluated before document content is returned.
- Administrators maintain permissions.
- Prefer existing application, storage and permission interfaces where available.
- Keep denied access and unavailable content as explicit observable outcomes.

Allocate state, decisions and orchestration to cohesive responsibilities.
Define the required operations, typed parameters/results, interfaces and dependencies.
Explain which concepts come from the requirements and which are proposed technical seams.
Keep storage and permission-provider details replaceable where the requirements justify it;
avoid introducing patterns or an interface for every class without a reason.

Ask only questions that affect a contract, responsibility or dependency. Use supplied
architecture/sequences when available and disclose missing provenance comparisons.

Save classes.puml and design-notes.md under design/classes/.
Explain responsibilities, extension points and dependency ownership, with the evidence
and limits of any SOLID claims. Render/check locally if available.
Only produce the design model; leave implementation and runtime verification for later.
```

**Expected files:**

```text
design/classes/
├── classes.puml
└── design-notes.md
```

</details>

<details>
<summary><strong>9. CDR — review detailed-design consistency</strong> — <code>mkl-cdr-review</code></summary>

```text
$mkl-cdr-review

Perform a scoped detailed-design review of an internal enterprise knowledge base.

Known requirements:
- Employees upload, search for, and read documents.
- Department permissions control access; administrators maintain permissions.
- Authentication uses the existing single sign-on service.
- Prefer the existing technology stack and databases.

Review inputs (replace with my actual files or attachments):
- design/classes/classes.puml
- design/interactions/read-document.puml
Use any specifications, architecture decisions or test plans I actually provide.

Check operation allocation against calls, signatures, cohesive responsibilities,
authorization boundaries, failure paths, dependency direction and requirement traceability.
Assess SOLID claims against available evidence; record absent source/runtime verification.
Only raise actionable findings supported by the reviewed artifacts.

If only a class model is supplied, complete that scoped review and identify the missing
interaction checks. The full CDR CLI needs both classes and a sequence; do not invent
a sequence merely to make it run. Missing materials cannot establish full readiness.

Save reviews/cdr.md with inputs/versions, findings and locations, impact, proposed
corrections, actual tool results, coverage and remaining questions.
Only review; do not modify the models, generate implementation code or claim formal approval.
```

**Expected files:**

```text
reviews/
└── cdr.md
```

</details>

For a complete connected example, continue with the [nine-stage tutorial](docs/EXAMPLES.md).
For C4 view selection and architecture handoffs, see [the C4 guide](docs/C4_ARCHITECTURE.md).

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
