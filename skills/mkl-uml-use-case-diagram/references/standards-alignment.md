# Standards Alignment for UML Use Case Diagram Skill

Use this file when the user asks whether the skill is standards-informed or when a review requires methodological justification.

## Standards used as engineering guidance

This skill is not a certification tool. It uses the following standards and specifications as quality references:

- **OMG UML 2.5.1**: use for notation, UML diagram semantics, actor/use case relations, system boundary, include, extend, and generalization.
- **ISO/IEC/IEEE 29148**: use for requirements quality: stakeholder relevance, traceability, verifiability, clarity, and requirements information structure.
- **ISO/IEC/IEEE 15289**: use for lifecycle information item discipline: consistent artifacts, purpose, content, and relationship among information items.
- **ISO/IEC/IEEE 42010**: use for viewpoint separation: stakeholders, concerns, views, system boundary, and avoiding architecture-detail leakage into functional diagrams.
- **ISO/IEC 25010**: use to evaluate the generated diagram/skill output as a quality artifact: functional suitability, usability, maintainability, compatibility, and reliability.
- **ISO/IEC/IEEE 29119**: use for validation mindset, regression examples, review evidence, and testability of generated outputs.

### Verification status of these references

The ISO/IEEE standards listed here are cited **by purpose, not by clause number**: their primary texts were not verified in this skill's corpus. UML actor/association semantics were checked against [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) §18.1.3–18.1.4 during this correction; the other purposes remain guidance, not conformance evidence. Treat the list as a statement of which quality concerns shaped the skill, not as evidence of conformance.

Two consequences worth stating plainly:

- **ISO/IEC/IEEE 15289 is not in the corpus.** It is invoked here for information-item discipline in general terms. If you need a citable requirement for what a *review record* must contain, use **IEEE Std 1028-2008 §6.7** instead — that clause was read against primary text (see the `mkl-pdr-review` sibling skill, `references/sources-and-methods.md`).
- **Before citing any of these in an academic or contractual deliverable, check the clause in the official text.** A verified citation is worth more than three plausible ones.

## Practical interpretation

Map standard ideas into actionable checks:

| Source | Skill behavior |
|---|---|
| OMG UML | Produce valid use case notation and avoid class/activity/sequence semantics inside use case diagrams. |
| ISO/IEC/IEEE 29148 | Ensure each use case candidate is traceable, stakeholder-relevant, clear, and testable. |
| ISO/IEC/IEEE 15289 | Keep artifacts coherent: domain model, use case diagram, textual use case specification, and later diagrams have distinct purposes. |
| ISO/IEC/IEEE 42010 | Separate viewpoints: functional concerns go in use case diagrams; workflow and architecture concerns go elsewhere. |
| ISO/IEC 25010 | Evaluate output quality: correct, useful, readable, maintainable, and reusable across domains. |
| ISO/IEC/IEEE 29119 | Use validators and regression examples to catch recurrent defects; do not rely only on intuition. |

## Key standards-informed rules

1. A use case must represent an externally observable actor goal or system service.
2. A candidate must be traceable to the verbal model or clearly inferable from it.
3. Domain Model classes are vocabulary, not automatic actors or use cases.
4. Use case diagrams must not become workflow, sequence, architecture, database, or UI diagrams.
5. Include/extend must express UML semantics, not temporal order.
6. Access/login is a use case only when authentication/session behavior is part of the requirements.
7. Outputs such as notifications or confirmations are not actor-initiated merely because actors receive them. An actor association can nevertheless represent supporting participation through data/signal exchange; it does not specify who initiates.
8. Internal validations, calculations, state updates, and generated identifiers usually belong in textual specifications or postconditions.

## Evidence-informed rationale

Empirical literature on use cases repeatedly reports practical issues around scenario granularity, inconsistent formats, and insufficient analysis guidance. The skill therefore emphasizes quality gates, traceability, dominant-use-case detection, and regression examples to reduce those risks.

## Practitioner sources (books)

Beyond the standards above, this skill is grounded in the practitioner literature on use cases. Cite concisely, only when the user asks for justification.

- **Fowler, M. (2004). *UML Distilled* (3rd ed.). Addison-Wesley.** Supports treating the diagram as an index of goals and the textual specification as the behavioral substance; includes human/non-human and primary/supporting actor distinctions.
- **Rosenberg, D., & Stephens, M. (2007). *Use Case Driven Object Modeling with UML: Theory and Practice*. Apress.** Informs domain-context vocabulary, event/response writing, basic/alternative behavior and restrained relationship use.
- **Rosenberg, D., Stephens, M., & Collins-Cope, M. (2005). *Agile Development with ICONIX Process: People, Process, and Pragmatism*. Apress.** Informs concise use cases and proportional documentation effort.
- **Wiegers, K., & Beatty, J. (2013). *Software Requirements* (3rd ed.). Microsoft Press.** Supplies actor/trigger/precondition/postcondition/flow context and requirements/testability guidance. Associations do not encode workflow order.
- **Cockburn, A. *Writing Effective Use Cases*.** Supplies goal-level vocabulary: user goal, subfunction and summary. Record the chosen level in text when useful.

Practical mapping: keep the diagram a lightweight summary of actor goals; put substance in the textual specifications; default to no include/extend; aim at user-goal level; name use cases in active voice with domain-model nouns.
