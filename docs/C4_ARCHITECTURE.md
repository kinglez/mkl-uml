<!-- Copyright 2026 kingle.zhuang. Licensed under Apache-2.0. -->
# Design a high-level architecture

Use `mkl-uml-c4-architecture` to choose system boundaries, application responsibilities
and data ownership. It can start from your supplied requirements; a PRD or complete UML
workflow is not required. Start with the [copyable architecture example](../README.md#start-with-your-own-architecture).

## What comes in, and what goes out?

Provide the business goals, known rules, existing systems/technology and important
constraints. The result is selected C4 views plus notes explaining decisions,
alternatives, open questions and how quality requirements will be verified.

## Ask about behavior and quality

Only pursue questions that change a design choice:

- Who uses the system, and which success/failure outcomes must it support?
- Which external systems and existing technologies must be reused?
- Who owns each kind of data, identity and access decision?
- Which performance, capacity, security, recovery or operational needs affect the design?

Keep unknown targets open. For each important quality, record the scenario, expected
response, agreed measurable criterion and proposed verification. Do not invent a number
to make the document appear complete.

## Choose the views

| View | It explains | Use |
|---|---|---|
| System context | Users, target system and external dependencies | Establish the system boundary |
| Container | Applications/data stores, responsibilities and communication | Normal system overview |
| Component | The internals of one selected container | Add when it resolves a design question |
| Code | Classes/interfaces inside one selected component | Later detailed design when needed |
| Deployment | Runtime placement and failure boundaries | Supporting view when placement matters |

Context and container views usually suffice for an overview. Deployment is not the
fourth C4 level. A container means an application or data store, not necessarily Docker.
Files, records and other stored data are not independent software systems.

## Handoff artifacts

A small task can use this layout; optional views are added only when useful:

```text
architecture/
├── context.puml
├── container.puml
├── component.puml       # Optional
└── architecture.md      # Responsibilities, ownership, choices and open questions
```

Save available previews beside the sources. In architecture.md, explain data ownership,
trust/permission boundaries, alternatives and costs, quality scenarios and verification.
Detailed design consumes these decisions when allocating interfaces and operations.

## Drawing and checking

The skill draws C4-PlantUML using the local PlantUML standard library when available.
Check rendering, model meaning and requirement coverage separately. A diagram does not
prove that a performance or recovery target has been achieved.
The optional JSON record and CLI are for additional mechanical checks, not prerequisites
for requesting an architecture. See the [validation profile](../skills/mkl-uml-c4-architecture/references/validation-profile.md).

Continue with the [full tutorial](EXAMPLES.md#6-c4-architecture) when you need architecture
to feed sequence/class design. The primary method reference is [the C4 model](https://c4model.com/).
