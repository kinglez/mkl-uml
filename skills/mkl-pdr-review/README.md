<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# MKL Preliminary Design Review

Scoped preliminary-design preparation or an explicitly requested formal MKL PDR. Distinguishes evidence coverage from gate disposition.

## Use

Read [SKILL.md](SKILL.md) for the operating instructions and conditional reference routes. Standalone assistance is the default; use the formal MKL workflow when requested. Generation, review, refactoring and validation are separate operations within either workflow.

**Minimum input:** Supplied preliminary-design artifacts for scoped checks. A full gate also needs robustness, CU behavior, domain and applicable review evidence.

**Result:** Located findings and coverage; a formal record with traceability, decisions and actions when requested.

Missing upstream evidence limits dependent checks. Report **checked**, **partial**, or **blocked** coverage; never turn missing evidence into an acceptance claim. Preserve existing IDs across reordering and refactoring. See [Operating contract](https://github.com/kinglez/mkl-uml/blob/main/docs/OPERATING_CONTRACT.md) for the shared input and identifier lifecycle rules.

For a copyable prompt, required files and expected output, see the [worked usage example](https://github.com/kinglez/mkl-uml/blob/main/docs/EXAMPLES.md#5-pdr-preparation).

## Validation

From this skill directory, the following is executable. Every `path/to/...` argument is a placeholder; documentation examples are not a record of execution:

```bash
python scripts/validate_pdr.py --robustez path/to/robustness.puml --spec path/to/spec.md --dominio path/to/domain.puml
```

Use `--help` for optional inputs and legacy flags. Exit 0 means no detected errors under the supported profile (warnings can remain); 1 means findings; 2 means invocation/input failure. Lexical checks, local MKL conventions and diagram quality heuristics are not a complete UML semantic validator. Inspect meaning and rendered syntax separately.

The repository-level assertion suite checks fixed expected exits and important diagnostics across all fixture sets, plus parser and cross-artifact regressions. `tests/examples/` includes deliberately invalid examples; names alone do not establish their expected result. Spanish fixture paths and parser vocabulary are retained for compatibility.

## Install and distribute

Install with `npx skills@latest add kinglez/mkl-uml --skill mkl-pdr-review -a codex`; use `-a claude-code` for Claude Code or add `-g` for personal scope. This folder includes its instructions, references, validator scripts, `LICENSE` and `NOTICE`. Shared project documentation is linked on GitHub. The Python installer and `.skill` archives additionally bundle offline project documentation. See [Installation](https://github.com/kinglez/mkl-uml/blob/main/docs/INSTALLATION.md).

## Sources and ownership

Consult the focused references linked from [SKILL.md](SKILL.md), the [bibliography](https://github.com/kinglez/mkl-uml/blob/main/docs/BIBLIOGRAPHY.md), and the [method overview](https://github.com/kinglez/mkl-uml/blob/main/docs/MKL_METHODOLOGY.md). Historical source checks are attributed records, not newly repeated verification or required audit ceremonies.

English edition: **kingle.zhuang**, <kinglezhuang@vip.qq.com>, organization **mkl**, copyright **2026**. Licensed under Apache-2.0; upstream attribution is retained in the distribution's `NOTICE` and `LICENSE`.
