<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Deriving `CP-XX` test cases

Produce sequence and tests in the **same pass**. The source extends its four steps (4069): *"we extend these steps to show how to systematically build a suite of test cases at the same time as your sequence diagrams"*.

`CP-XX` was **reserved but unowned** in the original `mkl-use-case-specifier` template. This skill uses it. Source status is inherited from upstream research.

---

## Derivation unit: Controller

The method states this three times:

> *"the nouns (Entity and Boundary objects) from the robustness diagram become object instances on the sequence diagram, and the verbs (controllers) get test cases created for them"* (1011)

> *"Boundary and entity classes on a robustness diagram will generally become object instances on a sequence diagram, while controllers will become messages. It's also advisable to create test cases for the controllers."* (2698)

> *"we systematically wrote the tests following the controllers on the sequence diagrams"* (companion book, 7276)

**Rule:** each `DR-XX` Controller yields **at least one** `CP-XX`. The behavior-allocation worklist also drives verification.

**Why not derive per message?** One Controller can span multiple operations. Test **behavior**, not the implementation structure; message-derived cases couple tests to that structure.

## Coverage check: paths

Controller coverage does **not** guarantee execution-path coverage. Check independently:

> **The basic course and every alternate/exception flow must be covered by a `CP-XX`.**

The source (5951) calls Controller-derived cases *"a bulletproof way"* to ensure alternate courses are considered.

**Uncovered path:** either a test case is missing or **its governing Controller is missing**. Route the latter to `/mkl-uml-robustness-diagram`.

## Fragment coverage criterion

UML semantics define the paths:

| Operator | Paths |
|---|---|
| `alt` | One per operand; without explicit `else`, an implicit path where no guard holds |
| `opt` | Two: executed and skipped |
| `break` | Two: taken—**replaces the remainder** of its enclosing fragment—and not taken |
| `loop(min,max)` | At least boundary values: `min` and `max` iterations |
| `par` | Relevant interleavings preserving each operand's internal order |

Linter-relevant facts: **an omitted operand guard means `true`**; `alt` chooses **at most one** operand.

**Evidence-backed scale warning.** A systematic UML-test-generation review (62 primary studies of 443, 1999-2019) reports intermediate trees/graphs and **path coverage** variants as common approaches. **Combined fragments are the hardest problem**; unrestricted all-path coverage with loops causes **test explosion**. *(Secondary confidence: indexed text, not digital-library version.)*

**Practical consequence:** cover operands, not unrestricted paths: every `alt` branch, both outcomes of `opt`/`break`, and `loop` boundaries. Declare this criterion. A modest explicit criterion is better than an unusable exhaustive one.

## `CP-XX` format

| Field | Content |
|---|---|
| `CP-XX` | Identifier |
| Originating Controller | Source `DR-XX` Controller |
| Covered path | Basic course or corresponding `FA-XX`/`FE-XX` |
| Precondition | Required execution state |
| Stimulus | Triggering message or actor action |
| Expected result | Observable behavior, not implementation |
| Traceability | `CU-XX` → `DR-XX` → `DS-XX` → `CP-XX` |

**Use observable expectations.** “The system registers entry and issues a ticket with the assigned space” is verifiable. “`save()` is called” couples the case to design and breaks on refactoring.

## Toward unit tests

The source describes the later step: collect cases in a plan and generate unit-test class/method skeletons (4638). The companion book goes further: transform robustness into sequence **and** test-case skeletons, exporting JUnit/NUnit (7299). **Design-Driven Testing** starts test preparation during analysis, well before coding.

**This skill delivers `CP-XX`, not test code.** Executable generation belongs downstream; mixing it here advances implementation decisions into a design artifact.

## Traceability note

The emitted cases complete the chain:

`RF-XX` → `CU-XX` → `FA-XX`/`FE-XX` → `DR-XX` + `B-`/`C-`/`E-` → `PDR-XX` → `DS-XX` → **`CP-XX`**

Traverse both directions: test → Controller → textual step → requirement. This fulfills design traceability under ISO/IEC/IEEE 12207 §6.4.5.2 h) and §6.4.5.3, explaining why identifiers matter.
