---
name: mkl-uml-c4-architecture
description: Create, review and validate C4 architecture in PlantUML, from system context through containers and components to a scoped UML code view. Use for high-level design, quality-driven decisions, supporting deployment views and detailed-design handoffs.
license: Apache-2.0
metadata:
  author: kingle.zhuang
---
# MKL C4 Architecture

Produce an architecture appropriate to the current question, with explicit boundaries,
responsibilities, dependencies and justified choices. C4 is an architecture model;
PlantUML is the notation/rendering tool. A C4 container is an application or data store,
not a requirement to deploy Docker or microservices.

The primary modeling reference is [the official C4 model](https://c4model.com/):
**system context → containers → components → code**. Deployment is a supporting view,
not the fourth level. C4-PlantUML supplies drawing macros, not the architecture method.

## Scope and inputs

Default to standalone generate/review/refactor/validate. Use the high-level design
handoff when requested. Accept any supplied sources: conversations, tickets, documents,
screenshots, contracts or current-system evidence, alone or combined. Record source
identity/version and distinguish confirmed requirements, assumptions and open questions.
No PRD, filename or input format is mandatory. Existing code establishes current behavior,
not automatically intended behavior.

Read actual targets before reviewing or refactoring. Reuse agreed decisions and current
artifacts. Ask only about missing information that changes behavior, acceptance or an
architectural choice; continue unaffected work. Preserve the requested endpoint.

## Architecture workflow

1. Identify target, audience, scope and source evidence. Read available domain, use-case,
   robustness and PDR results; missing sources limit the applicable comparisons.
2. Check functional behavior, actors, interactions, authoritative data and failure paths.
   Assess relevant quality requirements: performance/capacity, availability/recovery,
   consistency, security/privacy, observability, maintainability, compatibility, deployment
   and cost. Reuse settled answers. Mark irrelevant dimensions with reasons.
3. Turn important qualities into scenarios: context/load, stimulus, response, observable
   criterion and verification method. Retain source, priority and decision status. Do not
   invent numeric targets, business decisions or evidence. See [quality and decisions](references/quality-and-decisions.md).
4. Select views using [modeling and review](references/modeling-and-review.md). Context and
   container views normally explain a system-level design; add component/deployment views
   for actual questions. Zoom into a complex/important component at the code level only
   when useful; use the code-view route below. A bounded module task can justify a different selection. Reuse a
   checked host context rather than invent a deployed system around a library.
5. Allocate responsibilities, dependencies, data ownership and external interfaces. Compare
   the simplest viable alternatives. Record requirement → architecture decision → affected
   elements/views → validation strategy, including costs and unresolved trade-offs.
6. Inspect the actual sources across views. Preserve stable aliases/IDs and scope mappings;
   a repeated name alone is not traceability. Keep abstractions at their declared level.
   Read [validation profile](references/validation-profile.md) before using the CLI.
7. Render with an available authorized backend. Prefer the local bundled C4 library:
   `!include <C4/C4_Context>`, `C4_Container`, `C4_Component`, `C4_Deployment`.
   Use the same local version for repeatable output. Rendering is separate from semantic
   review. An unavailable renderer is a disclosed gap; do not silently upload sources.
8. Deliver editable sources, previews when available, decisions and verification limits.
   For a handoff, name the current inputs, ready outputs, unresolved blockers and actual
   next consumer. Revalidate affected decisions/views on source changes before reuse.

## Code-level zoom

For level 4, scope one component and map its responsibilities to actual/proposed classes,
interfaces, functions or data structures. Use UML class diagrams as the normal static
view; sequence diagrams explain behavior alongside it, not as a replacement for the
fourth static level. Preserve explicit parent system/container/component identities and
map code elements back to the selected component and architecture constraints.

Use `mkl-uml-design-class-model` when available, reading its installed instructions and
running its applicable validator; use `mkl-uml-sequence-diagram` for an interaction question.
If unavailable, produce the requested scoped UML directly and disclose the missing helper
checks. Do not pretend those skills were invoked or that the C4 literal checker validates
code diagrams. There is no required `C4_Code` include: ordinary PlantUML UML can express
this view. For an existing implementation, prefer current source-derived/tool-generated
structure and show only members needed for the question. For design-before-code, label
proposed structure. Do not impose a permanent class inventory for every component.

## Results and transition

Standalone: return the requested view or review, with material assumptions and limits.
A response-only request needs no project files or record. High-level handoff: use the
[brief](assets/architecture-brief.md) or existing equivalent to link requirements,
applicable views, decision trade-offs, quality scenarios and detailed-design constraints.

Detailed design consumes that architecture: map components/responsibilities to modules,
class/operation ownership, sequences and lifecycle behavior where applicable. The
`mkl-uml-design-class-model` and `mkl-uml-sequence-diagram` skills can consume this handoff;
`mkl-cdr-review` checks relevant architecture/design correspondence within its actual
coverage. Existing PDR evidence remains analysis evidence, not a substitute for this
architecture work. Do not invent formal approval, reviewers or a completed skill invocation.

## Optional mechanical checks

Standalone command template:
```bash
python3 scripts/validate_c4.py path/to/context.puml --level context
```

An optional record makes source/requirement/decision/view links inspectable:
```bash
python3 scripts/validate_c4.py --record path/to/architecture.json --require-ready
```

Start from [the draft record](assets/architecture-record.json). Replace draft fields with
actual results; JSON is an internal handoff option, not a restriction on requirement input.
Only record requirements in the current design scope. The checker reads local sources
without evaluating macros, includes or commands. It checks a documented literal profile,
references, selected view readiness and declared coverage. Unsupported constructs make
coverage partial and block the strict gate. It does not establish measurable adequacy,
actual NFR achievement, full PlantUML validity or architecture correctness. Run local
syntax/render checks and semantic review separately.

New instructions, templates and protocol fixtures remain business-independent. Keep
task-specific applications and evaluation evidence in the target project or an external
workspace. [Sources and boundaries](references/sources-and-methods.md).
