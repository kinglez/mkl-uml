<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# MKL UML Skills

Eight English-language skills for domain modeling, use cases, robustness analysis, sequence diagrams, class design, and PDR/CDR reviews. Use a skill independently or request the full MKL workflow.

Author: **kingle.zhuang** · <kinglezhuang@vip.qq.com> · Organization: **mkl** · Copyright **2026**.

## Install

Use the [Skills CLI](https://github.com/vercel-labs/skills), with Node.js 22.20+ and Git. Python 3.9+ is needed to run the bundled validators. Run from the project where you want to use the skills.

**Codex:**

```bash
npx skills@latest add kinglez/mkl-uml -a codex
```

**Claude Code:**

```bash
npx skills@latest add kinglez/mkl-uml -a claude-code
```

Choose skills when prompted. Installation is project-scoped by default; add `-g` for personal installation across projects. Add `--skill mkl-uml-domain-modeler` to select one, or `--skill '*' -y` to install all eight without prompts. These are executable instructions; verification used temporary projects, not your personal skills directories.

Each skill includes its local references, scripts, LICENSE and NOTICE. For the Python/bundled installer, offline documentation, Windows, the local plugin, or Claude web uploads, see [Installation](docs/INSTALLATION.md).

## Use

Open your project in Codex or Claude Code after installation. Paste the following into the **agent chat**, not your terminal.

**Codex — create your first domain model:**

```text
$mkl-uml-domain-modeler
Model a technical support desk in PlantUML:
- A Requester reports an Incident in a Category.
- Each Category has a current ServiceAgreement defining its deadline.
- Only requesters authorized for that category may register incidents.
- A registered incident has a description, registration date and due date.
Save the conceptual model to uml/domain.puml and explain your assumptions.
```

**Claude Code:** use `/mkl-uml-domain-modeler` instead of `$mkl-uml-domain-modeler`, followed by the same request.

Expected result: `uml/domain.puml` containing the four domain concepts and their relationships, plus an explanation of assumptions. This requests PlantUML source; ask for SVG/PNG as well if you want a rendered image and a renderer is available.

**Review the file you just generated:**

```text
$mkl-uml-domain-modeler
Review uml/domain.puml against the requirements above. Locate modeling
problems, explain their impact, and suggest corrections. Preserve existing IDs.
```

See [Usage examples](docs/EXAMPLES.md) for copyable prompts for **all eight skills**, the full modeling sequence, existing-file review, and a complete worked input/output set. The prompts describe work to request; installation alone does not generate files.

## Choose a skill

| Skill | Use it for |
|---|---|
| [mkl-uml-domain-modeler](skills/mkl-uml-domain-modeler/README.md) | Conceptual domain vocabulary and relationships |
| [mkl-uml-use-case-diagram](skills/mkl-uml-use-case-diagram/README.md) | Actors, system scope and user goals |
| [mkl-use-case-specifier](skills/mkl-use-case-specifier/README.md) | Basic, alternative and exception flows |
| [mkl-uml-robustness-diagram](skills/mkl-uml-robustness-diagram/README.md) | Boundary/control/entity analysis |
| [mkl-pdr-review](skills/mkl-pdr-review/README.md) | Preliminary Design Review before detailed design |
| [mkl-uml-sequence-diagram](skills/mkl-uml-sequence-diagram/README.md) | Interactions, responsibility allocation and operation deltas |
| [mkl-uml-design-class-model](skills/mkl-uml-design-class-model/README.md) | Design classes, operations, state and relationships |
| [mkl-cdr-review](skills/mkl-cdr-review/README.md) | Critical Design Review before implementation |

Standalone work is the default. Formal reviews are requested explicitly. Operation calls can establish class-operation provenance; replies, Signals and lifecycle messages retain their own semantics. Missing source artifacts are reported as verification limits.

## Documentation

- [Operating contract](docs/OPERATING_CONTRACT.md): modes, required inputs, coverage and stable IDs.
- [Usage examples](docs/EXAMPLES.md): first model, all eight skills and worked artifacts.
- [MKL methodology](docs/MKL_METHODOLOGY.md): the complete design workflow.
- [Bibliography](docs/BIBLIOGRAPHY.md): primary sources and attribution.
- [Third-party sources](docs/THIRD_PARTY_SOURCES.md): content provenance and redistribution dispositions.
- [Release notes](docs/RELEASE_NOTES.md): the local candidate and published-version boundaries.
- [Validation record](docs/VALIDATION.md): executed checks and known limits.

MKL is this edition's branding for an adapted use-case-driven workflow. The source literature remains attributed to its original authors. Skill instructions and outputs are English by default; request another output language when needed.

## Development and distribution

These executable commands run tests and rebuild the ZIP-format `.skill` archives in `dist/`:

```bash
python3 -m unittest discover -s tests -v
python3 tools/package_skill.py
```

The `.skill` suffix is a packaging convention, not a universal import format. Follow the host-specific [installation guide](docs/INSTALLATION.md). Validators check supported profiles and heuristics; passing does not establish complete UML semantics or formal human acceptance.

## License and contribution

[Apache-2.0](LICENSE). [Project information](NOTICE) combines authorship, upstream attribution, citation, contribution steps and community conduct. This edition was translated and adapted with AI assistance; AI tools are not coauthors.
