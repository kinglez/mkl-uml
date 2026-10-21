<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Metrics and triage — what can be measured and what can't

> **Operational scope.** Default work uses lightweight checks of the requested artifact and affected links. This reference retains the fuller **opt-in formal MKL review** recipe and its historical source material. Apply its meeting roles, minutes, package metrics, disposition thresholds, and full checklist only when a formal review is requested. Missing material outside the selected scope is a disclosed check limitation, not an automatic blocker. Check available evidence and report concrete findings; do not require the entire pipeline, repeated self-audits, or two clean passes for an ordinary create/update/check task. Source quotations remain source claims; adaptations and numeric thresholds are MKL conventions, not certification requirements.

This reference exists for a specific reason: **to prevent the skill from inventing thresholds**. A number without origin on an artifact that promises traceability is exactly the defect that the CDR looks for in others.

House rule: **every number either has a quote, or is labeled as a convention of this skill.** There is no third option.

---

## 5/20/80 triage — the only supported quantitative criterion

From *Software Measurement* (Ebert & Dumke), §9.3.3 *Identifying Error-Prone Components*, line 4805:

> *"The most critical and most complex, for instance, **the top 5%**, of the analyzed modules are candidates for a **redesign**… **The top 20%** should have a **code inspection** instead of the usual code reading, and **the top 80%** should be at least entirely (C0 coverage of 100%) **unit tested**."*

And the fact that justifies it (line 4757):

> *"An analysis of many projects revealed the applicability of the **Pareto rule: 20-30% of the modules are responsible for 70-80% of the malfunctions** of the whole project."*

**Why it works in a CDR.** It is not a quality threshold: it is an **attention distribution rule**. A package is not homogeneous—RITME data measures 2.4 failures/page in the subsystem with the highest defect density and ~0 in the best—so checking everything with the same intensity wastes effort where there are no defects and skimps on it where there are.

**How to adapt to classes of a design model:**

| Section | What to do in the CDR |
|---|---|
| **Top 5%** | Candidates for **redesign**: they are discussed in Act II as their own group |
| **Top 20%** | **Detailed inspection** of all your operations and relationships |
| **80% remaining** | Mechanical checks and verification that each operation has a test case |

**How they are ordered.** By size (operations + attributes) and coupling (incoming and outgoing relationships). **The ordering formula is declared to be a convention of this skill**: the source sorts by complexity and change history, which do not exist before coding. What is preserved from the source is the 5/20/80 distribution, not the order metric.

**Honest disclaimer about origin.** The text talks about **code modules**, not classes of a model. The transposition is ours and is declared. What makes it defensible is that the criterion is **proportional distribution**, not an absolute threshold: it does not say "more than N operations is bad", it says "dedicate more attention to the top 5%", and that holds the same over classes.

---

## CK metrics — what they are and what they are for here

From *Software Measurement*, §10.4, lines 5828-5835:

| Metric | verbatim definition |
|---|---|
| **WMC** — Weighted Method per Class | *"the sum of complexities of all methods in a class"* |
| **DIT** — Depth of Inheritance Tree | *"the maximum length of the inheritance tree up to the root"* |
| **NOC** — Number of Children | *"All direct sub-classes subordinated to a class"* |
| **CBO** — Coupling between Objects | *"direct coupling of objects… The usage of methods or instance variables of the other class is counted"* |
| **RFC** — Response for a Class | *"the size of the response set of a class"* |
| **LCOM** — Lack of Cohesion in Methods | *(see warning below)* |

**Which ones to look at first.** The corpus brings correlation data with defect propensity: **DIT, RFC and CBO** are the ones with the strongest and most consistent correlation; **NOC** is uncertain; **LCOM** came out weak in the cited study. If you have to prioritize, you start with inheritance depth, response set size, and coupling.

**⚠ LCOM warning.** The formula is **corrupt in the corpus markdown**: it is missing the intersection symbol and the similarity function arguments. **Not cited or implemented from there.** If formal LCOM is ever needed, it is checked against Chidamber & Kemerer (1994) directly. It is left written so that no one copies it from the corpus believing it is correct.

**What is actually used in the validator.** Only what can be reliably counted about a `.puml`: number of operations and attributes, depth of inheritance, and incoming and outgoing relationships as an approximation to CBO. **WMC is not calculated** —it requires the complexity of each method, which a design model does not have—, and neither is **RFC**, for the same reason. To say that they are calculated would be false.

---

## Thresholds: what exists and what does not

### There is no cyclomatic complexity threshold in the corpus

It was explicitly searched. *Software Measurement* defines the metric (lines 4785-4791) — *"Cyclomatic complexity thus highly correlates with poor software quality"* — but **does not give any number**, neither McCabe's classic nor any other.

And the standard that does address it **delegates the threshold to the organization**. ISO/IEC 25023 §8.8.1, measurement MMo-2-S *Cyclomatic complexity adequacy*:

> *"X = 1 – A/B; A = Number of software modules which have a cyclomatic complexity score that **exceeds the specified threshold**"*
> **NOTE:** *"Such a threshold is used to determine whether a value of cyclomatic complexity is acceptable or not for each module. **This is defined by each project or organization**…"*

**Consequence for this skill:** if someone asks about the complexity threshold, the answer is **"the corpus does not set it and the standard delegates it to your organization"**, not a made-up number. The standard gives the **formula**; You set the threshold.

The same with the other measure in the same table, MMo-1-G *Coupling of components*: `X = A/B`, where A are the components implemented without impact on others. The formula is normative; the target belongs to the project.

### And the comparison thresholds are not normative either

*Software Measurement* brings observed values on Java standard libraries (95% confidence interval): DIT 0.57-0.61 · NOC 0.14-0.16 · WMC 8.54-8.85 · CBO 2.92-3.09 · RFC 14.45-15.10. **They are a comparative reference, not objectives.** And the book itself warns: *"a step in planning a measurement process is measurement adjustment which involves determination of the favorable values and **tuning of the thresholds**"*.

---

## The bridge with ISO 25010

Why looking at coupling and cohesion in a design review is not a hobby but a consequence of the definition of maintainability. ISO/IEC 25010, *Modularity* subcharacteristic note:

> *"Modularity implies that the product is composed of discrete modules or components with **cohesive content and minimal coupling** to other modules or components."*

And the maintainability subcharacteristics that a class model already determines, with its definition:

| Subfeature | verbatim definition |
|---|---|
| **Modularity** | *"capability of a product to limit changes to one component from affecting other components"* |
| **Reusability** | *"capability of a product to be used as assets in more than one system"* |
| **Analysability** | *"capability of a product to be effectively and efficiently assessed regarding the impact of an intended change… or to identify parts to be modified"* |
| **Modifiability** | *"capability of a product to be effectively and efficiently modified without introducing defects or degrading existing product quality"* |
| **Testability** | *"capability of a product to enable an objective and feasible test to be designed and performed"* |

**Testability is what closes the circle with rule #1.** The course reaches the same conclusion from practice: *"A design that is easy to test is usually more modular, more maintainable, less coupled. On the contrary, designs that are difficult to test usually hide structural problems."*

**A notice from the course material itself**, which should be kept in mind: *"ISO 25010 defines characteristics and subcharacteristics, but **does not provide specific quantitative metrics**; these must be designed or selected in each project."* It serves as a vocabulary to organize findings, not as a measurement scale.

---

## How to decide a threshold, if one is needed

ISO/IEC/IEEE 15939 defines the mechanism, and is the one that avoids inventing:

> **decision criteria** — *"thresholds, targets, or patterns used to determine the need for action or further investigation, or to describe the level of confidence in a given result"*
> *"Decision criteria may be derived from **historical data, plans, and heuristics**, or computed as **statistical control limits** or statistical confidence limits."*

And its Annex A brings an already solved example that is almost this case — *"Evaluate product quality during design"*, with indicator *design defect density* and criterion *"Results outside the control limits require further investigations"*.

**What this skill takes from there:** the review self-check (`session-budget.md`) is exactly a defect density with decision criteria — its criteria come from measured data (0.4 faults/page) and not from calculated control limits, because there is no historical series. It is declared like this.

---

## Summary: what numbers does this skill use and where do they come from?

| Number | Origin | Status |
|---|---|---|
| 3-4 pages/hour (detailed design) | IEEE 1028 §6.5.2 | **Regulatory** |
| 5-7 pages/hour (test plan) | IEEE 1028 §6.5.2 | **Regulatory** |
| 100 PPH / 200 LPH (code) | IEEE 1028 §6.5.2 | **Regulatory** |
| 0.4 errors/page in design | GQM, RITME case | **Measured** |
| Maximum 20 pages · unusable > 50 | GQM, RITME case | **Measured** |
| Degradation below 2 min/page | GQM, RITME case | **Measured** |
| Preparation ≥ 50% of meeting time | Wiegers chap. 17 | **Quoted** |
| Meeting ≤ 2 hours | Wiegers chap. 17 | **Quoted** |
| No more than 3 reviews of the same material | Wiegers chap. 17 | **Quoted** |
| 5/20/80 distribution | Ebert & Dumke §9.3.3 | **Quoted**, transposed from modules to classes *(stated)* |
| 1 page ≈ 40 effective lines of `.puml` | — | **Convention of this skill** |
| Warning below 0.1 findings/page in packs > 10 pages | — | **Convention of this skill**, about 0.4 measured |
| God class thresholds | — | **Convention of this skill.** Warnings only |
| Cyclomatic complexity threshold | — | **DOES NOT EXIST.** The corpus does not fix it; ISO delegates it to the organization |

---

## Origin

| Source | Locator |
|---|---|
| Ebert & Dumke, *Software Measurement* | §9.3.3 (4757, 4805), §10.4 (5828-5835), §13 (8535-8566), cyclomatic complexity (4785-4791) |
| ISO/IEC 25023:2016 | §8.8.1, MMo-1-G and MMo-2-S measurements |
| ISO/IEC 25010 | *Modularity* Note and Maintainability Subcharacteristics |
| ISO/IEC/IEEE 15939:2017 | Definition of *decision criteria* and Annex A.3.2 |
| Course material, *Quality models* | The warning that ISO 25010 does not include metrics |
