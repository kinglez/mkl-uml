# Sources and capability boundaries

Original workflow guidance and neutral protocol fixtures in this skill are authored for
MKL. They do not contain an application requirement or reference business implementation.

Primary references consulted for this extension (method first, notation second):
- [Official C4 model](https://c4model.com/): system/context, containers, components and code.
- [C4 code diagram](https://c4model.com/diagrams/code): optional zoom into one component, normally using UML or a similar code representation.
- [C4 diagram levels](https://c4model.com/diagrams): select useful context/container/component/code views and supporting deployment views.
- [C4 review checklist](https://c4model.com/diagrams/checklist): inspect scope, element meaning, relationships and readable notation.
- [C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML): source notation, bundled includes and macro capabilities.
- [PlantUML standard library](https://plantuml.com/stdlib): use the local C4 library.
- [arc42 quality requirements](https://docs.arc42.org/section-10/): make relevant qualities concrete with scenarios and criteria.

These references guide authoring; no third-party library, figure, text passage or remote
renderer is bundled. C4-PlantUML retains its own license in its actual distribution.
Installed MKL UML sibling skills are optional collaborators; reading their definitions is
not invocation. Their profile validators do not automatically validate C4 semantics.
