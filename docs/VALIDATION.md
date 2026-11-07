<!-- Copyright 2026 kingle.zhuang. Organization: mkl. -->
# Validation record

This is a maintainer reference. To use a skill, start with the
[single-skill guide](STANDALONE.md).

## Latest recorded checks

Version 1.1.1 includes the corrective update based on v1.1.0 (`7445f41`) and the
simplified documentation. The following records describe local executions on
2026-11-07. Hosted CI is recorded separately in the repository's Actions runs.

| Check | Recorded result |
|---|---|
| Original audit inputs | 16 findings corrected; 52 CLI replays with controls retained |
| Regression suite | 286 tests passed on Python 3.9.6 and 3.12.14 |
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
```

For archive/npm payload checks, use the [advanced installation reference](reference/INSTALLATION.md#check-a-distribution-you-build).
Release status and older versions are in [release notes](RELEASE_NOTES.md).
