<!-- Copyright 2026 kingle.zhuang. Organization: mkl. -->
# Use one skill

Start with the result you want. You do not need to complete the whole workflow
or install the other skills.

## Choose a skill

| I want to… | Skill | Provide | Result |
|---|---|---|---|
| Design the high-level architecture | `mkl-uml-c4-architecture` | Goals, constraints and existing systems | C4 views and design decisions |
| Identify users and their goals | `mkl-uml-use-case-diagram` | System scope and actor goals | Use case diagram |
| Specify what happens in a scenario | `mkl-use-case-specifier` | A goal, known rules and outcomes | Textual use case |
| Clarify business concepts | `mkl-uml-domain-modeler` | Business terms and behavior | Conceptual model and glossary |
| Allocate analysis responsibilities | `mkl-uml-robustness-diagram` | A scenario and its flows | Boundary/control/entity diagram |
| Review the preliminary design | `mkl-pdr-review` | Existing analysis artifacts | Located findings and review notes |
| Design an interaction | `mkl-uml-sequence-diagram` | A scenario and responsibilities | Sequence diagram |
| Design classes and interfaces | `mkl-uml-design-class-model` | Responsibilities and contracts | Design class model |
| Review the detailed design | `mkl-cdr-review` | Existing class/interaction models | Consistency findings and remaining actions |

## Make a request

After [installation](INSTALLATION.md), send the skill name and a concrete task in chat:

```text
$mkl-uml-c4-architecture
Design an internal knowledge base where employees upload, search and read documents.
Access depends on department permissions; use our existing single sign-on service.
Ask only questions that change the architecture. Keep unknown quality targets open.
Save context/container diagrams, available previews and design notes in architecture/.
Stop at high-level design; detailed models and coding are later tasks.
```

Replace this business context with yours. State **what is known**, **what you want
produced**, and **where to save it**. Files, attachments and conversation notes are all
valid sources. The [nine copyable examples](../README.md#examples) show each skill in use.

## Check the result

- Does the artifact represent your rules and outcomes, including relevant failures?
- Are assumptions and unanswered questions visible?
- Are editable sources and requested notes saved in the chosen folder?
- Does the agent say which checks ran and what remains unverified?

A rendered diagram or successful script does not establish business correctness.
Review the actual content before relying on it.

## When you provide only part of a design

A review needs a real target. Missing comparison material limits that comparison;
it does not require generating every earlier stage.
The PDR CLI needs a robustness diagram. The CDR CLI needs both a class model and
a sequence. With only a class model, request a scoped manual review and keep interaction
checks unverified. See [exact input and review rules](OPERATING_CONTRACT.md) when needed.
