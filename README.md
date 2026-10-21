<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# MKL UML Skills

Eight English-language skills for domain modeling, use cases, robustness analysis, sequence diagrams, class design, and PDR/CDR reviews. Use a skill independently or request the full MKL workflow.

Author: **kingle.zhuang** · <kinglezhuang@vip.qq.com> · Organization: **mkl** · Copyright **2026**.

## Install

Requires Node.js 20+ (with npm/npx), Python 3.9+ and Git. Choose your application; each command installs all eight skills, documentation and license notices from [kinglez/mkl-uml](https://github.com/kinglez/mkl-uml).

**Codex — personal installation:**

```bash
npx --yes --allow-git=all --package "git+https://github.com/kinglez/mkl-uml.git#v1.0.0" mkl-uml install --agent codex
```

**Claude Code — personal installation:**

```bash
npx --yes --allow-git=all --package "git+https://github.com/kinglez/mkl-uml.git#v1.0.0" mkl-uml install --agent claude-code
```

These are executable instructions, not a record of installation into your account. Existing skill directories are never overwritten. To install just one skill, add `--skill mkl-uml-domain-modeler`. Use `--destination` for a custom directory or `--python` to select a Python executable.

The commands use the GitHub release tag directly; npm registry publication is not required. npm 12 requires the command-scoped `--allow-git=all` option; npm 11 and earlier can omit it. For a local checkout, replace the Git URL with `.`. Without Node.js, clone the repository, enter its root and use the Python installer:

```bash
python3 tools/install_skills.py --destination "$HOME/.agents/skills"
```

For Claude Code's Python command, project-only installation, Windows, tarball distribution, the local plugin, or Claude web uploads, see [Installation](docs/INSTALLATION.md).

## Use

In Codex, send:

```text
$mkl-uml-domain-modeler Model the domain of a hotel reservation system in PlantUML.
```

In Claude Code, send:

```text
/mkl-uml-domain-modeler Model the domain of a hotel reservation system in PlantUML.
```

Codex detects skill changes automatically; restart it if the new skills do not appear. In Claude Code, open `/skills` to check availability. Installation only makes the skills available; it does not generate a model until you request one.

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
- [MKL methodology](docs/MKL_METHODOLOGY.md): the complete design workflow.
- [Bibliography](docs/BIBLIOGRAPHY.md): primary sources and attribution.
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
