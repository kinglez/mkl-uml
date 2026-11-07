# Literal profile and optional record

The checker uses Python 3.9+ standard library, reads files only, and never renders or
executes includes/macros/recorded verification text. Its output is mechanical evidence.

## Standalone

The CLI level values select four supported source profiles, not the four C4 abstraction
levels: deployment is supporting. Code-level UML uses the class skill/validator and
manual component mapping; it is outside this literal C4 macro checker.

Pass one .puml file with --level context/container/component/deployment. Use the matching
bundled include, one @startuml/@enduml pair, literal aliases, quoted names and literal
technology labels. Supported elements: Person/System and their _Ext forms, Container,
ContainerDb/Queue, Component, ComponentDb/Queue, System_Boundary, Container_Boundary,
Boundary, Enterprise_Boundary, Deployment_Node and Node. Scope braces appear on the call
line and closing braces occupy their own lines. Literal calls can span lines. Rel/BiRel/
Rel_Back with optional _U/_D/_L/_R directions are checked for endpoints and nonempty intent.
Basic title/direction/one-line skinparam and selected LAYOUT/SHOW/HIDE calls are display-only.
Computed/named arguments and unknown display macros make coverage partial. This narrow
profile deliberately does not evaluate the full library language.

Comments, notes and legends cannot provide modeled declarations. Remote/local arbitrary
includes are outside the profile. Other constructs are reported as partial coverage;
they must not silently establish strict readiness. This is a local profile, not the full
C4-PlantUML language. Full syntax remains a separate renderer check.

## Record version 1

Use assets/architecture-record.json as a draft. Unknown fields and duplicate IDs/JSON keys
are rejected. IDs are stable task references; sources can point to any external medium.

| Field | Contents |
|---|---|
| schema_version | Integer 1 |
| scope | Current architectural question and limits |
| required_levels | Nonempty, explicit selected levels; normally context/container for a system |
| sources | id, reference; location/version or description of supplied external evidence |
| requirements | id, kind functional/quality/constraint, text, source_ids, status confirmed/open/proposed; optional priority |
| quality_scenarios | id, requirement_ids, context, stimulus, response, measure, verification; optional source_ids, priority, status confirmed/open/proposed |
| decisions | id, requirement_ids, view_ids, decision, rationale, tradeoffs, status settled/proposed |
| views | id, level, status ready/draft/not_applicable, scope alias, reason; artifact for an actual view |
| handoff | status ready/draft, consumer, notes |

Every current requirement needs a source and an architectural response/retain decision.
Every decision links at least one actual applicable view through view_ids. These links
are declared references; their semantic adequacy is reviewed against the actual sources.
Quality requirements need linked quality scenarios; criteria are reviewed semantically.
Unconfirmed inputs and proposed choices block declared readiness. Optional scenario
metadata preserves explicit source IDs, textual priority and agreement status. Omitted
source/status metadata inherits from linked requirements; priority may be recorded there
or in the brief. An explicit open/proposed scenario also blocks readiness. Confirmed
means the scenario is agreed, not that its runtime quality has been achieved.

A required level needs a ready checked source. Non-applicable optional views have reasons
and no artifact. Artifacts are existing relative files under the record directory, or
--project-root when supplied; absolute/traversing/symlink-escaping paths are rejected.
Container/component record views identify their corresponding system/container boundary
through scope. The scoped managed profile checks ownership of internal children; use
System_Ext/Container_Ext for collaborators beyond that scope. Deployment uses physical
placement without replacing logical ownership. Shared aliases are compared across views
for type, label and technology; preserve aliases when an element is actually the same.

The checker does not authenticate sources, detect unannounced changes, prove inputs were
read, infer required views, execute checks, validate decisions against reality, or grant
formal acceptance. A handoff is rechecked against current evidence when consumed.

Exit 0: no structural findings; strict --require-ready additionally requires no blockers
or partial-profile warnings. Exit 1: findings/gate failure. Exit 2: unreadable/invalid input.
Results: structure_valid, ready, errors, blockers, warnings and coverage. Rendering remains
not_run and architecture_semantics remains not_verified even for a mechanically ready record.
