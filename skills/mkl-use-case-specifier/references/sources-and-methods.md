<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sources and Methods — mkl-use-case-specifier

The foundation for this skill's rules. Content is paraphrased and attributed rather than transcribed. Cite sources concisely only when the user requests justification.

## Sources

- **Fowler, M. (2004). *UML Distilled* (3rd ed.). Addison-Wesley.** The technique's value lies in use case *text*, rather than the diagram; goal levels (Cockburn: user/sea, subfunction/fish, summary/kite).
- **Rosenberg, D., & Stephens, M. (2007). *Use Case Driven Object Modeling with UML*. Apress.** Write use cases in the context of the domain model; the two-paragraph rule; event/response style; naming boundary classes in the text; the Eight Steps; fitting the complete use case into one sequence diagram.
- **Rosenberg, D., Stephens, M., & Collins-Cope, M. (2005). *Agile Development [abbreviated title]*. Apress.** Minimalism: avoid spending time on lengthy, elaborate templates; use two paragraphs (sunny-day + rainy-day), active voice, and present tense.
- **Wiegers, K., & Beatty, J. (2013). *Software Requirements* (3rd ed.). Microsoft Press.** Flow anatomy and labeling; functional-requirement derivation; use case traps; quality attributes; traceability; test derivation.

## The Eight Steps for a Better Use Case (Rosenberg & Stephens)

Review/audit checklist for the text:

1. Remove out-of-scope content without importing another use case's steps.
2. Change passive voice to active voice and present tense.
3. Replace overly abstract wording with concrete action/response pairs.
4. Reflect the actual interaction interface accurately, including GUI and machine interfaces, without inventing or omitting real interactions.
5. **Name participating domain and boundary objects.**
6. Verify that **all alternate courses** are present; their complete absence is a warning sign.
7. **Trace every requirement** to its use cases.
8. Ensure each use case describes **what the user is trying to accomplish**.

## Two-paragraph rule and event/response style

- A use case consists of two paragraphs: **BASIC COURSE** (basic/sunny-day course) and **ALTERNATE COURSES** (alternate/rainy-day courses). If it cannot fit into two paragraphs, it probably represents two use cases.
- Operational criterion: the complete use case should fit into **one** sequence diagram; longer text leads to unmanageable sequences.
- Style: *user action → system response* pairs, active voice, present tense. Use the **noun-verb-noun** pattern: noun (object) – verb (message) – noun (object), which later appears as sequence-diagram messages.
- **Refer to boundary classes by name** (“the Payment page,” rather than “a page”). This links use case text ↔ robustness diagram ↔ class diagram ↔ code. A control lacking behavioral support in the text is a candidate “rogue controller”; check the supporting verb/responsibility and clarify the text when needed. A control name need not be a domain noun.

## Common textual mistakes (Rosenberg's exercises)

Unnamed boundary objects; a vague basic course trying to cover every case simultaneously; alternate courses that are not anchored to a specific textual step; superfluous preconditions hiding the real initial action; excessive presentation detail, such as treating form fields as steps rather than domain attributes; terminology inconsistent with the domain model; and a complete absence of alternate courses.

## Flow anatomy and traps (Wiegers)

- **Anatomy:** trigger → precondition verification → numbered normal flow (actor–system dialogue) → postconditions. Alternate flows branch from the normal flow and may rejoin it; exceptions prevent achievement of the postcondition.
- **Labels:** normal flow `4.0`, alternate flow `4.1`, exception from the normal flow `4.0.E1`.
- **Staying in bounds:** postconditions hold at the end of the normal flow; additional steps are unnecessary.
- **Traps:** too many use cases, often indicating the wrong abstraction level; flows exceeding about 10–15 steps, requiring confirmation that they describe one scenario; introducing design/data details (“the System presents options,” rather than “displays a dropdown”; data definitions belong in the data dictionary); **forcing every requirement** into a use case, although use cases reveal most requirements rather than all of them.
- **Quality attributes per requirement:** complete, correct, feasible, necessary, prioritized, unambiguous, and **verifiable**. Without verifiability, implementation correctness becomes a matter of opinion rather than objective analysis.

## From use cases to functional requirements (Wiegers)

Developers implement **functional requirements**, rather than use cases. Derive functional requirements (RF) in an EARS-like form: *“[optional precondition] [optional triggering event] the system shall [expected response]”*, one per relevant step/rule, and trace them. Three documentation strategies are available: requirements embedded in the use case; a simple use case with separately traced requirements; or functional requirements alone in the SRS.

## Traceability and test derivation (Wiegers)

- Give each item a **unique, persistent label**. Use a many-to-many use case × requirement traceability matrix. When a use case changes, review linked functional requirements as potentially suspect links.
- **Derive tests from flows:** cover basic, alternate, and exception courses. Complete, precise, clear use cases make test derivation straightforward.
- **Given/When/Then from flows:** Given = preconditions; When = action/step; Then = consequence/postcondition. Trace each test to its requirement/use case.

## Construction pipeline: inputs → specification → downstream artifacts

`verbal model` → **domain model** (/mkl-uml-domain-modeler) → **use case diagram** (/mkl-uml-use-case-diagram) → **SPECIFICATION** → robustness → sequence → tests.

- The **domain model** supplies vocabulary, the nouns in the text; the **diagram** supplies actors, relationships, and scope; the **verbal model** supplies behavior.
- **Backward traceability:** domain concepts trace to the domain model or a disclosed discovery delta; actor-role names trace to external participation evidence (and the actor diagram when supplied); boundary/interface names trace to named interaction/interface evidence (screens, APIs, webhooks, message ingress, or device adapters). Flow behavior traces to supplied requirements/scenario evidence. These distinct origins are not an all-nouns-in-domain rule. Missing optional upstream artifacts limit cross-artifact checks rather than block an independently scoped specification.

## Stable identifiers

Preserve existing document, use-case, requirement, rule, flow, element, and trace mappings when identity is unchanged. Allocate a new ID only for a new identity. Mark deleted identities retired; never silently reuse their IDs. Record renames as aliases/changes to the same identity, and update references consistently. Check that every referenced ID resolves to an existing item or an explicit retired/replacement record. Prefixes describe the artifact type; they do not require inventing missing upstream artifacts for standalone work.
