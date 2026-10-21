# Installation and distribution

The package contains eight independent skills and a local Claude Code marketplace. Select the method supported by the host. UI metadata does not supply a runtime integration or tool authorization.

The commands below are executable instructions, not a record of installation into your account. Run the Skills CLI from your target project; repository tools require a local checkout. `path/to/...` arguments are placeholders. The validation record identifies checks performed in temporary directories.

## Recommended: Skills CLI

Requires Node.js 22.20+ and Git. Python 3.9+ is needed only when running the validators, not when copying the skills. From your target project, choose your agent:

```bash
npx skills@latest add kinglez/mkl-uml -a codex
npx skills@latest add kinglez/mkl-uml -a claude-code
```

The CLI prompts for skills and installs to the current project by default. Add `-g` for user-level installation across projects. To select one or all eight explicitly:

```bash
npx skills@latest add kinglez/mkl-uml -a codex --skill mkl-uml-domain-modeler
npx skills@latest add kinglez/mkl-uml -a codex --skill '*' -y
```

Use `--list` to discover skills without installing. `--copy` selects file copies rather than links when supported. The standard CLI manages discovery, agent locations and updates; no MKL npm registry publication is required. See the [official CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

Every source skill folder includes its entrypoint, local references, scripts, LICENSE and NOTICE. Shared project documentation is linked on GitHub. For an installation that also carries offline copies of the shared project documentation, use the bundled installer or per-skill archive below.

## Alternative: bundled npx installer

Requires Node.js 20+ with npm/npx and Python 3.9+. Git is also required for the GitHub source below. The Node entrypoint reuses the same Python payload builder and installer, including legal notices, standalone docs and refusal to overwrite existing targets.

### From GitHub

Run from any directory. These commands pin the source to release tag `v1.0.0`:

```bash
npx --yes --allow-git=all --package "git+https://github.com/kinglez/mkl-uml.git#v1.0.0" mkl-uml install --agent codex
npx --yes --allow-git=all --package "git+https://github.com/kinglez/mkl-uml.git#v1.0.0" mkl-uml install --agent claude-code
```

The command-scoped `--allow-git=all` option permits this Git dependency with npm 12, which otherwise reports `EALLOWGIT`. npm 11 and earlier can omit that option. It does not change global npm configuration. See [npm package specifications](https://docs.npmjs.com/cli/using-npm/package-spec/) and [npm configuration](https://docs.npmjs.com/cli/using-npm/config/).

The repository keeps `package.json`, `bin/`, `tools/`, `skills/`, `docs/`, `LICENSE` and `NOTICE` at its root. Publishing to GitHub makes this source installation available; it does not publish the package to the npm registry.

### From a local checkout

From this `mkl-uml` directory, choose your application:

```bash
# Codex: all eight in the personal .agents/skills directory.
npx --yes --package . mkl-uml install --agent codex

# Claude Code: all eight in the personal .claude/skills directory.
npx --yes --package . mkl-uml install --agent claude-code
```

Single skill or explicit destination:

```bash
npx --yes --package . mkl-uml install --agent codex --skill mkl-uml-domain-modeler
```

Add `--destination path/to/skills` to override the directory; that path is a placeholder. Python is detected automatically (`python3`, then `python`; on Windows the `py -3` launcher is tried first). Add `--python path/to/python` if needed; replace that executable placeholder with your actual Python path.

The package has not been published to the npm registry. Use the explicit GitHub source, local directory or tarball; an unqualified registry package name is a different installation source. No npm registry account is required for these methods.

### Share the npm tarball

On macOS/Linux, these executable commands create a tarball and install from it:

```bash
mkdir -p dist
npm pack --ignore-scripts --pack-destination dist
npx --yes --package ./dist/mkl-uml-1.0.0.tgz mkl-uml install --agent codex
```

The tarball includes the CLI, Python helpers, eight skills, supporting documentation, LICENSE and NOTICE. It can be moved to another machine; run npx with its actual local path. This is separate from the per-skill `.skill` archives. npm registry installation becomes available only after a separate registry publication.

## Python alternative: personal installation

On macOS or Linux, run from the repository root with Python 3. These commands have no placeholder arguments; choose the application you use.

```bash
# Codex: install all eight into the documented personal skills location.
python3 tools/install_skills.py --destination "$HOME/.agents/skills"

# Claude Code: install all eight into its personal skills location.
python3 tools/install_skills.py --destination "$HOME/.claude/skills"
```

To install only one skill:

```bash
python3 tools/install_skills.py --destination "$HOME/.agents/skills" mkl-uml-domain-modeler
```

The commands are installation instructions, not actions performed on your account. Actual installer verification used temporary directories only.

In Windows PowerShell, use `python` if that is your Python 3 executable:

```powershell
python tools/install_skills.py --destination "$env:USERPROFILE/.agents/skills"
python tools/install_skills.py --destination "$env:USERPROFILE/.claude/skills"
```

Official discovery locations: [Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills), [Claude Code](https://code.claude.com/docs/en/skills#choose-where-skills-load).

## Verify and invoke

In Codex, select a skill with `$` and send, for example:

```text
$mkl-uml-domain-modeler Model the domain of a hotel reservation system in PlantUML.
```

Codex detects skill changes automatically; restart it if the new skills do not appear. In Claude Code, check `/skills`, then send:

```text
/mkl-uml-domain-modeler Model the domain of a hotel reservation system in PlantUML.
```

Directory installation applies to the local application. Claude web/Cowork account skills require the separate upload flow below.

## Custom destination or project-only installation

Use the shared payload installer so legal notices and local documentation accompany the skill. It requires an explicit destination and refuses to overwrite any existing target skill directory. Choose another destination or inspect/move an existing installation before replacing it.

```bash
python3 tools/install_skills.py --destination path/to/skills mkl-uml-domain-modeler
python3 tools/install_skills.py --destination path/to/skills
```

The second command installs all eight. Destinations can be a host's user skills directory or a project's skills directory. Discovery/reload and invocation syntax depend on the host; these commands do not configure host permissions or create an account integration. The Python payload adds offline project documentation; source folders installed by the standard Skills CLI link that shared documentation on GitHub.

For a project-only installation, use the absolute path to the project's `.agents/skills` (Codex) or `.claude/skills` (Claude Code) as the destination. The repository's own `skills/` directory is a source collection, not automatically an installed host location.

## Claude web: ZIP upload

The current builder writes ZIP archives with a `.skill` suffix. Claude's documented upload format is `.zip`. Build a skill and copy the archive with that extension:

```bash
python3 tools/package_skill.py mkl-uml-domain-modeler
cp dist/mkl-uml-domain-modeler.skill dist/mkl-uml-domain-modeler.zip
```

The `cp` example is executable on macOS/Linux; Windows users can copy/rename the archive through their file manager. Its contents remain identical. In Claude, open **Customize > Skills**, choose **Upload a skill**, and select the `.zip`. Enable the skill, then test a matching request. This package has not been uploaded through that interface during local validation. See [Claude's official instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Archive contents

```bash
python3 tools/package_skill.py
python3 tools/package_skill.py mkl-uml-domain-modeler
```

Archives are ZIP files written to `dist/<skill-name>.skill`. Upload them only through a host that supports that format. Each archive contains one skill root with its resources, `LICENSE`, `NOTICE`, and `package-docs/`. Archive and directory installation share the same payload construction; relative documentation links work without the repository.

Source and release downloads belong to [kinglez/mkl-uml](https://github.com/kinglez/mkl-uml). No public marketplace listing is implied. Build from this edition rather than retrieving an upstream-language release.

## Local Claude Code plugin

The root `.claude-plugin/marketplace.json` declares the local marketplace and its eight skills. If that CLI is available, these are executable commands:

```bash
claude plugin validate .
claude plugin marketplace add .
claude plugin install mkl-uml@mkl-uml
```

Validation checks the manifest. Adding the marketplace and installing the plugin are separate host changes; they are not implied by packaging or validation. The plugin retains access to repository root resources. The namespace is `mkl-uml`, with invocation names such as `/mkl-uml:mkl-uml-domain-modeler`.

## Verify a distribution

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 tools/run_all_validators.py
python3 tools/run_all_validators.py --check-structure
```

Assertions check known behavior; smoke checks check execution and recognized statuses. Neither proves complete UML semantics or human review. See [Validation record](VALIDATION.md) for current evidence and limits.
