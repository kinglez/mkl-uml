<!-- Copyright 2026 kingle.zhuang. Organization: mkl. -->
# Validation record

This archived record preserves verification history captured before the documentation
cleanup on 2026-11-07. See the [current summary](../VALIDATION.md) for the short entry point.

**Evidence reference:** this page records checks that were actually executed and their limits. To run the example yourself, use the [example guide](../../examples/order-pricing/README.md#run-the-example). To learn the skills, follow the [tutorial](../EXAMPLES.md). See the [documentation guide](../README.md) for the reading order.

## Unreleased correctness and standalone update — 2026-11-07

This working-tree update is based on v1.1.0 (`7445f41`); it is not a new tag or
hosted release. The original audit and corrected replays are kept separately.

| Executed check | Observed result |
|---|---|
| Original audit cases | All **16** confirmed findings have corrected original-input replays, with normal/detection controls retained. **52** CLI invocations were re-executed without overwriting the initial failure evidence. |
| Repository regressions | **286 tests passed** on Python **3.9.6** and **3.12.14**; **23** test methods were added. New regression inputs are domain-neutral; task-specific forward trials remain outside the repository. |
| Single-skill execution | Each of the **9** skills runs with its minimum targets from an unrelated working directory, through both a raw source copy and the explicit installer, with isolated Python imports and no sibling skill. CDR header generation resolves its own helper. |
| Standard Skills CLI | **9/9** single-skill local installations and validator executions passed using the actual cached Skills CLI **1.7.4**. Each project contains only the selected skill; installed validator bytes match the corrected local source. This does not test an unpublished GitHub revision. |
| Independent forward use | All nine skills were exercised independently from isolated installations. Actual generated sources, local renders, scoped reviews and commands were inspected. The text-specification heading defect was reproduced and rechecked on unchanged English and Chinese inputs after correction. |
| Additional scoped checks | Nearest typed C4 ownership, Markdown identifier headings and Chinese structural labels have positive/negative regressions. Existing legal external-actor participation remains valid. |
| Maintainer checks | **9/9** Skill Creator metadata checks, repository structure, **89** validator smoke invocations, Python 3.9 grammar for **16** changed/new Python files, Node syntax and local Claude plugin-manifest validation pass. Smoke checks alone do not establish expected semantic outcomes. |

Empty or annotated support cannot establish completed coverage. PDR keeps basic dialogue
separate from alternate/exception behavior. Flow labels require behavior in their own
operand. Sequence activation analysis respects terminating breaks and combines parallel
operands; capped enumeration remains sampled. Conceptual declarations/relationships
retain aliases and supported decoration. Enumeration literals, modeled members,
interface inheritance and parameter direction are preserved or explicitly diagnosed.

The [standalone guide](../STANDALONE.md) records minimum inputs and partial coverage.
A CDR class-only request can be reviewed manually; its CLI still requires classes
and a sequence. Chinese specification field/ID/outcome-keyword recognition does not
extend English/Spanish writing-risk lexicons or establish Chinese semantic correctness.

Core validators remain Python-standard-library tools. The separate maintainer metadata
checker used an isolated Python 3.12 environment with PyYAML 6.0.3; this is not a
runtime dependency added to any skill. No personal skill installation was changed.
Formal human acceptance, exhaustive UML semantics, runtime quality and current hosted
CI are not established by these local checks.

## Source release v1.1.0 - 2026-11-07

The v1.1.0 source tag includes the C4 skill and the reviewed nine-stage Order Pricing
replay. The local checks below apply to that release preparation. Hosted CI status is
recorded separately; a source tag is not an npm registry publication or formal approval.

## Order-pricing nine-stage replay - 2026-11-07

The maintained example now adds C4 high-level architecture between PDR and detailed
design. Requirements, the independent oracle and all reference Python sources/tests
remain byte-unchanged across **11** frozen files. Existing models/code were retained
and reexamined; this is a retrospective replay, not an independently regenerated build.

| Executed check | Result |
|---|---|
| Whole reference, Python 3.9.6 with local rendering | **21 checks passed**, **10 diagrams**, **8 blocking/revalidation test methods**, **15 reference test methods / 30 oracle cases**. |
| Whole reference, Python 3.12.14 without rendering | **18 checks passed** on the same sources; rendering is a separate recorded invocation. |
| Core repository regression suite | **263 passed** on Python 3.9.6 and 3.12.14. Application-specific acceptance stays under examples/order-pricing/scripts, outside the business-independent skill tests. |
| Architecture allocation | Six responsibility groups, 17 modeled classifiers, 22 actual declarations and four scoped L4 classifiers. Shared adapter helper consumers are compared with actual calls. |
| Semantic/wording reinspection | Independent AI review closed two allocation/specification findings and four editorial findings; architecture/design snapshots include actual inspected inputs and mandatory upstream edges. |
| Distribution | 13 distribution tests and 7 npm-install tests passed, including standalone links and packed/offline payload equality. Homepage workflow SVG is carried in legacy offline documentation; the C4 skill remains self-contained. |
| Visual/static checks | Ten diagram previews inspected; homepage Fireworks geometry/composition/text checks pass. HTML has nine unique tab targets, valid assets and valid embedded JS syntax. Browser file:// preview was blocked by URL policy, so interaction testing is not claimed. |

The current [example result](../../examples/order-pricing/VALIDATION.json) records actual
invocations; logs and role/scope limits are separate from formal approval. Historical
pre-C4 result/source/handoff records remain under review-history/. No new deployment,
state lifecycle, performance/SLA target, business policy, hosted CI result or release tag
is inferred from these local results. The current [architecture review](../../examples/order-pricing/architecture/REVIEW.md)
records the actual primary-author and independent AI roles and the closed findings.

## Initial C4 capability validation - 2026-11-07 (before order-pricing replay)

This candidate adds the ninth skill and a high-level architecture handoff. Its primary
method reference is the official C4 model: context, containers, components and code;
deployment is supporting. C4-PlantUML draws architecture macros. Scoped UML classes
express the code zoom, with sequences as complementary behavior. Requirement sources
remain arbitrary external evidence; no PRD or fixed input filename is required.

| Check | Observed local evidence |
|---|---|
| Full repository suite | **263 tests passed** on Python **3.9.6** and **3.12.14**. This includes **22** new C4 contract tests and one new C4 distribution test. |
| C4 contracts | Ready and blocked handoffs, source/requirement/decision/view links, unknown fields/references, quality scenarios/metadata, cross-view drift, ownership, unsupported syntax, malformed input and path containment are exercised. |
| Adversarial shape probe | **189** field/type mutations returned structured results without uncaught exceptions; this finite probe is not exhaustive fuzzing. |
| Real rendering | The four neutral C4 sources rendered to SVG and PNG using PlantUML **1.2026.9**, bundled C4-PlantUML **2.14.0**, Graphviz **16.1.0**. All four previews were inspected. No public renderer or library download was used. |
| Code-level route | A neutral component-to-class mapping and proposed UML class view were locally rendered. The existing class checker reports no errors; without behavior/domain sources, five provenance/responsibility layers remain unexecuted. This is a notation/handoff exercise, not complete design verification. |
| Installation/distribution | Actual standard Skills CLI installation of the new local skill into an isolated Codex project succeeded. The full suite packs a real npm tarball, installs offline and compares all nine payloads. C4 directory/archive bytes match; standalone links and four installed fixtures pass. |
| Metadata and smoke | **9/9** Skill Creator checks pass. All nine validator smoke checks, structure check, Node syntax and local Claude plugin-manifest validation pass. Deliberately invalid legacy fixtures retain their expected findings. |
| Maintained reference | The original order-pricing directory is byte-unchanged against HEAD and all **13** default reference checks pass. No new C4 business acceptance is claimed for that example. |

The C4 checker does not run PlantUML or approve an architecture. It checks a documented
literal profile and declared references; unsupported syntax remains partial and blocks
strict readiness. Actual quality achievement, complete semantics, stale-source detection
and formal human approval are outside that mechanical result. Existing PDR/CDR tools do
not automatically parse C4. Their in-scope architecture comparison is a labeled semantic
review. This candidate has no release tag or hosted CI result. Local verification does not imply publication.

Independent forward evaluation used a meeting-notes-only desktop task in an isolated
external workspace. It produced source/requirement/decision/view mappings and locally
rendered views without demanding a PRD. Undefined policies remained draft and strict
readiness was withheld. A scenario-metadata schema mismatch was reproduced, corrected
and rechecked with the original input. Semantic inspection also corrected an authored
view that had treated data artifacts as software systems; both the checker and renderer
had accepted it. The modeling guidance now makes that abstraction distinction explicit.
This is bounded AI evaluation, not independent human approval or proof across all tasks.

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
| Worked example | The maintained [order-pricing validation record](../../examples/order-pricing/VALIDATION.json) identifies its actual runtime snapshot, source baselines, finite contract tests and optional local rendering results. |

The compact historical illustration still contains the historical unsupported negative-minimum policy described in its PDR. A passing format-recognition check does not endorse that business rule. More generally, action recognition, word overlap, test-plan presence and clean exit codes do not prove semantic completeness or SOLID. The new [SOLID evidence guide](../../skills/mkl-cdr-review/references/solid-evidence.md) records bounded claims and challenges; it creates no automatic score or certification.

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

See [THIRD_PARTY_SOURCES.md](../THIRD_PARTY_SOURCES.md) for removed long quotations, retained bibliographic sources and remaining rights/provenance limits. All 18 root/per-skill LICENSE and NOTICE files retain their baseline bytes. This engineering cleanup does not assert legal clearance for every source-inspired adaptation, inherited asset or old release.

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
