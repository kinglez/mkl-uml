# Release notes

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
