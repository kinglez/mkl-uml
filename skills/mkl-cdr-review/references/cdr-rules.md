<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# The ten CDR checks

Use these checks to assess whether the selected detailed design is implementable and consistent with its requirements. This is independently worded MKL operational guidance, informed by Rosenberg & Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice* (2007), chapters 8–9 and 11–12. Chapter 9 supplies the historical countdown numbering. Source status and limitations are recorded in [sources-and-methods.md](sources-and-methods.md).

For standalone work, check the supplied target and available supporting evidence. For a formal release review, enumerate the release's use cases and record every applicable evidence gap. Missing evidence withholds full acceptance; continue checks that are independent of it. Review-and-fix authorization is governed by `SKILL.md`.

## Traverse by use case and required behavior

List each selected `CU-XX`, its `DS-XX`, and the related model, requirements and tests. When robustness diagrams are supplied, use their Controllers as a behavior worklist rather than reviewing the robustness artifact again. A Controller may become several collaborating operations; matching counts does not demonstrate coverage. For each check below, record evidence, demonstrated findings, unresolved candidates and unavailable evidence separately.

| Rule | Operational check | Completion evidence and limits |
|---|---|---|
| **10 — Scenario realization** | Walk each specified actor action and system response against the interaction. Then inspect significant interaction behavior for an origin. | Record the corresponding messages and outcome. Word overlap locates candidates; a reviewer confirms that the behavior satisfies the step. Technical collaboration may originate in a documented design decision rather than literal use case wording. |
| **9 — Alternative and exception behavior** | For each local `(CU-ID, FA/FE-ID)`, identify the actual implementing branch or a linked interaction. | Show the guard, behavior and continuation/termination. Labels or prose saying a branch is missing are not implementation evidence. One CU's `FA-01` cannot cover another CU's `FA-01`. |
| **8 — Operation allocation** | Match classified Operation calls to the receiving classifier and inspect responsibility placement. | Trace significant operations to calls, interface/framework contracts or a justified design delta. A reply carries outputs of its original synchronous call; a Signal or lifecycle event does not automatically add an ordinary operation. Ambiguous sorts or signatures remain gaps. |
| **7 — Coherent classes** | Inspect each class's responsibility, state and collaborators. Investigate empty classes, unrelated operation groups, and wrappers with no stated role. | A coherent responsibility and justified state are required. A stateless service, interface, or adapter may be valid; counts alone identify candidates rather than prove poor design. |
| **6 — Explicit implementation collaboration** | Check that significant chosen patterns, framework contracts and infrastructure interactions appear where the selected scenario requires them. | Explain each significant effect through behavior or a declared contract. Avoid both unexplained effects and unnecessary infrastructure detail in diagrams. |
| **5 — Requirements traceability** | Traverse requirement → scenario/design decision → classes/operations → test, and inspect unexplained design elements in reverse. | Use requirement IDs and rationale. Nonfunctional requirements may be realized by architecture decisions, configuration and constraints. Missing requirements evidence leaves this check unverified; vocabulary matching is insufficient for acceptance. |
| **4 — Implementer assessment** | Obtain the implementing team's assessment of feasibility, integration constraints, performance assumptions and testability. | Record the actual participant, assessment and unresolved issues. A script or the author's self-check cannot stand in for absent implementer evidence. |
| **3 — Usable signatures** | Inspect every modeled attribute type and each operation's parameters, directions and result. | Resolve types and meaning for each individual parameter. Generic or unresolved types and names become findings only when they prevent the intended contract from being understood. Syntax checks cannot establish domain correctness. |
| **2 — Header inspection** | Generate requested or already authorized review headers, then compare them with the model. | Check members, aliases, derived properties, generic types, associations and multiplicities. Disclose any unsupported translation. Generated output is an inspection aid; human review remains necessary. See [traceability-and-headers.md](traceability-and-headers.md). |
| **1 — Test design** | Map required behaviors and specified basic/alternative/exception outcomes to `CP-XX` cases. | Controller coverage and flow coverage are separate checks. Require observable expected results; test-plan presence or a repeated ID alone does not establish coverage. |

## Reverse inspection

Inspect suspicious classes and follow their originating interactions. For example, an unexpectedly one-sided collection API may reveal an out-of-scope scenario, deliberate contract or wrongly allocated call. Confirm which explanation the artifacts support before changing either diagram. An absent inverse operation alone is not a defect.

## Findings and formal readiness

Keep proven inconsistencies separate from design-risk candidates. A formal clean result requires evidence that every applicable check was performed, including implementer and header inspection when applicable. A validator's clean preparation result can coexist with **Not fully verified** formal readiness. Record actual author and verifier identities; changing skill names does not create an independent reviewer.

Message semantics follow [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF), §17.4.3 and §17.12.18. The method's coverage, provenance and workflow checks are local MKL practices rather than additional UML conformance rules.
