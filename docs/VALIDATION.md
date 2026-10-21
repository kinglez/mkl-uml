<!-- Copyright 2026 kingle.zhuang. Organization: mkl. -->
# Validation record

Validation date: **2026-10-21**. Local environment: macOS, Python **3.14.7**, PlantUML **1.2026.7**, and the installed Claude Code CLI. Author: **kingle.zhuang**, <kinglezhuang@vip.qq.com>, organization **mkl**.

## Executed checks

| Check | Observed result |
|---|---|
| Persistent assertion suite | **147 tests passed** |
| Original fixture behavior contracts | All **85** scenarios have literal expected exit codes and important diagnostic assertions |
| Full pipeline handoffs | All **8** validators exercised against the shared coherent pipeline fixture |
| Original smoke suite | **85/85** execute without crashes or unexpected statuses; deliberately invalid fixtures retain their expected findings |
| Validator mutation | Replacing all eight validators with `raise SystemExit(0)` in a temporary copy causes **98 failures in 100 contract tests**, exit 1 |
| Skill metadata | **8/8** pass Skill Creator `quick_validate.py` |
| PlantUML syntax | **210/210** repository files pass: 205 original skill examples plus 5 pipeline fixtures |
| Python compilation | All **20** Python sources compile; Node CLI syntax check passes |
| Plugin manifest | `claude plugin validate .` passes |
| Markdown references | No broken local file links in the repository; all installed links stay inside each skill payload |
| Distribution | **8** archives rebuilt; ZIP integrity, legal notices and archive/directory payload byte parity checked |
| Temporary installation | Single/all-skill installs, explicit destination, existing-target preservation, unsafe names and symlink rejection checked |
| Independent forward test | Three standalone ticketing views render; final validators report 6 participants, 5 ordinary operations, 1 Signal reception, no errors/warnings, with missing-source coverage still partial |

CI runs the assertion suite on Linux and Windows, alongside the original smoke and structure jobs. Hosted results are recorded in [GitHub Actions](https://github.com/kinglez/mkl-uml/actions). Local results alone do not establish hosted-platform results.

## Repaired behavior and regression evidence

- **Activation path cap:** retained paths include the suffix after alternatives. Seven/eight/nine binary alternatives exercise 128/256/512 combinations; 256 complete paths are exhaustive, while larger sets explicitly report bounded sampling. Tests detect both leaks and false leaks in suffixes and restore suffix self-call warnings.
- **Empty/malformed sequences:** empty or markerless inputs, invalid boundaries, and fake declarations/messages inside comments or notes cannot pass as usable sequence diagrams. Invocation failures retain exit 2; model errors use exit 1.
- **Aliases:** relationship endpoints resolve to visible class identities before inheritance and operation provenance checks, including legitimate inherited operations.
- **Message sorts:** explicit synchronous/asynchronous calls can establish operation provenance; replies, Signals and lifecycle events cannot create spurious receiver operations. Ambiguous asynchronous provenance is reported. Typed creation declarations register the lifeline, and Signal receptions remain separate from ordinary operations in design/CDR parsing.
- **PDR coverage:** missing review sources now produce `NOT FULLY VERIFIED`, rather than an acceptance-with-rework disposition. Detected blocking defects retain reinspection precedence. The CLI's exit status still describes detected errors, separately from coverage.
- **Identifier lifecycle:** reorder, partial regeneration, explicit retirement, reserved high-water marks, namespaces and collision rejection are executable contracts. Omitted artifacts are retained and retired identifiers are not reused.

The original three parser defects and the semantic/lifecycle/reception follow-ups were observed failing before their fixes. The PDR coverage mismatch was also reproduced with a failing test before correction. Tests exercise CLI behavior and meaningful results rather than matching instructional prose. The mutation check proves that mere successful process execution cannot satisfy the fixture contracts; it is not an exhaustive mutation analysis.

## Independent skill forward test

A separate agent received a realistic request to produce a use case view, Buy Ticket sequence and design class model, without robustness or a PDR/CDR session. Supplied identities were `CU-07 Buy Ticket` and `CU-12 Refund Ticket`, displayed in the opposite order, plus a new payment-status goal. The request involved a Kiosk API client, supporting Payment Gateway, webhook Signal, synchronous reply, Ticket creation and refusal outcome.

The result retained CU-07/CU-12, marked CU-13 provisional because the complete registry was unavailable, associated the supporting gateway, used machine interfaces, and separated Signal reception/reply/lifecycle semantics from ordinary operations. It recorded polling as a design assumption and withheld cross-artifact completeness claims where sources were missing. The initial forward run exposed the created-lifeline/reception parser gaps; after focused fixes and new regressions, a final local rerun of all three validators exited 0 with no errors/warnings. Class coverage remained `NOT FULLY VERIFIED` because formal domain/specification sources were absent. All three generated diagrams rendered to SVG and PNG.

This is behavioral evidence for the tested scenario, not a guarantee that every future model or agent run will be correct.

## Operating and distribution changes

The recommended installation now uses the standard Skills CLI: `npx skills@latest add kinglez/mkl-uml -a codex` (or `-a claude-code`). Registry `skills@latest` resolved to 1.7.2 during verification, requiring Node.js 22.20+. Discovery found all eight skills. An initial temporary project install exposed absent root-level legal files and root-relative README links; each source folder now includes LICENSE/NOTICE and links shared project docs on GitHub. Two new regression tests check all eight source folders for legal-notice parity and links that remain valid when only that folder is installed. The updated local suite passed all 147 tests. A separate actual Skills CLI run installed all eight from the local source into a temporary Codex project with notices intact. Shared project docs remain available offline through the bundled installer and archives.

The npm package adds `bin/mkl-uml.mjs` and a `mkl-uml install` command for Codex or Claude Code. It uses the existing Python installer; no separate copy/provenance rules are introduced. Seven new tests cover help, all/selected skill installation, existing targets, invalid arguments, Python discovery failures, and installation from an actual npm-packed tarball. The package test also runs npm exec offline against that tarball. A separate actual npx run from a local directory installed all eight into a temporary destination. The full suite has 145 tests. Local runtime was Node.js 26.1.0 with npm 12.0.2; hosted CI uses Node.js 20 on Linux/Windows.

An npm tarball is built as `dist/mkl-uml-1.0.0.tgz`. No npm registry publication or installation into personal skill directories was performed. An actual npx command using `git+https://github.com/kinglez/mkl-uml.git#main` installed all eight from the public GitHub repository into a temporary destination. npm 12 rejected Git dependencies with its default policy; repeating with the command-scoped `--allow-git=all` option passed. The installation guide documents this requirement.

The first hosted Windows assertion run exposed two test portability assumptions: archive keys were compared with platform-native paths, and a synthetic text fixture used the host's default newline translation. Tests now use POSIX keys and explicit fixture bytes. The actual Windows npm-packed installation test and all sixteen hosted validator jobs passed on that initial run. Subsequent hosted outcomes are available in GitHub Actions.

All eight skill identifiers and directories now use the `mkl-` prefix. Frontmatter names, UI display names, internal invocation references, fixture contracts, CI matrices and plugin paths were synchronized. After the rename, all 138 tests, 85 smoke executions, eight metadata checks and plugin validation passed; the eight archives were rebuilt using the current names.

The eight entrypoints decreased from **2,139 to 481 lines** (about 77.5%). Essential input, modeling and verification decisions remain inline; conditional references hold detailed formal recipes. Standalone work is the default, with formal MKL handoffs requested explicitly. Coverage states are separate from gate dispositions, and existing remediation/header authorization is reused. Fixed repeated self-audit cycles and assurance certificates are no longer imposed on ordinary work.

Directory installation and archives use `tools/skill_payload.py`. Both include the same skill resources, LICENSE, NOTICE and selected standalone documentation. Markdown links are rewritten into the installed payload; repository-only destinations are left as readable labels. No personal skill directory or live plugin installation was modified.

## Compatibility and limits

- Names, authorship, organization and edition branding are MKL/mkl. Upstream copyright remains attributed in LICENSE/NOTICE; the source repository and snapshot are resolvable from NOTICE. The original source checkout was left unchanged.
- Existing CLI flags, fixture paths and multilingual parser vocabulary remain compatible. The 85 baseline fixture exit outcomes remain unchanged. New partial-review outputs and reception counts are intentional diagnostic changes.
- The inherited `enriched_good.puml` domain fixture exits 1 under the strict conceptual profile; its name does not imply acceptance under that profile. The previously documented escaped-newline correction to the academic use case example remains in place.
- Validators are small, profile-specific parsers with lexical heuristics. They do not implement the complete UML grammar/metamodel, prove correct responsibility allocation, establish human review, or certify production readiness.
- Capped path sampling can miss defects confined to omitted paths. Loop/interleaving semantics are not exhaustively explored. Retaining suffixes fixes the truncation defect, not the general state-space problem.
- The principal UML corrections were checked against OMG UML 2.5.1. Historical private-corpus line citations and quotations were not all re-verified. Resolvable publisher DOI references were added to the [bibliography](BIBLIOGRAPHY.md). A conflicting historical IEEE code-review rate transcription remains explicitly unresolved; no unsafe unit conversion or mandatory pacing policy is imposed from it.

## Reproduce

These commands are executable from the repository root, contain no argument placeholders, and were run locally:

```bash
python3 -m unittest discover -s tests -v
python3 tools/run_all_validators.py
python3 tools/run_all_validators.py --check-structure
python3 tools/package_skill.py
claude plugin validate .
plantuml --check-syntax 'skills/**/*.puml' 'tests/fixtures/**/*.puml'
```

All 210 PlantUML paths were additionally passed explicitly to the local CLI. Metadata checks were run against each skill with the locally installed Skill Creator validator. The repository's tests execute distribution installers only in temporary directories. The temporary no-op mutation is isolated from the source package.
