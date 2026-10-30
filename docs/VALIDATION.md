<!-- Copyright 2026 kingle.zhuang. Organization: mkl. -->
# Validation record

**Evidence reference:** this page records checks that were actually executed and their limits. To run the example yourself, use the [example guide](../examples/order-pricing/README.md#run-the-example). To learn the skills, follow the [tutorial](EXAMPLES.md). See the [documentation guide](README.md) for the reading order.

## Documentation usability update — 2026-10-30

The README and introductory documents now follow order pricing throughout. The tutorial creates separate working artifacts; the maintained reference and its historical acceptance boundary remain explicit. Two independent AI editorial reviews compared the new instructions with the unchanged business requirements, specification and actual example output, with no unresolved concrete documentation finding.

| Check | Actual result |
|---|---|
| Source documentation | Local file links, heading anchors and the eight legacy tutorial anchors resolve. The six printed JSON results match the documented amounts and refusals. |
| Standalone documentation | All eight in-memory skill payloads contain `package-docs/docs/README.md`, retain the root navigation link and provide the online example fallback. Installed local links resolve. |
| Distribution and installer regressions | **12 distribution tests and 7 npx installation tests passed**, including archive/directory equality, standalone links and installation from a packed package. |
| Maintained reference | **All 13 default checks passed**, including both sequence validators, inspected-header comparison, 15 reference test methods, 30 oracle cases, visible examples and the extension exercise. Rendering was not rerun because the diagrams are unchanged. |
| Review baseline | Only the two changed example guides and their editorial maintenance note received new design-baseline hashes after affected-scope review. Requirements, oracle, models, pricing implementation and validator runtime are unchanged. |

These are documentation-maintenance checks against the 1.0.3 runtime. The existing version tag remains the previously published snapshot; this update does not change its target or turn the reference verifier into a checker for newly generated tutorial files.

## 1.0.3 workflow and evidence update — 2026-10-30

This source update strengthens PDR handoff, supported table recognition and scoped SOLID review. The implementation was tested and independently reviewed before updating the worked example's runtime snapshot. Formal human/business acceptance is still separate from these results.

| Check | Observed evidence |
|---|---|
| Full repository suite | **240 tests passed**: the previous 206 plus 31 PDR table regressions and 3 CDR display-label regressions. |
| Test-first PDR correction | The original compact-flow example produced ten false missing-behavior errors. The supported compact and numbered representations now pass the same flow checks. Empty actions, ID/reference-only cells, annotated placeholders, source/traceability tables and quoted/commented/code examples remain negative evidence. |
| Independent adversarial review | Two additional false greens were reproduced through the real CLI: reference-only/annotated-placeholder actions and tables nested beneath traceability headings. Both were corrected and independently reinspected; actual negative inputs return exit 1. Longer late reference material does not replace valid numbered behavior. |
| Test-first CDR correction | Wrapped control labels now retain visible word boundaries in test-plan comparison. Unrelated controls and comment-only evidence still produce warnings; missing supporting layers still withhold acceptance. |
| Minimum Python | All 31 new PDR tests passed on actual Python **3.9.6** as well as Python **3.14.7**. The reference example's current execution is recorded separately below. |
| Skill and distribution checks | **8/8** Skill Creator metadata checks pass. The full suite includes standalone installed-link containment and archive/directory equality; all eight `.skill` archives were generated. Local plugin-manifest validation and the repository structure check pass. |
| Workflow instruction consumption | An independent AI reviewer applied four scenarios: stale PDR with an open blocker, standalone work without PDR, diagram-only SOLID claims, and a supplied behavioral substitution counterexample. Responses preserve affected-scope reinspection, standalone autonomy, missing-evidence limits and the distinction between a finding and unexecuted runtime checks. |
| Worked example | The maintained [order-pricing validation record](../examples/order-pricing/VALIDATION.json) identifies its actual runtime snapshot, source baselines, finite contract tests and optional local rendering results. |

The compact historical illustration still contains the historical unsupported negative-minimum policy described in its PDR. A passing format-recognition check does not endorse that business rule. More generally, action recognition, word overlap, test-plan presence and clean exit codes do not prove semantic completeness or SOLID. The new [SOLID evidence guide](../skills/mkl-cdr-review/references/solid-evidence.md) records bounded claims and challenges; it creates no automatic score or certification.

## Historical 1.0.1 verification

Validation date: **2026-10-29**. Version **1.0.1** was verified locally before publication, then committed as [`83e1f6b`](https://github.com/kinglez/mkl-uml/commit/83e1f6b29161de8882d1b9176c8f4d0c4a6cef1b) and tagged [`v1.0.1`](https://github.com/kinglez/mkl-uml/tree/v1.0.1). The remediation baseline was `f6f21221ef950371700e0db5860f3e94e077bc07`.

Local environment: macOS, Python 3.14.7 and 3.9.6, Node.js 26.1.0, npm 12.0.2, PlantUML 1.2026.7 / Graphviz 15.1.1, Claude Code 2.1.270. Author: kingle.zhuang, organization mkl.

### Executed checks

| Check | Observed evidence |
|---|---|
| Full unittest suite | **206 passed**, including the original 147 and 59 additional regressions |
| Fixture contracts | All **85** example scenarios retain reviewed expected outcomes; **100** fixture/pipeline/degradation tests pass |
| Minimum Python runtime | Python **3.9.6** executes all **85** smoke scenarios; deliberately invalid examples retain expected findings. The final **32** CDR/header regressions also pass on 3.9.6 |
| Input and annotation contracts | All eight validator CLIs handle unreadable inputs without traceback; PlantUML comments/notes/legends and Markdown HTML comments cannot supply modeled evidence |
| Skill metadata | **8/8** pass Skill Creator quick validation |
| Plugin manifest | `claude plugin validate .` passes; manifest validity is separate from marketplace approval |
| PlantUML corpus | **210/210** repository inputs pass the local syntax check; this is not semantic certification |
| Syntax compatibility | **24** Python sources/tests parse under the Python 3.9 grammar; Node entrypoint syntax check passes |
| Standard Skills CLI | An actual `npx skills@latest add` copied all eight current local skills into an isolated Codex project; scripts and legal bytes matched source |
| npm installation | The full suite packs a real tarball and installs it with offline npm exec into a temporary destination; existing targets and unsafe names remain protected |
| Independent review | Separate runtime and reference/distribution reviews accepted the corrections within their declared scopes; review findings were corrected and reverified |

The tagged repair commit also passed the actual [GitHub Actions run](https://github.com/kinglez/mkl-uml/actions/runs/40868349510): assertion suites and all eight validator smoke jobs on Linux/Windows, plus the structure check. This hosted result applies to that commit; later documentation changes have their own run.

### Corrected contracts

- Evidence must be substantive and usable, not just a supplied path. Empty/unrecognized supporting artifacts withhold full acceptance while independent checks continue. Comments and annotations cannot act as real review targets or coverage.
- PDR accounts for every supplied CU specification. CDR compares `(CU, local flow)` identities and executable branch evidence. Explicit release scope remains distinct from an individual artifact's identity.
- Stray fragment separators do not truncate sequence parsing. Manual activation checks resume after `autoactivate off`; automatic regions and bounded path sampling retain explicit limits.
- Ordinary business operation names are no longer exempted as accessors. Each parameter is checked independently, including nested generic types and quoted defaults.
- Header generation rejects input/output aliases, preserves supported aliases/derived properties/generic types/association and property bounds, and exposes unsupported conversions. Signal receptions remain classified annotations with an explicit language-specific mapping gap rather than invented Operations.
- Existing correction authorization, actual reviewer independence, evidence-first disposition and valid zero-finding results are consistent across deep references. Planning rates/counts and defect-density observations are not acceptance criteria.
- Positive examples now have correctly addressed replies, observable success/refusal outcomes, anchored alternatives and coherent description/date/reference data. Only the missing-flow diagnostic fragment in the shared fixture oracle required updating; no expected exit status was relaxed.

### Independent forward use

Two independent agents used all eight skills in isolated workspaces, without the audit's intended solutions. The first generated library-renewal domain/use-case/specification/robustness artifacts and rendered the three diagrams. All four validators passed; two justified robustness style/degree warnings were documented.

The second performed PDR/CDR preparation and authorized local corrections on a support-desk package, then generated a standalone CU-12 ticket interaction and design model. It preserved AD-02 internal-state provenance and separated Operations, a Signal reception, replies and creation. Applicable validators and rendering passed. It withheld formal acceptance where implementer, decision-maker and independent signoff evidence was absent.

Header inspection found two additional silent omissions during that use: reception signatures and optional property bounds. Four new regressions reproduced them; the corrected generator was replayed on the actual CU-12 model and independently re-reviewed on both Python versions. Original forward observations and the corrected replay are retained separately in the remediation evidence.

### Provenance and distributions

See [THIRD_PARTY_SOURCES.md](THIRD_PARTY_SOURCES.md) for removed long quotations, retained bibliographic sources and remaining rights/provenance limits. All 18 root/per-skill LICENSE and NOTICE files retain their baseline bytes. This engineering cleanup does not assert legal clearance for every source-inspired adaptation, inherited asset or old release.

The Python/Node installer and ZIP archives consume the shared payload builder. Offline payloads include the operating contract, source inventory and release notes; local links are rewritten within each skill. Build hashes accompany artifacts in `dist/SHA256SUMS`. Record the exact final source tree/patch and artifacts when creating a release; older `v1.0.0` installations do not receive unpublished changes.

### Reproduce

Run from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 tools/run_all_validators.py
python3 tools/run_all_validators.py --check-structure
python3 tools/package_skill.py
claude plugin validate .
plantuml --check-syntax 'skills/**/*.puml' 'tests/fixtures/**/*.puml'
npm pack --ignore-scripts --pack-destination dist
```

All 210 PlantUML paths were also passed explicitly to the local renderer. Installer tests use temporary directories; no personal skill directory or live plugin installation was changed. The detailed Chinese acceptance matrix, red/green logs, independent reviews, forward artifacts and final distribution manifest are delivered with the remediation result.

Validators remain profile-specific lexical/structural checks. They do not prove complete UML semantics, production behavior, exhaustive branch/loop/interleaving coverage, legal rights or human acceptance.
