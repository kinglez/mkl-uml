# View selection and semantic review

| View | Question | Content |
|---|---|---|
| Context | Where is the system boundary and who interacts with it? | Target, people, neighboring systems and meaningful relationships |
| Container | Which applications/data stores collaborate? | Responsibilities, technology choices, communications and data ownership |
| Component | How is a selected container organized? | Container scope, internal components and relevant external collaborators |
| Code | How is one component implemented? | Relevant classes, interfaces, functions or data structures; normally a scoped UML class diagram |
| Deployment (supporting) | How do runtime units map to infrastructure? | Environment, nodes, instance placement, connections and relevant failure boundaries |

Select levels by the design question. A component diagram is scoped to a container;
a deployment view is a supporting view, not a mandatory fourth abstraction level.
The code level uses a static view of one component, typically UML classes; existing UML
class skills support it, and sequence skills explain complementary behavior. Preserve
the parent component and architecture-to-code mapping. Distinguish proposed structure
from current source-derived code. Do not expand every task into
all diagram levels or invent services/databases to fill a template.

A software-system box represents a software system, not a raw data artifact or business
capability. At context level, describe data inputs/outputs without promoting them to
neighboring systems. At lower levels, an actual database/filesystem store can be a data-store
container with ownership and technology made explicit. Check abstraction meaning separately
from macro names; a valid System_Ext call does not establish a software-system boundary.

Every view needs a clear title, scope, readable names and relationship intent.
Explain responsibilities, technology where relevant, direction, protocol and symbols.
Use a legend when notation or styling needs explanation. Check boundaries, external vs
internal roles, data authority, synchronous/asynchronous meaning and relevant failure paths.

Maintain explicit stable alias/ID mappings across views and versions. Check that the same
logical element keeps its meaning/name/technology; finer levels refine a coarser element.
A deployment node is infrastructure, not automatically an application or domain entity.
BCE controls do not map one-to-one to containers, components or classes.

Record architecture decisions against the functional behavior and quality scenarios they
address. For each significant choice explain alternatives, benefit, cost and verification.
A diagram with boxes is insufficient evidence of performance, recovery, security or SOLID.

## Handoff

Input: actual external evidence and available analysis/PDR outputs.
Output: selected editable views, decisions and quality-response strategies, source versions,
coverage/limits and implementation-changing open issues.
Consumer: detailed module/class/interaction/state design. It reads the actual architecture
and rechecks affected choices if upstream facts change. Missing essential input blocks its
dependent choice; scope exclusions require reasons.

At CDR, compare relevant detailed operations/interfaces/dependencies with this architecture.
Current CDR tools do not automatically parse C4; perform and label that comparison manually.
After implementation, architecture review checks whether the decisions and qualities were
realized with actual source/runtime evidence; it does not create missing up-front design.
