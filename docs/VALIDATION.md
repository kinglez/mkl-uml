<!-- Copyright 2026 kingle.zhuang. Organization: mkl. -->
# Validation record

This is a maintainer reference. To use a skill, start with the
[single-skill guide](STANDALONE.md).

## Latest recorded checks

| Check for v1.2.0 | Local result |
|---|---|
| Regression suite | 359 tests passed |
| Validator smoke tests | 89 invocations completed |
| Order-pricing example | 21 checks passed in candidate mode, including syntax checks and SVG/PNG rendering of 10 diagrams |
| Standalone review checks | Replayed the PDR disconnected-control and CDR premature-message cases from isolated skill packages, with corrected and incomplete-input controls |

## Version 1.1.1 checks

Version 1.1.1 includes the corrective update based on v1.1.0 (`7445f41`) and the
simplified documentation. The following records describe local executions on
2026-11-07. Hosted CI is recorded separately in the repository's Actions runs.

| Check | Recorded result |
|---|---|
| Original audit inputs | 16 findings corrected; 52 CLI replays with controls retained |
| Regression suite | 286 tests passed on Python 3.9.6 and 3.12.14 |
| Frozen reference / 1.1.1 runtime | 18 checks passed, including 8 gate methods and 15 reference test methods / 30 oracle cases; models, reviewed headers and 11 frozen input/code files unchanged |
| Single-skill use | All nine independently installed/executed; isolated forward trials inspected actual artifacts |
| Standard Skills CLI 1.7.4 | 9/9 local single-skill installs and validator executions passed |
| Other maintainer checks | 9/9 metadata checks, 89 smoke calls, Python/Node syntax and plugin manifest passed |

The detailed scope, original failure evidence and limitations remain in the
[full validation history](reference/VALIDATION_HISTORY.md). Historical results apply
to their recorded sources and environment, not automatically to future edits.

## What these checks establish

Validators exercise supported syntax, local rules and selected cross-artifact checks.
Rendering establishes that a runtime accepts the source. Semantic review examines the
actual meaning; runtime tests examine executed behavior. These are separate evidence.
None supplies formal human approval or proves every business rule, SOLID claim or quality target.

## Reproduce maintainer checks

Run from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 tools/run_all_validators.py --check-structure
python3 tools/sync_skill_modules.py
```

Standalone skills carry their own copies of shared validator modules. Edit
`bce_structure.py` in the robustness skill and `operation_evidence.py` in the
design-class skill. Edit `sequence_structure.py` in the sequence skill. Run
`python3 tools/sync_skill_modules.py --write` to refresh the PDR and CDR copies.
CI checks the copies without writing them.

For archive/npm payload checks, use the [advanced installation reference](reference/INSTALLATION.md#check-a-distribution-you-build).
Release status and older versions are in [release notes](RELEASE_NOTES.md).
