<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# MKL Design class models

Cohesive responsibilities, complete operation signatures, state and relationships. Supports inherited contracts and PlantUML aliases.

## Use

Read [SKILL.md](SKILL.md) for the operating instructions and conditional reference routes. Standalone assistance is the default; use the formal MKL workflow when requested. Generation, review, refactoring and validation are separate operations within either workflow.

**Minimum input:** Design scope/responsibilities and constraints, or an existing class model.

**Result:** PlantUML design model; provenance map and justified solution classes for MKL handoff.

Missing upstream evidence limits dependent checks. Report **checked**, **partial**, or **blocked** coverage; never turn missing evidence into an acceptance claim. Preserve existing IDs across reordering and refactoring. See [Operating contract](https://github.com/kinglez/mkl-uml/blob/main/docs/OPERATING_CONTRACT.md) for the shared input and identifier lifecycle rules.

## Validation

From this skill directory, the following is executable. Every `path/to/...` argument is a placeholder; documentation examples are not a record of execution:

```bash
python scripts/validate_design_class_puml.py --clases path/to/classes.puml
```

Use `--help` for optional inputs and legacy flags. Exit 0 means no detected errors under the supported profile (warnings can remain); 1 means findings; 2 means invocation/input failure. Lexical checks, local MKL conventions and diagram quality heuristics are not a complete UML semantic validator. Inspect meaning and rendered syntax separately.

The repository-level assertion suite checks fixed expected exits and important diagnostics across all fixture sets, plus parser and cross-artifact regressions. `tests/examples/` includes deliberately invalid examples; names alone do not establish their expected result. Spanish fixture paths and parser vocabulary are retained for compatibility.

## Install and distribute

Install with `npx skills@latest add kinglez/mkl-uml --skill mkl-uml-design-class-model -a codex`; use `-a claude-code` for Claude Code or add `-g` for personal scope. This folder includes its instructions, references, validator scripts, `LICENSE` and `NOTICE`. Shared project documentation is linked on GitHub. The Python installer and `.skill` archives additionally bundle offline project documentation. See [Installation](https://github.com/kinglez/mkl-uml/blob/main/docs/INSTALLATION.md).

## Sources and ownership

Consult the focused references linked from [SKILL.md](SKILL.md), the [bibliography](https://github.com/kinglez/mkl-uml/blob/main/docs/BIBLIOGRAPHY.md), and the [method overview](https://github.com/kinglez/mkl-uml/blob/main/docs/MKL_METHODOLOGY.md). Historical source checks are attributed records, not newly repeated verification or required audit ceremonies.

English edition: **kingle.zhuang**, <kinglezhuang@vip.qq.com>, organization **mkl**, copyright **2026**. Licensed under Apache-2.0; upstream attribution is retained in the distribution's `NOTICE` and `LICENSE`.
