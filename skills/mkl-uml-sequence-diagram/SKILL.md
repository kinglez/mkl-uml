---
name: mkl-uml-sequence-diagram
description: Create, review, refactor, and validate UML sequence diagrams in PlantUML. Use to describe interactions, allocate operation calls, cover specified flows, and derive justified design and test deltas.
license: Apache-2.0
metadata:
  author: kingle.zhuang
  email: kinglezhuang@vip.qq.com
  copyright: 2026 kingle.zhuang
  organization: mkl
---
# MKL UML Sequence Diagram

## Operating contract

- Use **standalone** mode by default: complete the requested artifact from the supplied evidence. Use **MKL workflow** mode when the user requests its cross-artifact handoff or formal gate.
- Treat generate, review, refactor, and validate as operations within either mode. Preserve existing scope and authorization; do not ask again for an already authorized correction.
- Review/refactor/validate requires the target artifact. Generation requires a stated goal and enough behavior to model it; record assumptions and ask only for information that changes the result.
- Report verification coverage as **checked**, **partial**, or **blocked**, with the checks run and missing evidence. Missing upstream artifacts limit cross-artifact checks; they do not block useful standalone work. A partial check cannot establish formal acceptance.
- Preserve supplied identifiers and their mappings across renaming, reordering, splitting, and regeneration. Allocate new identifiers above the existing high-water mark; retain retired identifiers and never reuse them. If the registry is unavailable, mark new IDs provisional. Diagram aliases are separate from traceability IDs.
- Distinguish UML semantics, local MKL conventions, and heuristic findings. Run a scoped verification pass and recheck affected parts after corrections. Do not require a fixed number of clean passes or issue an assurance certificate from a validator result.

## Inputs and result

| Operation | Minimum input | Additional MKL evidence |
|---|---|---|
| Generate | Scenario behavior and participants/responsibilities | CU specification, DR diagram, domain model, PDR record with findings and transition basis |
| Review/refactor/validate | Existing sequence diagram | Specification, DR and domain for cross-artifact checks |

A standalone interaction does not require every MKL predecessor. A formal MKL handoff needs the behavior specification and its analysis/domain sources; disclose missing coverage. Respect a requested conceptual or framework-specific level of detail.

For MKL workflow work, read the PDR handoff before allocating dependent behavior. Match its scope and reviewed versions to the current inputs, and carry findings, closure evidence and remaining constraints into the design rationale. Follow the receiving-stage checks in [sequence-guidelines.md](references/sequence-guidelines.md); a missing or stale PDR limits that handoff, rather than blocking unrelated standalone work.

## Interaction workflow

1. Establish participants and the scenario boundary. Resolve existing actors, boundaries and entities, then allocate analysis controls to cohesive design responsibilities. Keep newly introduced solution classes distinct from domain discoveries.
2. Order messages from specified behavior. Distinguish synchronous operation call, asynchronous operation call, asynchronous signal, reply, creation, and destruction; arrow appearance alone may not establish the UML message sort.
3. Derive operations only from calls targeting operations. A reply carries results of an earlier call; a signal targets a Signal/reception; creation/destruction establishes lifecycle behavior. None automatically creates a same-named ordinary operation on the receiving class.
4. When asynchronous provenance matters, state the message sort or explicit operation mapping. The validators recognize `<<synchCall>>`, `<<asynchCall>>`, `<<reply>>`, `<<asynchSignal>>`, `<<createMessage>>`, and `<<deleteMessage>>` in labels. Unresolved sort remains a review limitation.
5. Express alternatives and exceptions with justified guards/fragments and clear continuation. Keep stable CU/DS/FA/FE/CP links independent of message numbering.
6. Balance activations along modeled paths, including suffixes after fragments. Loops and sampled branch combinations limit mechanical coverage; disclose those limits.

## Output and verification

Return valid PlantUML and the requested explanation. For a formal handoff, add an operation delta with receiver, signature, call/source ID, and problem/solution classification; list signals and lifecycle effects separately. Derive tests from meaningful conditions, outcomes and flows rather than every message.

This executable command runs the local MKL profile from this skill directory; paths are placeholders:

```bash
python scripts/validate_sequence_puml.py --secuencia path/to/sequence.puml --con-activaciones
```

Add `--spec path/to/spec.md`, `--robustez path/to/robustness.puml`, or `--dominio path/to/domain.puml` only when the files exist and those checks are intended. Confirm supported flags with `--help`. Report syntax/profile errors, heuristics, missing evidence and bounded path coverage separately.

## Focused references

- For message sorts, fragments and activation notation, read [notation-rules.md](references/notation-rules.md).
- For responsibility allocation, read [behavior-allocation.md](references/behavior-allocation.md).
- For a full MKL design handoff, read [sequence-guidelines.md](references/sequence-guidelines.md).
- For test derivation, read [test-derivation.md](references/test-derivation.md).
- For targeted examples or smells, consult [regression-examples.md](references/regression-examples.md) or [anti-patterns.md](references/anti-patterns.md); consult [sources-and-methods.md](references/sources-and-methods.md) for attribution.
