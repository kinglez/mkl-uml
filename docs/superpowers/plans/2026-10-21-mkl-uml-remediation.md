# MKL UML Remediation Implementation Plan

> For agentic workers: implement the authorized remediation in sequence; preserve scope and verify observable behavior. Use focused independent workers only for disjoint files.

**Goal:** Correct the audited modeling and validator defects, then make the suite reliably testable, usable independently, and distributable.

**Architecture:** Retain the eight existing skills and standalone Python validators. Distinguish UML semantics, MKL workflow conventions, and heuristic warnings. Default to scoped standalone assistance; use the formal MKL review workflow when requested.

**Tech Stack:** Markdown/YAML, standard-library Python, unittest, PlantUML for syntax verification.

**Spec:** The 17-item review and the user's instruction to implement semantic/validator fixes, assertion tests, operating/ID contracts, then entrypoint/distribution improvements in that order.

## Global constraints

- English instructions; MKL/mkl branding; author kingle.zhuang, email kinglezhuang@vip.qq.com, organization mkl, copyright 2026.
- Use the current mkl-prefixed skill names; preserve existing user artifacts, legacy CLI flags and supported Spanish input vocabulary.
- Retain upstream copyright and license notices. Work in mkl-uml only; the upstream directory remains unchanged.
- No installation into personal application configuration. Test installed payloads in temporary directories.
- Never treat self-review counts or heuristic checks as proof of semantic correctness.

## Review focus

- Reply/signal/create/delete messages must not create spurious receiving-class operations.
- Supporting actors and machine interfaces must remain representable without invented screens.
- Path caps must retain suffix events; empty/markerless inputs and alias relations require explicit regression tests.
- Existing CU/DR/DS/CP identifiers must survive declaration reorder and partial regeneration.
- Archive and directory installation must contain identical self-contained resources, notices, and working local links.

## Tasks

- [x] 1. Reproduce and fix the three validator defects with failing-then-passing unittest cases. Correct message-kind, actor-association, and vocabulary-closure instructions and references.
- [x] 2. Establish persistent assertion tests for representative valid/invalid fixtures, important diagnostics, the repaired parser cases, and complete pipeline handoffs. Add them to CI alongside smoke and structure checks; verify a no-op-validator mutation is detected.
- [x] 3. Unify standalone versus MKL modes, per-operation required inputs, partial-review statuses, typed vocabulary origins, stable identifier lifecycle, and existing authorization handling. Correct boundary, derived-property, composition, and normative-versus-local-policy inconsistencies.
- [x] 4. Shorten entrypoints while retaining usable contracts and routing detailed method guidance into references. Replace unconditional repeated audit ceremonies with scoped verification and optional formal review.
- [x] 5. Share payload construction between archive packaging and directory installation; preserve notices, make references/local documentation work after installation, and test a temporary installed copy.
- [x] 6. Run all assertion tests, existing smoke checks, metadata validation, all PlantUML fixtures, plugin validation, independent behavioral review, and archive integrity checks. Rebuild the eight distributions and update the validation record with actual limits.

## Completion evidence

Record actual test results, changed behavior and limitations in docs/VALIDATION.md. Keep regression tests in the repository rather than relying on temporary parity scripts. Do not claim complete semantic verification of the UML language.
