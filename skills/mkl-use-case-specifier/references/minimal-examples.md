<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Minimal Examples

## Example 1: specify one bounded goal

**User input**

> Specify CU-03 Register support request. System: Support Portal. Domain model: Customer, Support Request, Category, Priority, Agent. Rules: RN-01 a request must have a category; RN-02 high priority requires a description.

**Expected behavior**

- Start with the summary form: actor, goal, trigger, preconditions, basic flow, relevant alternatives, postconditions, rules and acceptance criteria.
- Use document control and the full template only when complexity or a requested formal handoff warrants them; missing prototypes do not require inventing a document bundle.
- Write the main flow as actor/system steps.
- Keep RN-01 and RN-02 in the business rules section.
- Create acceptance criteria for the main, alternate, and exception flows.
- Record pending decisions when prototypes or nonfunctional requirements are missing.

## Example 2: review an existing specification

**User input**

> Review this use case: “The user enters the system, fills in data, it is saved in the database, and a message is displayed.”

**Expected behavior**

- Flag ambiguities: “user,” “data,” “it is saved,” and “message.”
- Separate internal persistence details.
- Ask for, or infer with explicit assumptions, the primary actor, functional object, and observable result.
- Propose a corrected name, such as `Register service request`.
- Rewrite the steps as verifiable actor and system actions.

## Example 3: prepare MKL outputs

**User input**

> From the Validate reservation use case, identify the inputs for robustness and sequence modeling.

**Expected behavior**

- Identify candidate boundary objects from interfaces or interaction points.
- Identify candidate entity objects from domain-model concepts.
- Identify candidate control objects only as flow coordinators, without turning them into requirements.
- Derive sequence messages from flow steps, preserving alternate conditions and exceptions.
