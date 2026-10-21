<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Use Case Specification Review Rubric

Use this rubric to review, complete, or refactor use case specifications. Classify findings as critical, major, or minor.

## Severity

| Severity | Criterion | Examples |
|---|---|---|
| Critical | Prevents understanding, validation, or derivation of functional behavior. | Internal primary actor; use case without a goal; incomplete main flow; missing system boundary; contradictory rules. |
| Major | Reduces verifiability, traceability, or methodological consistency. | Unverifiable preconditions; alternate flows mixed with exceptions; rules embedded in the flow; missing acceptance criteria. |
| Minor | Affects clarity, style, or maintainability. | Vague names; passive voice; inconsistent terms; excessive interface detail. |

## Quality checklist

| Dimension | Review question | Expected result |
|---|---|---|
| Goal | Does the use case have one observable functional goal? | One actor goal, rather than a technical task or UI step. |
| Name | Does the name start with an infinitive verb and functional object? | `Register request`, `Check status`, `Approve order`. |
| Actors | Are actors external to the system under analysis? | People, external systems, external devices, or external organizational roles. |
| System boundary | Is system behavior distinguished from external actor behavior? | A clear actor/system flow with separate responsibilities. |
| Domain | Do the concepts match the domain model? | Official terminology without ambiguous synonyms. |
| Main flow | Does it describe a complete, verifiable successful scenario? | Ordered steps from trigger to observable result. |
| Alternate flows | Do they represent valid business variations? | Valid conditions, return/termination, and associated rules. |
| Exceptions | Do they represent errors or unexpected events? | Cause, system response, message, final state, and recovery. |
| Rules | Are business rules separate from the flow? | Rules identified by ID and referenced from steps/flows. |
| Special requirements | Do security, performance, audit, privacy, and availability have measurable criteria? | Verifiable thresholds, evidence, or standards. |
| Traceability | Is the use case linked to RF, RN, CP, the domain, robustness, and sequence? | Clear, consistent references. |
| MKL | Does the specification support robustness and sequence derivation? | Candidate boundary/entity/control objects and messages derived from steps. |
| Ambiguity | Are vague terms avoided? | Qualify “information,” “data,” “screen,” and “processes” with a specific object. |
| Implementation | Is internal design excluded? | No tables, controllers, SQL, frameworks, or software classes. |

## Quick diagnostic rules

- If a use case can be named as an internal technical action, it is probably not a user use case.
- If the flow does not end in an observable state, its postcondition is incomplete.
- A step saying “validates the data” without an object or rule is ambiguous.
- If a rule is written as a flow step, move it to business rules and retain an ID reference.
- An alternate flow that neither returns nor terminates is incomplete.
- If an acceptance criterion cannot be tested, rewrite it as Given/When/Then.
