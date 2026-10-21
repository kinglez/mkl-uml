<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Audit gate: seven layers

> **Operational scope.** Default work uses lightweight checks of the requested artifact and affected links. This reference retains the fuller **opt-in formal MKL review** recipe and its historical source material. Apply its meeting roles, minutes, package metrics, disposition thresholds, and full checklist only when a formal review is requested. Missing material outside the selected scope is a disclosed check limitation, not an automatic blocker. Check available evidence and report concrete findings; do not require the entire pipeline, repeated self-audits, or two clean passes for an ordinary create/update/check task. Source quotations remain source claims; adaptations and numeric thresholds are MKL conventions, not certification requirements.

Optional checklist for an explicitly requested formal MKL audit. For ordinary work apply only the checks relevant to the requested artifact and affected links. The cited design/development guidance calls for verified outputs before acceptance and subsequent use (ISO/IEC/IEEE 90003 §8.3.4.2). See `sources-and-methods.md` for verification qualifications.

Optional formal cycle: **construct → audit selected layers → correct supported findings → recheck affected evidence**. Record actual coverage and residuals; clean passes do not guarantee correctness.

## Layer 1: syntax and hard rules — delivery criterion

Run the following, replacing `diagram.puml` and `domain_model.puml` with actual input paths:

```bash
python3 scripts/validate_robustness_puml.py diagram.puml --domain domain_model.puml
```

- [ ] **Zero errors.** These are deterministic connection-rule violations, not reviewer preferences.
- [ ] Address each warning or justify it in writing.
- [ ] If execution is unavailable, **state that in the certificate**; an unexecuted layer must remain visible.

## Layer 2: text ↔ diagram correspondence — Highlighter Technique

Walk the use case text **one sentence at a time**, highlighting it and marking corresponding diagram elements.

- [ ] **All text is highlighted**: no use case behavior is missing from the diagram.
- [ ] **All diagram elements are highlighted**: nothing lacks textual support.
- [ ] Explicitly report residuals. Remove unsupported elements; add omissions, or record an ambiguity when the text is at fault.
- [ ] When presentation evidence is available, show use case text, diagram, and interface evidence. GUI wireframes validate screens; API/webhook contracts, message schemas, and device protocols validate machine boundaries. Missing optional interface evidence is recorded as an unexecuted check.

**Optional visible correspondence:** number labels with their textual step, such as `1. select Register Author` or `7. generate confirmation`. This makes the highlighter check visible within the diagram and can help academic deliverables, but is not mandatory.

## Layer 3: method guidelines

Apply the **six steps toward better preliminary design**:

- [ ] Diagram matches use case text.
- [ ] Diagram obeys robustness-analysis rules.
- [ ] Diagram focuses on **logical flow**.
- [ ] Diagram includes **every alternative course**.
- [ ] No design-pattern-itis.
- [ ] Diagram stays at preliminary rather than detailed design level.

Apply relevant robustness and PDR guidance:

- [ ] Place use case text beside the diagram.
- [ ] Take entities from the domain model and record missing entities in the delta.
- [ ] Use clearly named human or machine boundaries at the chosen interface level.
- [ ] Treat controls as logical functions rather than controller classes.
- [ ] Make data movement between entities and screens traceable.
- [ ] Cover **both sides of the user/system dialogue**.
- [ ] Specify alternative behavior, rather than merely mentioning it.
- [ ] Reserve sequence-level detail for the sequence diagram.

## Layer 4: anti-patterns

- [ ] No catalog entry in `anti-patterns.md` remains without explicit justification.

Quick scan: noun-to-noun connections; rogue controls grounded in neither domain nor text; widget boundaries; verbs disguised as boundaries; missing alternatives; inheritance or operations; generic presentation controls; premature design patterns.

## Layer 5: traceability

The source record grounds design/requirement/entity traceability in ISO/IEC/IEEE 12207 §6.4.5.2 h and §6.4.5.3, with bidirectional links to verification methods. It records these clauses as **verified against primary text**; see `sources-and-methods.md` for provenance.

Use the existing **`DR-XX`** and element-ID mappings when supplied. Allocate `B-01`/`C-01`/`E-01`-style IDs only for genuinely new identities; preserve IDs across rename/layout changes, mark deleted identities retired, and never reuse or renumber them silently. Verify references resolve to the current item or an explicit retirement/replacement record. For standalone work allocate only the requested artifact's new identities; do not fabricate upstream reservations.

Minimum matrix, without unexplained orphans:

| ID | Element alias | ← Textual sentence | ← Domain/actor origin | → Sequence/test destination |
|---|---|---|---|---|
| `B-01` | `B_...` | Step N | Named human/machine interface evidence | Sequence instance |
| `C-01` | `C_...` | Step N (verb) | — | Message + **one test case** |
| `E-01` | `E_...` | Step N (noun) | Domain class or discovery delta | Sequence instance |
| `ACT-01` | `ACT_...` | — | Use case diagram actor | — |

Pipeline identifier chain: `RF-XX` → `CU-XX` → flow step (`FA-XX`/`FE-XX` where applicable) → **`DR-XX`** + element (`B-/C-/E-`) → sequence message (`DS-XX`) → test case. The original ID prefixes remain stable for cross-artifact compatibility.

- [ ] Every element has an origin.
- [ ] Every textual sentence has a corresponding element.
- [ ] Every entity exists in the domain model or reported delta.

## Layer 6: information item quality

ISO/IEC/IEEE 12207 §6.3.6 gives seven quality criteria, recorded as **verified** in the upstream source review. The corresponding 16326 coverage remains pending verification.

- [ ] **Unambiguous:** precise names; no unexplained generic “screen,” “data,” or “information.”
- [ ] **Complete:** basic and all alternative courses; all text represented.
- [ ] **Verifiable:** checkable against text (layer 2) and by script (layer 1).
- [ ] **Consistent:** vocabulary agrees with domain model and specification.
- [ ] **Modifiable:** regular structure and aliases support safe editing.
- [ ] **Traceable:** satisfies layer 5.
- [ ] **Presentable:** readable when rendered, without unnecessary crossings or overload.

## Layer 7: input/output conformance

The cited acceptance criterion is that each stage's inputs are **correctly reflected** in its outputs (ISO/IEC/IEEE 90003 §8.3.5; clause verification status is recorded separately).

- [ ] Every specification step has a representation.
- [ ] Entities derive from the domain model or discovery delta.
- [ ] Actors and invoked cases agree with the use case diagram.
- [ ] Nothing contradicts the stated scope in the business description.
- [ ] Every element has identifiable provenance; no invented behavior.

## Optional formal completion criteria

For an explicitly requested formal audit, the following are MKL reporting thresholds. They do not establish absence of defects or UML/ISO certification:

| Condition | Threshold |
|---|---|
| Critical findings | **0** |
| Major findings | **0** |
| Minor findings | **≤ 2**, documented and justified |
| Traced basic, alternative, and exception steps | **100%** |
| Recheck of corrected findings | Record the actual affected checks; no fixed number of clean passes |

**Optional audit budget: at most five scoped correction/recheck rounds.** Stop earlier when the requested scope is checked; disclose unresolved findings. A budget is not a requirement to perform five or two passes.

### `AUDIT NOT PASSED`

If critical or major findings remain at the limit, report **`AUDIT NOT PASSED`**, deliver the best available result, and include:

- Open findings grouped by severity.
- The **input or user decision needed to close each finding**; for example, “the specification does not define payment failure behavior; an alternative course is required.”

This prevents success being declared merely because the iteration budget is exhausted. A falsely converged certificate discourages human review precisely where it is needed.

### Why a limit exists

The technique is intended to take approximately ten minutes per diagram. If the diagram continues growing on the third pass, **split the use case**. Document genuine dilemmas as justified exceptions instead of iterating without an end.

## Audit certificate template

```markdown
### Audit certificate — [DR-XX] · [CU-XX Use case name]

**Passes:** N of 5 · **Status:** converged / converged with exceptions / **AUDIT NOT PASSED**

**Closure:** critical N · major N · minor N · traceability N% within declared scope · affected corrections rechecked [details]

| Layer | Result | Note |
|---|---|---|
| 1. Hard rules (script) | 0 errors, N warnings | Or: not executed — reason |
| 2. Text ↔ diagram | Complete coverage | Residuals and resolution |
| 3. Method guidelines | Passed | |
| 4. Anti-patterns | None | |
| 5. Traceability | No unexplained orphans | |
| 6. Information item quality | 7/7 | |
| 7. Input/output conformance | Passed | |

**Corrections by pass**
- Pass 1 → 2: [correction and rationale]
- Pass 2 → 3: [...]

**Declared exceptions**
- [Decision, rejected alternative, and reason]

**Unresolved decisions, only if needed**
- State ambiguity, why evidence cannot resolve it, and the specific decision required.
- Apply already authorized supported corrections/discovery deltas and record them; no blanket confirmation step.
```

Report unexecuted layers and unresolved decisions honestly. Those qualifications make the remaining evidence usable.
