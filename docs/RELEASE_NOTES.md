# Release notes

## 1.0.4 — 2026-10-30

Tagged source: [`v1.0.4`](https://github.com/kinglez/mkl-uml/tree/v1.0.4). This documentation release uses order pricing throughout the README and introductory guides, adds a documentation reading guide, and presents eight stage prompts with inputs, outputs and completion checks. Tutorial outputs are separate from the maintained reference example. Offline skill packages include the new documentation navigation.

Package and plugin metadata identify the same version. The example retains its reviewed **1.0.3 validator snapshot** because the modeling instructions, validator runtime, business inputs, models and pricing implementation are unchanged. Installation instructions pin this new source tag. Publishing the source tag does not publish an npm registry package or imply formal design acceptance.

## 1.0.3 — 2026-10-30

Source update on `main`; package and plugin metadata identify the same version. Existing CLI arguments and the eight independently installable skills remain compatible.

- PDR produces a compact handoff with reviewed scope/versions, finding states, closure evidence and downstream implications. Sequence design checks that record against current inputs before relying on its transition recommendation; standalone work remains independent of a formal gate.
- PDR recognizes substantive compact alternative/exception tables alongside numbered steps. Identifier lists, traceability rows and placeholders remain insufficient behavior evidence.
- CDR normalizes PlantUML line wrapping when comparing control responsibilities with test-plan vocabulary. This removes a display-format false warning without claiming semantic test coverage.
- SOLID review uses explicit responsibility, change, substitution, client and source-dependency evidence. Coverage, demonstrated findings and unverified claims remain separate from formal acceptance; no automatic SOLID score or certification is introduced.

The order-pricing reference example is reverified against this runtime snapshot. Source publication does not publish an npm registry package, update existing installations or supply missing human review evidence.

## 1.0.2 — 2026-10-29

Tagged source: [`v1.0.2`](https://github.com/kinglez/mkl-uml/tree/v1.0.2). This documentation release includes the GitHub homepage workflow diagram, problem statements, usage steps, stage artifact tree and linked CU-07 examples. Installation commands and package/plugin metadata identify the same version.

The modeling instructions and runtime validators retain the v1.0.1 implementation. Publishing this source tag does not publish an npm registry package or imply marketplace approval.

## 1.0.1 — 2026-10-29

Tagged source: [`v1.0.1`](https://github.com/kinglez/mkl-uml/tree/v1.0.1), commit [`83e1f6b`](https://github.com/kinglez/mkl-uml/commit/83e1f6b29161de8882d1b9176c8f4d0c4a6cef1b). This version addresses the commercial-readiness audit of 2026-10-29. The npm package and Claude marketplace metadata identify the same version. Publishing the source tag does not publish to the npm registry, update an existing installation or complete marketplace review.

The changes cover evidence-aware PDR/CDR checks, annotation filtering, use-case-scoped flow coverage, complete sequence-fragment parsing, accurate accessor and parameter checks, input/output protection and faithful supported header conversion. Supporting guidance and positive examples are corrected alongside the executable regressions. See [the operating contract](OPERATING_CONTRACT.md) and [third-party source dispositions](THIRD_PARTY_SOURCES.md).

Validate the final candidate from a temporary installation before publication. Retain the source commit, working-tree patch or file hashes, test logs and archive hashes with the release. Create a tag only from the reviewed final commit, and build/upload artifacts from that commit. Published installations pinned to `v1.0.0` continue to refer to that older content.

The eight skills remain modeling and review aids with profile-specific validators. Formal gate acceptance needs the applicable evidence and human review. Third-party bibliography entries identify sources rather than providing a redistribution license for their publications.

## 1.0.0

Initial public English adaptation with eight independently installable skills, Apache-2.0 attribution, local plugin metadata and distribution helpers. Later work on `main` added the standard Skills CLI instructions and worked examples before this patch candidate was prepared.
