<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Install and start

Run installation commands in your project's **terminal**. Send task prompts in
your agent's **chat**.

## Recommended: Skills CLI

You need Node.js **22.20+** and Git. For example, install only the architecture skill:

```bash
npx skills add kinglez/mkl-uml --skill mkl-uml-c4-architecture -a codex -y
```

Change the skill name to the one you need. To install all nine:

```bash
npx skills add kinglez/mkl-uml --skill '*' -a codex -y
```

For Claude Code, replace `-a codex` with `-a claude-code`.
These commands install the published GitHub source into this project.
From a local checkout, replace `kinglez/mkl-uml` with `.`.

## Invoke a skill

Open that project in your agent and paste a prompt from the [examples](../README.md#examples).
Codex uses `$mkl-uml-c4-architecture`; Claude Code uses `/mkl-uml-c4-architecture`.
Include your requirements or actual files and say what to save.

If the skill is not available, check the project and selected agent, then reopen the
agent session. Python **3.9+** is needed for bundled validator scripts. A PlantUML
runtime is needed for local diagram previews; installing a skill does not install it.

Next: **[send your first request](STANDALONE.md#make-a-request)**.

## Other installation methods

Use these only when the standard command does not fit your environment:

- <a id="pinned-source-or-bundled-npx-installer"></a>[Pinned source or bundled installer](reference/INSTALLATION.md#pinned-source-or-bundled-npx-installer).
- <a id="python-installer-and-windows"></a>[Python installer and Windows](reference/INSTALLATION.md#python-installer-and-windows).
- <a id="offline-skill-archives"></a>[Offline archives and Claude web upload](reference/INSTALLATION.md#offline-skill-archives).
- <a id="local-claude-code-plugin"></a>[Claude Code plugin](reference/INSTALLATION.md#local-claude-code-plugin).
- <a id="check-a-distribution-you-build"></a>[Maintainer distribution checks](reference/INSTALLATION.md#check-a-distribution-you-build).
