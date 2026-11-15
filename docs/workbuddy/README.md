# WorkBuddy distribution

Build and submit one skill at a time:

```bash
python3 tools/package_workbuddy_skill.py mkl-uml-domain-modeler --with-icon
```

The adapter uses the existing standalone payload builder, preserving legal notices,
offline references, and the English instruction body. It adds WorkBuddy frontmatter
from `skills.json` and the repository package version (or an explicit platform-only
version override in that catalog). The ZIP and a local metadata /
SHA-256 sidecar are written under `dist/workbuddy/`. Building does not submit anything.

The live parser additionally requires at most `skill-root/subdirectory/file`.
Nested payload paths are flattened with `__` separators and Markdown destinations
are rewritten to the corresponding bundled files. Collisions stop the build.
`--with-icon` uses `rsvg-convert` to render each distinct existing SVG mark with a
shared frame. The resulting market avatar is 512×512 PNG, below the form's 500 KB
limit. Rendering is a packaging dependency, separate from running the skill.

The [official skill schema](https://open.workbuddy.cn/docs/skill) defines the required
bilingual metadata. The creation form observed on 2026-11-15 accepts ZIP files up to
3 MB; this account's dashboard shows a limit of five skill review submissions per day.
Recheck the live form and quota before submission. All nine releases are authorized
as free. Submission success and review approval are separate states.
Replacing an uploaded draft's code ZIP requires a higher package version, even if
that draft has never been submitted. The 鲁棒分析图 terminology correction therefore
uses WorkBuddy version 1.1.2, leaving the portable repository version unchanged.
An existing name uploaded through Create returns an instruction to carry `assetId`;
adding that field to SKILL.md does not satisfy the parser. Its supported transport
has not been established. The draft Edit flow exposes package-derived fields as
read-only. Navigating directly back to its upload step changes the confirmation
preview but does not replace the persisted draft package: do not use this route.
Verify the persisted draft name/version in the asset list before submitting.

Release order: domain model, use-case diagram, use-case specification, robustness
diagram, PDR review, C4 architecture, sequence diagram, design class model, CDR review.
Record actual platform receipts in `submission-log.md`; never infer submission from
the generated ZIP or sidecar.
