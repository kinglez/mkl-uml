# Architecture replay: author inspection - 2026-11-07

Scope: current frozen CU-01 baseline, PDR, C4 views/record, DS-01/DS-02, MC-01,
source modules and existing behavioral evidence. This section records the actual
primary author's inspection, not independent review or formal human acceptance.

- Requirements and oracle are unchanged. No production host, remote catalog, database,
  latency/SLA target, write lifecycle or new coupon policy was introduced.
- L1/L2 retain one quoting goal and local program; L3 identifies six logical groups;
  the catalog stays in process. L4 scopes a contract slice of discount_engine.
- ARC-01..ARC-06 cover all 23 RF/RN/RNF drivers; QS-01..QS-05 name observable existing
  checks. Mechanical reference coverage alone cannot prove their adequacy.
- Mapping inspection allocates all 17 MC-01 classifiers and 22 Python declarations;
  the actual allocation checker passes. Call arrows and source dependency ownership
  are explicitly distinguished.
- The initial L4 title contained an accidental physical newline. The class-profile
  checker reported no errors while PlantUML rejected it. The title was corrected;
  local syntax and rendering were rerun. This demonstrates separate syntax coverage,
  not a business or architecture change.
- The existing architecture/design choices are retained after source comparison;
  the new layer is a retrospective replay, not a claim about the original creation order.

The standalone L4 checker omits five provenance layers without domain/sequence/spec
inputs; the complete MC-01/DS-01 checks and explicit component mapping supply separate
coverage. Local source review and finite tests do not establish production readiness.

## Independent AI reinspection

A separate agent, `order_pricing_c4_review`, independently read the frozen business
sources, analysis/PDR, C4 artifacts, detailed design, current code and tests in isolated
copies. The following is an English repository adaptation of its actual 2026-11-07
report, not a signed original. Raw commands, snapshot hashes, probes and its full
report are retained in the external acceptance workspace for this replay.

### C4-IR-F01 - shared adapter helper allocation (Minor, closed)

The first map exclusively assigned parse_utc to request_boundary. The actual
InMemoryCatalog.lookup_coupon also calls it for trusted expiry text. This could imply
an unintended component dependency even though declaration counts were green.
The map now records a shared adapter helper with both actual consumers; brief and
L3 explain the reuse without inventing a seventh component or moving parsing into
the domain. The checker compares declared consumers with actual AST calls.
The independent reviewer ran the corrected map, removed catalog_snapshot in a copy
(exit 1), restored it (exit 0), and reinspected the rendered L3. Closed.

### C4-IR-F02 - overstated FE-02 response (Minor, closed)

The old FE-02 summary promised the unresolved Product code in the returned reason.
RF-09, CP-18 and current output require only UNKNOWN_PRODUCT and no successful quote.
The summary was corrected to that bounded contract, with a dated PDR-01-F02 entry.
The reviewer reread spec, oracle and source, reran spec/PDR checks, and confirmed all
11 frozen requirement/oracle/reference Python files remain unchanged. Closed.

### Examined correspondence and actual execution

The reviewer confirmed system/data meaning, one local runtime container, six logical
responsibility groups, scoped L4, stable identities, data ownership, eligibility before
discount invocation, fail-closed amounts, extension and small replaceable contracts.
It compared all 23 RF/RN/RNF inputs against actual DS/MC/source and the bounded oracle;
a count of linked IDs was not used as semantic proof.

Actual independent execution used Python 3.9.6 and local PlantUML 1.2026.9: C4 strict,
allocation, the then-current seven gate methods, standalone L4, complete MC/CDR profiles,
15 reference test methods / 30 oracle cases, existing code probes, runners, extension
and additional reviewer-only failure/substitution probes. Spec/PDR and changed L3 were
rechecked after corrections. The coordinator subsequently added the eighth gate for
shared-helper consumer omission. The reviewer did not claim to run Python 3.12 itself.

CDR produced zero errors and nine warnings. The reviewer examined the adapter handle
contract, tuple/association representation, value/result/refusal responsibilities,
reply semantics and RNF-03/05 evidence rather than treating warnings as approval or
requiring invented classes. Standalone L4 still leaves five provenance layers unexecuted;
full design/source correspondence is separate review evidence.

Technical recommendation: retain the design for this bounded example; both minor
findings are independently closed. Final reviewed snapshots must pin the actual
DS/MC/code inputs of this source-derived replay, and the combined verifier must pass
on that final set. This does not claim blind regeneration, universal SOLID, achieved
production qualities or formal human/business acceptance.

## Documentation correspondence and final snapshot recheck

The same independent reviewer read the project README, tutorial, reading guide, C4
guide, example README and replay guide. It checked 159 local links/anchors with no
missing target, and found four minor editorial issues. All were actually rechecked
and closed: E01 names the brief/mapping outputs that the next stage reads, with
proposed allocation labeled before code exists; E02 changes the stale Eight-steps
label; E03 limits bundled includes to C4 macro views; E04 distinguishes published
GitHub installation from this local candidate and supplies the local-checkout command.

The reviewer also reran all eight final example gate methods, and checked all three
reviewed handoffs read-only. At that inspection the architecture record pinned 35
source inputs, including the examined DS/MC/code/test evidence, and excluded design.json.
Final metadata/doc recording updates are rehashed by the coordinator only after this
actual reinspection; fresh combined verification supplies the current execution result.
The browser blocked file:// preview, so no interactive-browser acceptance is claimed.
Static HTML/tab targets/assets/JS syntax and actual diagram images are checked separately.
