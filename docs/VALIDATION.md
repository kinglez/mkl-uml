<!-- Copyright 2026 kingle.zhuang. Organization: mkl. -->
# Validation record

Validation date: **2026-10-29**. Candidate: **1.0.1**, based on source commit `f6f21221ef950371700e0db5860f3e94e077bc07` plus the reviewed local remediation changes. This record does not claim a published tag or successful remote CI for those uncommitted changes.

Local environment: macOS, Python 3.14.7 and 3.9.6, Node.js 26.1.0, npm 12.0.2, PlantUML 1.2026.7 / Graphviz 15.1.1, Claude Code 2.1.270. Author: kingle.zhuang, organization mkl.

## Executed checks

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

CI configuration runs assertions and smoke checks on Linux/Windows. No fresh hosted run was triggered for this local candidate; local results do not establish current remote-platform results.

## Corrected contracts

- Evidence must be substantive and usable, not just a supplied path. Empty/unrecognized supporting artifacts withhold full acceptance while independent checks continue. Comments and annotations cannot act as real review targets or coverage.
- PDR accounts for every supplied CU specification. CDR compares `(CU, local flow)` identities and executable branch evidence. Explicit release scope remains distinct from an individual artifact's identity.
- Stray fragment separators do not truncate sequence parsing. Manual activation checks resume after `autoactivate off`; automatic regions and bounded path sampling retain explicit limits.
- Ordinary business operation names are no longer exempted as accessors. Each parameter is checked independently, including nested generic types and quoted defaults.
- Header generation rejects input/output aliases, preserves supported aliases/derived properties/generic types/association and property bounds, and exposes unsupported conversions. Signal receptions remain classified annotations with an explicit language-specific mapping gap rather than invented Operations.
- Existing correction authorization, actual reviewer independence, evidence-first disposition and valid zero-finding results are consistent across deep references. Planning rates/counts and defect-density observations are not acceptance criteria.
- Positive examples now have correctly addressed replies, observable success/refusal outcomes, anchored alternatives and coherent description/date/reference data. Only the missing-flow diagnostic fragment in the shared fixture oracle required updating; no expected exit status was relaxed.

## Independent forward use

Two independent agents used all eight skills in isolated workspaces, without the audit's intended solutions. The first generated library-renewal domain/use-case/specification/robustness artifacts and rendered the three diagrams. All four validators passed; two justified robustness style/degree warnings were documented.

The second performed PDR/CDR preparation and authorized local corrections on a support-desk package, then generated a standalone CU-12 ticket interaction and design model. It preserved AD-02 internal-state provenance and separated Operations, a Signal reception, replies and creation. Applicable validators and rendering passed. It withheld formal acceptance where implementer, decision-maker and independent signoff evidence was absent.

Header inspection found two additional silent omissions during that use: reception signatures and optional property bounds. Four new regressions reproduced them; the corrected generator was replayed on the actual CU-12 model and independently re-reviewed on both Python versions. Original forward observations and the corrected replay are retained separately in the remediation evidence.

## Provenance and distributions

See [THIRD_PARTY_SOURCES.md](THIRD_PARTY_SOURCES.md) for removed long quotations, retained bibliographic sources and remaining rights/provenance limits. All 18 root/per-skill LICENSE and NOTICE files retain their baseline bytes. This engineering cleanup does not assert legal clearance for every source-inspired adaptation, inherited asset or old release.

The Python/Node installer and ZIP archives consume the shared payload builder. Offline payloads include the operating contract, source inventory and release notes; local links are rewritten within each skill. Build hashes accompany artifacts in `dist/SHA256SUMS`. Record the exact final source tree/patch and artifacts when creating a release; older `v1.0.0` installations do not receive unpublished changes.

## Reproduce

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
