<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# The five PDR metrics

> **Operational scope.** Default work uses lightweight checks of the requested artifact and affected links. This reference retains the fuller **opt-in formal MKL review** recipe and its historical source material. Apply its meeting roles, minutes, package metrics, disposition thresholds, and full checklist only when a formal review is requested. Missing material outside the selected scope is a disclosed check limitation, not an automatic blocker. Check available evidence and report concrete findings; do not require the entire pipeline, repeated self-audits, or two clean passes for an ordinary create/update/check task. Source quotations remain source claims; adaptations and numeric thresholds are MKL conventions, not certification requirements.

For an explicitly requested formal PDR, calculate the applicable metrics and publish their method and scope in the minutes. Ordinary checks report only relevant measurements and do not require the full five-metric gate. A metric without a published method is not verifiable, and in a gate that is unacceptable: the verdict is derived from these numbers.

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

**What it measures.** How many `FA-XX` or `FE-XX` are declared in the specification but **do not** have their behavior specified, or do not appear as a branch in the diagram. It is guideline #7 expressed numerically, and the source supports it: the alternate courses represent more than half of the complexity of the software.

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

**Goal: ≤ 3.** The limit comes from Wiegers: it is not advisable to ask anyone to review the same material more than three times, because reviewer fatigue degrades detection.

**How to interpret it.** A use case that makes it to the third revision without passing does not have a revision problem: it has an artifact or scope problem. The usual reading is that **the use case should be split**, which is consistent with the method's own recommendation when a diagram grows too large.

When the limit is reached, the minutes say so explicitly and propose splitting the use case, instead of calling a fourth round.

---

## From number to verdict

The thresholds are applied in this order. It stops at the first condition that is met:

| Order | Condition | Verdict |
|---|---|---|
| 1 | Any **critical** or **major** open findings · or entities without domain > 0 · or alternates without behavior > 0 · or syntax violations > 0 · or coverage **below the floor** | **Reinspection required** |
| 2 | Only moderate or minor findings, **all** with agreed correction, responsible party and date · or layers not executed · or coverage **above the floor but incomplete** | **Accepted with rework verification** |
| 3 | Zero critical and major findings, all three hard metrics at zero, **complete** coverage | **Accepted** |

**Two partial layer classes, and only one degrades the verdict.** The distinction matters, and the validator implements it with an explicit list of degraded layers, not guessing from the state text:

| Class | Example | Does it degrade? |
|---|---|---|
| **Partial due to absent input** | Without a use case diagram, actor-diagram consistency is not checked; without a domain model guideline #9 does not run | For a requested full-package formal review, qualify that package disposition. For an independent scoped check, report the limitation without treating out-of-scope optional material as a failure |
| **Partial by nature** | Guideline #4 is not automatable; half of #8 needs a wireframe that the script doesn't even accept as an argument | **No.** Treating it as a degradation would make `Accepted` unattainable even if you contribute everything |

A real bug from a previous version illustrates this: the layers were declared as not executed, they were printed in the report, and the verdict came out `Accepted` anyway **because the function that calculated it did not receive the layers**. Declaring the truth and then ignoring it is the same lie by omission that this gate claims to combat, achieved through another means. It was uncovered by an audit that actually invoked the skill on a package that was missing two inputs.

**Two coverage thresholds, not one.** It is advisable not to confuse them: there is a **floor** below which the verdict is forced to be re-inspected, and a **complete coverage requirement** to be able to accept. Between the two remains the band of the intermediate state: the package is usable but there is text without a counterpart in the diagram, and that is rework with the person responsible and the date, not a clean pass. The validator checks the two conditions **separately and directly**; If it were based on the fact that the warnings already push the intermediate state, the criterion would be broken as soon as the treatment of the warnings changed.

**The order is deliberate.** The rejection condition is evaluated first so that no unfavorable result is upgraded by accumulation of favorable cases.

**No metric relaxes due to exhaustion.** Neither time, number of internal cycle passes, nor session pressure change a threshold. If the package fails, the verdict is `Reinspection required`, and that is a valid and useful result — not a failure of the skill.

## Session budget

It is not one of the five, but it is published alongside them because it conditions the validity of all of them.

**How to calculate.** Package volume—equivalent pages of specification plus diagrams—versus the rate of **3-4 pages/hour** that IEEE 1028 §6.5.2 sets for preliminary design.

**What is it for?** If the package does not fit in a reasonable session, the minutes say so and propose splitting it. Reviewing above the sustainable pace does not speed up the review: it makes the examination superficial while still producing a verdict. A record that cannot justify that there was time to look at the material is stating less than it appears.
