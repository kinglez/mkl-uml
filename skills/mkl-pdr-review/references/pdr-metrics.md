<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# The five PDR metrics

> **Operational scope.** Default work uses lightweight checks of the requested artifact and affected links. This reference retains the fuller **opt-in formal MKL review** recipe and its historical source material. Apply its meeting roles, minutes, package metrics, disposition thresholds, and full checklist only when a formal review is requested. Missing material outside the selected scope is a disclosed check limitation, not an automatic blocker. Check available evidence and report concrete findings; do not require the entire pipeline, repeated self-audits, or two clean passes for an ordinary create/update/check task. Source records identify historical influences; adapted procedures and numeric thresholds are MKL conventions, not certification requirements.

For an explicitly requested formal PDR, calculate applicable metrics and publish their method and scope in the minutes. Ordinary checks report relevant measurements without requiring the full five-metric gate. A measure without a published method is unverified; disposition depends on sufficient evidence and confirmed findings, with metrics directing investigation.

**Overall goal of the method:** A successful PDR ends with **zero non-domain entities** and **zero non-behavioral alternate courses**. It is a criterion of acceptance, not aspiration.

---

## 1. Highlighter coverage percentage

**What it measures.** What proportion of the steps in the use case text have identifiable correspondence in the robustness diagram. It quantifies guideline #10.

**How to calculate it (lexical approximation).** For each numbered step of the basic flow and each alternative or exception flow, its significant terms are searched—discarding stop words—among the element names and relationship labels of the diagram. A step counts as covered if its overlap exceeds the declared threshold.

**Goal.** Complete coverage: every step of the text has its counterpart, and every element of the diagram has its phrase.

**Limits, which must be published next to the number.** This metric is **indicative**:

- 100% **does not** prove that the diagram is correct: it proves that the words match.
- Low coverage may be due to legitimate synonyms—the text says "verifies," the diagram says "validates"—and not a defect.
- It does not detect the reverse direction with the same reliability: an element of the diagram that is left over is more difficult to see due to overlap than an uncovered step.

**The actual highlighter test is done by the reviewer**, sentence by sentence. The number is a map of where to look first, not a verdict. When published, it is accompanied by this warning; never alone.

---

## 2. Number of non-domain entities

**What it measures.** How many Entity-type objects appear in some package robustness diagram and **do not** exist as a class in the domain model. It is guideline #9 expressed numerically.

**How to calculate it.** Deterministic: set of entities from all robustness diagrams, minus the set of domain model classes, comparing by normalized key—no accent marks, no capital letters, no separators—so that `CartLine`, `Cart Line`, and `cart_line` count as the same.

**Formal package goal: 0.** A confirmed non-zero value prevents an unqualified full-package `Accepted` disposition. Distinguish an unincorporated, disclosed domain discovery delta from invented concepts; boundaries and actors have separate origins and are not counted as missing domain entities.

**The reverse sense is information, not a defect.** The domain classes that this package does not use are reported separately: they may be the scope of other use cases, or they may indicate that the domain model grew too large. They are never counted as a defect.

**Known risk of normalized comparison:** two genuinely different concepts with very similar names can be confused. That's why the report lists **the names as they appear on each artifact**, not the normalized key, so that the person can break the tie.

---

## 3. Number of alternate courses without behavior

**What it measures.** How many `FA-XX` or `FE-XX` are declared in the specification but **do not** have their behavior specified, or do not appear as a branch in the diagram. It quantifies guideline #7: alternate and exception handling needs explicit coverage within its parent use case.

**How to calculate it.** Two different checks that add up:

- **No branch:** the identifier is in the specification and does not appear on any diagram labels. The spellings are normalized: `FA-01`, `FA1`, `FA 1` and `fa_01` count as the same.
- **No behavior:** the alternate is declared but its text block does not describe behavioral steps — it only states the condition.

**Formal package goal: 0.** A confirmed non-zero value prevents an unqualified full-package `Accepted` disposition; assess the specified behavior rather than merely matching flow labels.

**Why it matters more than it seems:** A no-behavior alternate may leave required handling unspecified. The defect does not manifest itself in the diagram, it manifests itself in production.

---

## 4. Number of syntax violations

**What it measures.** Banned links and other violations of the hard rules of robustness analysis, added to all diagrams in the package. It is guideline #5 expressed numerically.

**How calculated.** Connection rules are property of `/mkl-uml-robustness-diagram`; here they are consumed and counted. Count every arc that joins a forbidden pair, every element without a recognizable type, and every diagram without Controllers.

**Goal: 0.** This is the strictest metric of all: a syntax violation allows no nuance, and the source itself warns that a diagram that cannot be expressed with these rules is signaling ambiguity or incompleteness in the use case.

---

## 5. Number of revisions necessary

**What it measures.** How many times the same use case has been reviewed again. It is the only metric that is **not** calculated from the artifacts: it is carried from session to session.

**Planning interpretation.** Wiegers motivates limiting repeated examination of the same material to manage reviewer fatigue. The inherited suggestion of three reviews is a planning aid, not a required minimum, automatic rejection threshold or mandatory split.

Repeated unresolved findings justify investigating artifact clarity, scope and reviewer capacity. Split a use case only when its behavior and goals support that change. Record a proportionate next action; rerun affected checks after a correction without requiring unchanged material to pass a fixed cycle count.

---

## Evidence eligibility before disposition

Keep evidence coverage and demonstrated defects separate. Applicable evidence includes human/semantic checks: being non-automatable does not mean already performed. A clean script preparation result can coexist with **Not fully verified** formal coverage.

| Condition | Formal treatment |
|---|---|
| An applicable layer lacks readable substantive input or actual reviewer evidence | **Not fully verified**. Identify the gap and continue independent checks; report known blocking defects as well. |
| Verified critical/major findings, non-domain Entities, undesigned alternatives or profile violations remain | **Reinspection required** for the affected design. No favorable aggregate metric cancels a demonstrated defect. |
| Applicable checks have evidence and only bounded agreed rework remains | **Accepted with rework verification**, with owner, due date, explicit correction and verification criteria. |
| Applicable checks have evidence, required semantic coverage is confirmed and blocking findings are closed | **Accepted**, subject to any separately identified organizational sign-off. |

Optional evidence outside a standalone check's selected scope is a disclosed limit, not an automatic failure. In a full formal package review, missing domain/actor evidence or absent stakeholder interpretation cannot be treated as minor rework or excused merely because it is not automatable.

Lexical coverage floors are local investigation heuristics, not semantic acceptance thresholds. Confirm uncovered steps and their consequence before classifying a finding. For example, missing required behavior is substantive rework, while an unrecognized synonym can be a dismissed candidate with evidence. Record which interpretation was verified.

Zero findings is valid. Repeat or broaden examination only for changed artifacts, actual gaps or new evidence; elapsed time and a fixed cycle count do not alter criteria.

## Session budget

Publish a session estimate when it helps plan the requested formal review. It does not determine design validity or evidence coverage.

**How to calculate.** State the page-equivalence convention and selected project review rate. Upstream notes attribute **3–4 pages/hour** for preliminary design to IEEE 1028 §6.5.2; this is inherited planning context, not a newly verified mandatory pace or a universal capacity limit.

**What is it for?** Compare scope, preparation and reviewer availability; propose smaller sessions where useful. Actual skipped checks or insufficient evidence limit coverage. Elapsed time or departure from a historical rate alone cannot establish superficial review, require a finding quota or decide acceptance.
