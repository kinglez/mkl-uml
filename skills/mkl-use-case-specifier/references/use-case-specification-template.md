<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Use Case Specification Template

## 1. Document control

| Field | Value |
|---|---|
| Project name | [Project name] |
| System name | [System name] |
| Document ID | [DOC-CU-XX] |
| Version | [Version] |
| Author | [Author name] |
| Creation date | [YYYY-MM-DD] |
| Last updated | [YYYY-MM-DD] |
| Status | [Draft / In review / Approved / Obsolete] |

### Change history

| Version | Date | Author | Change |
|---|---|---|---|
| [0.1] | [YYYY-MM-DD] | [Name] | [Change description] |
| [0.2] | [YYYY-MM-DD] | [Name] | [Change description] |

---

## 2. Expected inputs for applying this template to a real case

| Input | Description | Status | Notes |
|---|---|---|---|
| System verbal model | Narrative description of the problem, actors, needs, and expected behavior. | [Available / Unavailable] | [Reference or location] |
| Domain model | Conceptual glossary of domain classes/concepts and relationships. | [Available / Unavailable] | [Text / Image / PlantUML / Other] |
| Use case model or diagram | Representation of actors, use cases, and UML relationships. | [Available / Unavailable] | [Text / Image / PlantUML / Other] |
| Selected use case | ID and name of the use case to specify. | [Available / Unavailable] | [CU-XX - Name] |
| Primary actor | External actor initiating or pursuing the functional goal. | [Available / Unavailable] | [Exact actor name] |
| Known business rules | Domain policies, constraints, or conditions. | [Available / Unavailable] | [RN-XX] |
| Prototypes, screens, or GUI | Interfaces, forms, pages, storyboards, or endpoints visible to the actor. | [Available / Unavailable] | [Interface name] |
| Associated functional requirements | Requirements satisfied by this use case. | [Available / Unavailable] | [RF-XX] |
| Special requirements | Security, performance, usability, audit, availability, privacy, etc. | [Available / Unavailable] | [RE-XX] |
| Constraints | Legal, organizational, technical, or regulatory conditions. | [Available / Unavailable] | [Description] |

---

## 3. Use case identification

| Field | Value |
|---|---|
| ID | [CU-XX] |
| Name | [Infinitive verb + functional object] |
| Functional package | [Functional package or module name] |
| Abstraction level | [Business / User / Subfunction] |
| Primary actor | [Primary Actor] |
| Priority | [High / Medium / Low] |
| Frequency of use | [High / Medium / Low / Occasional] |
| Criticality | [High / Medium / Low] |
| Status | [Proposed / Validated / Approved / In review] |

---

## 4. Purpose

| Field | Description |
|---|---|
| Goal | [What the primary actor seeks to accomplish through this use case] |
| Brief description | [Functional summary of the use case] |
| Functional or business value | [Observable benefit for the actor, organization, or process] |
| Observable result | [State or result confirming achievement of the goal] |

---

## 5. Actors

| Type | Actor | Description | Participation |
|---|---|---|---|
| Primary actor | [Primary Actor] | [External role initiating or directly benefiting from the use case] | [Main action] |
| Secondary actor | [Secondary Actor] | [Supporting external role] | [Service or interaction] |
| External system | [External System] | [System interacting with the system under analysis] | [Validate / Query / Notify / Authorize / Other] |
| External device | [Device] | [Sensor, reader, terminal, or another external device] | [Functional input or output] |
| Related stakeholder | [Stakeholder] | [Interested party who may not interact directly with the system] | [Interest or impact] |

---

## 6. Scope and context

| Field | Value |
|---|---|
| Functional scope | [Functional goal covered by this use case] |
| System boundary | [What belongs to the system and what remains outside it] |
| Includes | [Functionality covered by this use case] |
| Excludes | [Functionality outside this use case] |
| Assumptions | [Assumptions needed to interpret the use case correctly] |

---

## 7. Domain model involvement

| Domain concept/class | Description | Participation in the use case | Relevant attributes | Important relationships |
|---|---|---|---|---|
| [Concept 1] | [Brief definition] | [How it participates in the use case] | [Attributes that improve clarity] | [Conceptual relationship] |
| [Concept 2] | [Brief definition] | [How it participates in the use case] | [Attributes that improve clarity] | [Conceptual relationship] |
| [Concept 3] | [Brief definition] | [How it participates in the use case] | [Attributes that improve clarity] | [Conceptual relationship] |

### Terminology control

| Official term | Meaning | Synonyms or prohibited terms | Note |
|---|---|---|---|
| [Domain Model term] | [Definition] | [Ambiguous terms to avoid] | [Correct usage] |
| [Domain Model term] | [Definition] | [Ambiguous terms to avoid] | [Correct usage] |

---

## 8. Relationships with other use cases

| Relationship type | Related use case | Direction | Justification |
|---|---|---|---|
| `<<include>>` | [CU-XX - Name] | [This use case includes / Is included by] | [Mandatory reusable behavior] |
| `<<extend>>` | [CU-XX - Name] | [This use case extends / Is extended by] | [Optional or conditional behavior] |
| Generalization | [CU-XX - Name] | [General / Specialized] | [Functional inheritance or specialization] |
| Functional dependency | [CU-XX - Name] | [Depends on / Is required by] | [Reason] |

---

## 9. Preconditions

| ID | Precondition | Type | Verifiable |
|---|---|---|---|
| PRE-01 | [Required prior state] | [Functional / Business / Authorization / Data] | [Yes / No] |
| PRE-02 | [Required prior state] | [Functional / Business / Authorization / Data] | [Yes / No] |

---

## 10. Trigger

| Field | Value |
|---|---|
| Initial event | [Event initiating the use case] |
| Generated by | [Actor / External system / Time / Business event] |
| Observable initial condition | [Condition by which the start of the use case can be recognized] |

---

## 11. Basic flow / main flow / sunny-day scenario

| Step | Responsible party | Active-voice action | Domain concept involved | System response / result | Interface or interaction point |
|---:|---|---|---|---|---|
| 1 | System | Displays the [Interface name] interface | [Concept] | [Visible result] | [Interface] |
| 2 | [Primary Actor] | [Enters / Selects / Requests / Confirms] [specific object] | [Concept] | [Observable result] | [Interface] |
| 3 | System | Validates [specific object/concept] | [Concept] | [Validation result] | [Interface] |
| 4 | System | [Queries / Registers / Updates / Calculates / Generates] [specific concept] | [Concept] | [Verifiable change or output] | [Interface] |
| 5 | System | Displays [specific result] | [Concept] | [Confirmation visible to the actor] | [Interface] |

---

## 12. Alternate flows

| ID | Name | Starting point | Activating condition | Expected result | Return or termination | Related rules |
|---|---|---|---|---|---|---|
| FA-01 | [Alternate flow name] | Step [N] | [Valid condition] | [Expected result] | [Returns to step N / Ends] | [RN-XX] |
| FA-02 | [Alternate flow name] | Step [N] | [Valid condition] | [Expected result] | [Returns to step N / Ends] | [RN-XX] |

### Alternate flow FA-01 detail

| Step | Responsible party | Action | Domain concept | Result |
|---:|---|---|---|---|
| FA-01.1 | [Actor/System] | [Specific action] | [Concept] | [Verifiable result] |
| FA-01.2 | [Actor/System] | [Specific action] | [Concept] | [Verifiable result] |

### Alternate flow FA-02 detail

| Step | Responsible party | Action | Domain concept | Result |
|---:|---|---|---|---|
| FA-02.1 | [Actor/System] | [Specific action] | [Concept] | [Verifiable result] |
| FA-02.2 | [Actor/System] | [Specific action] | [Concept] | [Verifiable result] |

---

## 13. Exception flows

| ID | Error or unexpected event | Occurrence point | Cause | System response | Displayed message | Final state | Possible recovery |
|---|---|---|---|---|---|---|---|
| FE-01 | [Error or unexpected event] | Step [N] | [Cause] | [System action] | “[Specific message]” | [Final state] | [Yes / No / How] |
| FE-02 | [Error or unexpected event] | Step [N] | [Cause] | [System action] | “[Specific message]” | [Final state] | [Yes / No / How] |

---

## 14. Postconditions

| Type | Postcondition | Verification |
|---|---|---|
| Success | [Successful final system state] | [How to verify] |
| Failure | [Final state when the use case does not complete] | [How to verify] |
| Data created | [Concepts/data created] | [Evidence] |
| Data queried | [Concepts/data queried] | [Evidence] |
| Data modified | [Concepts/data modified] | [Evidence] |
| Data deleted | [Concepts/data deleted] | [Evidence] |
| State changes | [Previous state → New state] | [Evidence] |
| Visible effects | [Result observed by the actor] | [Interface, notification, or output] |

---

## 15. Business rules

| ID | Business rule | Type | Affected use cases | Applicable step/flow | Source or justification |
|---|---|---|---|---|---|
| RN-01 | [Rule description] | [Validation / Policy / Constraint / Calculation / Authorization] | [CU-XX] | [Step or flow] | [Source] |
| RN-02 | [Rule description] | [Validation / Policy / Constraint / Calculation / Authorization] | [CU-XX] | [Step or flow] | [Source] |

---

## 16. Special requirements

| ID | Category | Requirement | Verifiable criterion |
|---|---|---|---|
| RE-01 | Security | [Security requirement] | [How to verify] |
| RE-02 | Performance | [Response time, concurrency, capacity, etc.] | [Metric or threshold] |
| RE-03 | Usability | [Ease-of-use condition] | [Criterion] |
| RE-04 | Availability | [Operating condition] | [Metric] |
| RE-05 | Accessibility | [Accessibility criterion] | [Standard or evidence] |
| RE-06 | Audit | [Event to record] | [Evidence] |
| RE-07 | Privacy | [Personal data handling] | [Criterion] |
| RE-08 | Compatibility | [Device, browser, external system, environment] | [Criterion] |
| RE-09 | Legal/regulatory | [Regulatory constraint] | [Criterion] |

---

## 17. Prototypes, GUI, or interface references

| Element | Explicit name | Purpose | Main fields | Available actions | Relevant messages | Related steps |
|---|---|---|---|---|---|---|
| Interface | [Interface name] | [Purpose] | [Field 1, Field 2] | [Button/action] | [Message] | [Steps] |
| Page | [Page name] | [Purpose] | [Fields] | [Actions] | [Messages] | [Steps] |
| Form | [Form name] | [Purpose] | [Fields] | [Actions] | [Messages] | [Steps] |
| Visible endpoint | [Functional endpoint name] | [Purpose] | [Functional parameters] | [Action] | [Response] | [Steps] |

---

## 18. Manipulated data and objects

| Domain concept | Data used | Functional operation | Related step/flow | Constraints |
|---|---|---|---|---|
| [Concept] | [Specific data item] | [Create / Query / Update / Delete / Validate / Calculate / Select / Confirm / Cancel] | [Step or flow] | [Constraint] |
| [Concept] | [Specific data item] | [Create / Query / Update / Delete / Validate / Calculate / Select / Confirm / Cancel] | [Step or flow] | [Constraint] |

---

## 19. Traceability

| Item type | Reference | Relationship to the use case |
|---|---|---|
| Functional requirement | [RF-XX] | [This use case fully/partially satisfies the requirement] |
| Business objective | [OBJ-XX] | [Contribution] |
| Business rule | [RN-XX] | [Application] |
| Test case | [CP-XX] | [Validated scenario] |
| Domain model | [Concepts] | [Concepts used] |
| Use case diagram | [CU-XX] | [Relationship] |
| Robustness diagram | [DR-XX] | [Pending / Derived] |
| Sequence diagram | [DS-XX] | [Pending / Derived] |
| RUP iteration/sprint/phase | [Name] | [Planning] |
| Acceptance criterion | [CA-XX] | [Validation] |

---

## 20. Acceptance criteria

| ID | Criterion | Associated flow | Expected evidence |
|---|---|---|---|
| CA-01 | Given [context], when [actor performs action], then [verifiable result]. | Basic flow | [Evidence] |
| CA-02 | Given [alternate context], when [event], then [verifiable result]. | FA-01 | [Evidence] |
| CA-03 | Given [error condition], when [event], then [verifiable system response]. | FE-01 | [Evidence] |

---

## 21. Risks, ambiguities, and pending decisions

| ID | Type | Description | Impact | Owner | Decision taken | Date | Status |
|---|---|---|---|---|---|---|---|
| RA-01 | Ambiguity | [Ambiguous concept, flow, or rule] | [Impact] | [Owner] | [Decision] | [YYYY-MM-DD] | [Open / Closed] |
| RA-02 | Risk | [Functional or methodological risk] | [Impact] | [Owner] | [Mitigation] | [YYYY-MM-DD] | [Open / Closed] |
| RA-03 | Pending decision | [Decision needed] | [Impact] | [Owner] | [Decision] | [YYYY-MM-DD] | [Open / Closed] |

---

## 22. Methodological review checklist

| Criterion | Meets criterion | Notes |
|---|---:|---|
| The use case has a single functional goal. | [Yes/No] | [Note] |
| The name starts with an infinitive verb. | [Yes/No] | [Note] |
| The primary actor is identified. | [Yes/No] | [Note] |
| Actors are external to the system. | [Yes/No] | [Note] |
| The main flow represents a complete successful scenario. | [Yes/No] | [Note] |
| Sufficient alternate flows are present. | [Yes/No] | [Note] |
| Relevant exception flows are present. | [Yes/No] | [Note] |
| Domain Model terminology is used. | [Yes/No] | [Note] |
| Ambiguous synonyms are absent. | [Yes/No] | [Note] |
| Interfaces are explicitly named. | [Yes/No] | [Note] |
| Business rules are separate from the textual flow. | [Yes/No] | [Note] |
| Special requirements are separate from the functional flow. | [Yes/No] | [Note] |
| Postconditions are verifiable. | [Yes/No] | [Note] |
| Implementation details are absent. | [Yes/No] | [Note] |
| Functional requirements are traceable. | [Yes/No] | [Note] |
| Business rules are traceable. | [Yes/No] | [Note] |
| Test cases are traceable. | [Yes/No] | [Note] |
| The use case can support robustness analysis. | [Yes/No] | [Note] |
| The use case can support a sequence diagram. | [Yes/No] | [Note] |
| Users, analysts, and developers can understand the document. | [Yes/No] | [Note] |

---

## 23. Summary form for simple use cases

### [CU-XX] [Use Case Name]

| Field | Value |
|---|---|
| Primary actor | [Actor] |
| Goal | [Functional goal] |
| Trigger | [Initial event] |
| Preconditions | [Necessary prior conditions] |
| Domain concepts | [Main concepts] |
| Basic flow | 1. [Step 1] 2. [Step 2] 3. [Step 3] |
| Alternate flows | [FA-01: brief description] |
| Exception flows | [FE-01: brief description] |
| Success postcondition | [Final state] |
| Business rules | [RN-XX] |
| Acceptance criteria | [CA-XX] |
| Related use cases | [CU-XX] |

---

## 24. Writing rules for completing the template

| Rule | Application |
|---|---|
| Use active voice | “[Actor/System] performs [action] on [object].” |
| Use present tense | “The System validates...,” “The Customer selects....” |
| Name interfaces explicitly | “The System displays the [Interface name] interface.” |
| Avoid ambiguity | Qualify terms such as “information,” “data,” and “screen.” |
| Avoid implementation details | Exclude tables, code, frameworks, design classes, and internal controllers. |
| Separate business rules | Put rules in section 15 rather than mixing them into the textual flow. |
| Maintain traceability | Each important flow must be relatable to requirements, rules, or tests. |
| Use Domain Model terms | Preserve official concepts rather than replacing them with ambiguous synonyms. |
