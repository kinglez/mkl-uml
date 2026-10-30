<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Install MKL UML

Install the eight skills into the project where you use your agent. Installation makes the skills available; you then invoke them in chat. To learn with the order-pricing files, first [clone this repository](../README.md#quick-start).

[Documentation guide](README.md) · [Eight-stage tutorial](EXAMPLES.md)

## Recommended: Skills CLI

You need Node.js **22.20+** and Git. Choose one command and run it in your target project's **terminal**:

```bash
# Codex: all eight skills in this project
npx skills@latest add kinglez/mkl-uml -a codex --skill '*' -y

# Claude Code: all eight skills in this project
npx skills@latest add kinglez/mkl-uml -a claude-code --skill '*' -y
```

These commands read the current GitHub repository. They do not require an MKL package on the npm registry. Python **3.9+** is needed when you run the bundled validators, not just to copy the skills.

| If you want… | Change the command |
|---|---|
| To choose skills interactively | Omit `--skill '*' -y`. |
| Only the domain modeler | Replace `--skill '*'` with `--skill mkl-uml-domain-modeler`. |
| A personal installation across projects | Add `-g`. |
| To list available skills without installing | Use `npx skills@latest add kinglez/mkl-uml --list`. |

See the [Skills CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) for additional options. The CLI handles agent discovery and installation locations.

## Invoke a skill

Open the project in your agent and send a matching request in **chat**. For example, in Codex:

```text
$mkl-uml-domain-modeler
Model the business concepts for a shopping-cart price quote with an optional
coupon. Product prices come from a trusted catalog. A quote returns the
subtotal, discount and payable amount without creating an order.
Save the conceptual model to uml/domain.puml and explain unresolved assumptions.
```

In Claude Code, replace the first line with `/mkl-uml-domain-modeler`. If the skill is not listed, reopen the agent session in the project where you installed it and check the selected installation scope.

For the complete order-pricing requirements and all eight prompts, continue with the **[tutorial](EXAMPLES.md)**. Skill installation does not copy `examples/order-pricing/` into another project; that folder belongs to the repository checkout.

## Other installation methods

Use these only when you need a pinned source, offline files or a host-specific upload. The source tag for the current version is **[v1.0.4](https://github.com/kinglez/mkl-uml/tree/v1.0.4)**. Historical release evidence remains in the [release notes](RELEASE_NOTES.md).

### Pinned source or bundled npx installer

The bundled installer adds offline project documentation and legal notices. It requires Node.js **20+**, Python **3.9+** and Git for the GitHub source. It installs all eight skills by default and refuses to overwrite existing target skill directories.

Run from any directory, choosing your agent:

```bash
npx --yes --allow-git=all --package "git+https://github.com/kinglez/mkl-uml.git#v1.0.4" mkl-uml install --agent codex
npx --yes --allow-git=all --package "git+https://github.com/kinglez/mkl-uml.git#v1.0.4" mkl-uml install --agent claude-code
```

`--allow-git=all` permits this Git dependency with npm 12. npm 11 and earlier can omit it. This option applies to that command. See [npm configuration](https://docs.npmjs.com/cli/using-npm/config/).

From an existing checkout, use its local source instead:

```bash
npx --yes --package . mkl-uml install --agent codex
```

Add `--skill mkl-uml-domain-modeler` for one skill, `--destination path/to/skills` for an explicit destination, or `--python path/to/python` for a specific interpreter. Replace the placeholder paths. The bundled installer uses personal locations by default: `.agents/skills` for Codex and `.claude/skills` for Claude Code.

### Python installer and Windows

From the repository root, choose the personal destination for your agent:

```bash
# macOS / Linux
python3 tools/install_skills.py --destination "$HOME/.agents/skills"
python3 tools/install_skills.py --destination "$HOME/.claude/skills"
```

```powershell
# Windows PowerShell
python tools/install_skills.py --destination "$env:USERPROFILE/.agents/skills"
python tools/install_skills.py --destination "$env:USERPROFILE/.claude/skills"
```

Append a skill name to install only that skill. For project-only installation, set the destination to the project's `.agents/skills` or `.claude/skills` folder. Existing target skills are preserved; inspect an existing installation before replacing it.

### Offline skill archives

From the repository root:

```bash
python3 tools/package_skill.py
```

This creates `dist/<skill-name>.skill` for each skill. Each is a ZIP containing one skill root, its local resources, `LICENSE`, `NOTICE` and offline `package-docs/`. The `.skill` suffix is this builder's convention; upload support depends on the host.

For Claude web, build one and copy it to the documented `.zip` extension:

```bash
python3 tools/package_skill.py mkl-uml-domain-modeler
cp dist/mkl-uml-domain-modeler.skill dist/mkl-uml-domain-modeler.zip
```

The `cp` command is for macOS/Linux; Windows users can copy/rename through the file manager. In Claude, use **Customize > Skills > Upload a skill** and select the ZIP. Enable it and try a matching request. See [Claude's upload instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude). Directory installation for Codex/Claude Code is separate from this web-account upload.

To share the whole bundled installer as a local npm tarball instead:

```bash
mkdir -p dist
npm pack --ignore-scripts --pack-destination dist
npx --yes --package ./dist/mkl-uml-1.0.4.tgz mkl-uml install --agent codex
```

These methods use GitHub or local files. They do not publish an npm registry package or submit a marketplace listing.

### Local Claude Code plugin

From the repository root, with the Claude CLI available:

```bash
claude plugin validate .
claude plugin marketplace add .
claude plugin install mkl-uml@mkl-uml
```

Choose this plugin method instead of a duplicate directory installation. Its skill names use the plugin namespace, for example `/mkl-uml:mkl-uml-domain-modeler`. Validation checks the manifest; adding the marketplace and installing the plugin are separate host changes.

## Check a distribution you build

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 tools/run_all_validators.py --check-structure
```

These are maintainer checks. To try the skills as a user, start with the chat request above and inspect its actual outputs. The [validation record](VALIDATION.md) documents previous executions and their scope.
