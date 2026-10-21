<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# MKL Conceptual domain modeling

Business vocabulary and conceptual relationships, kept separate from implementation design.

## Use

Read [SKILL.md](SKILL.md) for the operating instructions and conditional reference routes. Standalone assistance is the default; use the formal MKL workflow when requested. Generation, review, refactoring and validation are separate operations within either workflow.

**Minimum input:** Business scope and relevant concepts, or an existing domain model.

**Result:** Conceptual PlantUML; assumptions and a proposed domain delta when relevant.

Missing upstream evidence limits dependent checks. Report **checked**, **partial**, or **blocked** coverage; never turn missing evidence into an acceptance claim. Preserve existing IDs across reordering and refactoring. See [Operating contract](../../docs/OPERATING_CONTRACT.md) for the shared input and identifier lifecycle rules.

## Validation

From this skill directory, the following is executable. Every `path/to/...` argument is a placeholder; documentation examples are not a record of execution:

```bash
python scripts/validate_domain_puml.py path/to/model.puml
```

Use `--help` for optional inputs and legacy flags. Exit 0 means no detected errors under the supported profile (warnings can remain); 1 means findings; 2 means invocation/input failure. Lexical checks, local MKL conventions and diagram quality heuristics are not a complete UML semantic validator. Inspect meaning and rendered syntax separately.

The repository-level assertion suite checks fixed expected exits and important diagnostics across all fixture sets, plus parser and cross-artifact regressions. `tests/examples/` includes deliberately invalid examples; names alone do not establish their expected result. Spanish fixture paths and parser vocabulary are retained for compatibility.

## Install and distribute

Use the package builder/installer in [Installation](../../docs/INSTALLATION.md); it includes legal notices and standalone documentation. Raw copying of this source folder omits those root resources. Directory installation and `.skill` archives use the same payload builder.

## Sources and ownership

Consult the focused references linked from [SKILL.md](SKILL.md), the [bibliography](../../docs/BIBLIOGRAPHY.md), and the [method overview](../../docs/MKL_METHODOLOGY.md). Historical source checks are attributed records, not newly repeated verification or required audit ceremonies.

English edition: **kingle.zhuang**, <kinglezhuang@vip.qq.com>, organization **mkl**, copyright **2026**. Licensed under Apache-2.0; upstream attribution is retained in the distribution's `NOTICE` and `LICENSE`.
