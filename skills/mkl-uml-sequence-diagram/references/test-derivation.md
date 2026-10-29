<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Deriving `CP-XX` test cases

Derive test design while allocating sequence behavior. This original method guidance is informed by Rosenberg & Stephens (2007), chapters 8, 9 and 12, and Rosenberg, Stephens & Collins-Cope (2005), model-driven testing discussions. Historical source status is recorded in [sources-and-methods.md](sources-and-methods.md).

## Behavior and flow coverage

Where supplied, use each robustness Controller as an index of behavior needing at least one test. A Controller can span multiple operations; avoid generating one business test for every implementation message. For standalone work, derive equivalent behavior cases from the supplied scenario and state the unavailable robustness link.

Check flow coverage separately: the basic flow and every specified local `(CU-ID, FA/FE-ID)` need a test with an observable outcome. A Controller coverage match does not establish that every outcome or branch was tested.

## Combined fragments

| Fragment | Practical test selection |
|---|---|
| `alt` | Cover each feasible operand, including a no-guard-match path when applicable. |
| `opt` | Cover taking and skipping the optional behavior. |
| `break` | Cover taking the break and continuing without it. |
| `loop` | Cover relevant lower/upper boundaries, including zero iterations when permitted. |
| `par` | Select relevant interleavings that preserve each operand's internal ordering. |

UML permits an omitted guard to mean true, and an `alt` selects at most one operand. Distinguish operator semantics from the chosen coverage criterion. Feasibility, dependencies and unbounded loops can prevent exhaustive path coverage. State the bounded criterion actually used rather than promise all possible paths. Research on UML test generation is supporting context, with the inherited secondary-confidence limitations in the source record.

## Case record

| Field | Content |
|---|---|
| Identifier | Stable `CP-XX`. |
| Origin | Required behavior, Controller or contract. |
| Scenario/flow | `CU-XX` and local basic/`FA-XX`/`FE-XX` path. |
| Preconditions | Relevant starting state. |
| Stimulus | Actor action, incoming call or event. |
| Expected result | Observable output and state change, including rejection/termination. |
| Trace links | Available requirements, robustness and sequence IDs. |

Prefer an expectation such as receiving an assigned space and ticket over a bare assertion that an internal `save()` method was called. Trace tests back to behavior and requirements in both directions. Missing behavior may require a requirements/robustness correction rather than an invented test.

This skill delivers test-design records, not executable unit tests. Generating language-specific test skeletons belongs to separately authorized implementation work. ISO/IEC/IEEE 12207:2017 §6.4.5 provides traceability context; the precise local ID chain is an MKL convention.
