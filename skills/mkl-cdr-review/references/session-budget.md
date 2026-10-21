<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Session budget and review self-check

> **Operational scope.** Default work uses lightweight checks of the requested artifact and affected links. This reference retains the fuller **opt-in formal MKL review** recipe and its historical source material. Apply its meeting roles, minutes, package metrics, disposition thresholds, and full checklist only when a formal review is requested. Missing material outside the selected scope is a disclosed check limitation, not an automatic blocker. Check available evidence and report concrete findings; do not require the entire pipeline, repeated self-audits, or two clean passes for an ordinary create/update/check task. Source quotations remain source claims; adaptations and numeric thresholds are MKL conventions, not certification requirements.

How much material fits in a review, at what pace, and **how to know if the review you just did was useful**. It is the part of this skill with the most empirical support and the least convention.

Everything quotable is transcribed here. Locators are for auditing, not consulting.

---

## The review rate table — IEEE 1028 §6.5.2, unabridged

This historical transcription is an explicit borrowing from the inspection clause; clause 5 provides no review-rate table. Its row/unit labels are preserved below, but the source-code and fixes rows mix PPH and LPH. The official table has not been rechecked here, so these units are **unresolved**, not a verified conversion or usable header estimate:

> *"The following table provides guidelines for typical inspection rates and anomaly recording rates, in terms of pages or lines of code per hour:"*

| Type of document inspected | Inspection rate |
|---|---|
| Architecture | 2 PPH to 3 PPH |
| Requirements | 2 PPH to 3 PPH |
| Preliminary design | 3 PPH to 4 PPH |
| **Detailed design** | **3 PPH to 4 PPH** |
| **Source code** | **100 PPH to 200 LPH** |
| **Test plan** | **5 PPH to 7 PPH** |
| Fixes and changes | 50 PPH to 75 LPH |
| User documentation | 8 PPH to 20 PPH |

> *"NOTE 1— Page per hour. NOTE 2— Lines (of code) per hour."*

**The three rows used by the CDR are in bold**, and there are three because the CDR touches three types of material:

| CDR material | Applicable row | Rate |
|---|---|---|
| `MC-XX` and `DS-XX` | *Detailed design* | **3-4 pages/hour** |
| Test plan / `CP-XX` (rule #1) | *Test plan* | **5-7 pages/hour** |
| Generated headers (rule #2), if authorized | *Source code* | **Unit unresolved in upstream transcription**; declare an actual project estimate until checked |

**This is more precise than what PDR uses**, which applies a single review rate (*preliminary design*, 3-4 PPH) to the entire package. It is not a defect of that skill: it reviews only one type of material. The CDR reviews three and that is why it needs three.

**Difference with Wiegers, declared.** Wiegers gives *"two to four pages per hour"* but **for requirements documents**, and adds that *"the optimum rate for maximum defect-detection effectiveness is about half that rate"*. Wiegers does not distinguish rates by artifact type; IEEE 1028 does. **The one that governs this skill is that of IEEE 1028.** That of Wiegers is cited because it converges in the same order of magnitude and because its nuance about the optimum points in the same direction as the empirical data below.

---

## Empirical data — GQM, RITME case

*The Goal Question Metric Method* (van Solingen & Berghout), Case B: **"REVIEW AND INSPECTION MEASUREMENT"**. It is a real field study on an industrial project: **378 failures, 43 hours of effort, 998 pages, 24 KSLOC**.

It matters because it is the **only measured evidence** of the corpus about reviews. The other sources provide guidance; this source supplies measured data.

### Expected performance

| Data | Value | Quote |
|---|---|---|
| Bugs per page in **design documents** | **0.4** | *"the number of faults detected by reviewing Project B was 0.4 faults per page equalling 24 SLOC. Grady reports that inspections resulted in 0.3 faults per page"* |
| Failures per hour, total | **8.75** | Compared to 0.34 for the acceptance test and 1.5 for the novice user test |
| Advantage of reviewing versus testing | **factor 25** | *"the effectiveness of reviewing over the acceptance test differs a factor 25… AT&T reported inspections to be a factor 20 more effective"* |
| Study's own performance objective | **7.5 faults/hour** and *"more than one fatal/major fault per hour"* | Conclusions from the feedback session |

### Size and speed limits — the finding that governs the budget

| Rule | Value | Quote |
|---|---|---|
| Length **unusable** | **> 50 pages** | *"Documents with more than 50 pages are unsuitable for reviews."* |
| Length **recommended** | **≤ 20 pages** | *"Results show a drop in review performance for documents larger than 20 pages"* · *"are more effective on documents of a maximum of 20 pages"* |
| Speed that **degrades** the result | **faster than 2 min/page** | *"When reviewing speed is faster than two minutes per page, results get reasonably lower."* |
| Average observed speed | **3 min/page**; **6 min/page** in word processor design documents | *"On average, reviewing takes three minutes per page."* … *"Reviewing design documents in text processor format takes twice as long: six minutes per page."* |
| Effect of experience | **×3** errors/hour, **×2** errors/page | *"Experienced reviewers detect over three times more faults per hour than less experienced reviewers."* |

**The mechanism, not just the correlation.** Two graphs from the study explain it together: effectiveness drops from ~2.5 errors/page in short documents to ~0.2 above 25 pages, and **time spent reviewing each page drops in parallel** from up to 15 min/page in short documents to 1-2 min/page in long ones. It is not that long documents have fewer defects: it is that **whoever reviews a long document skims it**. That's why splitting the package is not a convenience, it's what preserves performance.

**And defect density varies greatly between parts of the system**: in the ten subsystems measured it ranges from 2.4 bugs/page at worst to ~0 at best. A package is not homogeneous, and that is why triage is advisable (see `metrics-and-triage.md`).

---

## How the budget is calculated

1. **Measure the package.** Count the material by type: `MC-XX` + `DS-XX` equivalent pages, test plan pages, and—if authorized—headers. As a page equivalence for PlantUML artifacts, use **one page ≈ 40 effective lines** (no blank lines or comments), and **declare this to be the convention of this skill**: no source defines the equivalence between a diagram and a page of text.
2. **Apply the rate for the corresponding row.** Detailed design 3-4 PPH; test plan 5-7 PPH. Estimate headers separately from actual line volume and a declared project rate until the source-code units are verified.
3. **Add and compare with empirical limits.** If the design material exceeds **20 equivalent pages**, notify; If it exceeds **50**, say it clearly: above that the evidence says that the review stops working.
4. **Propose how to divide the material into sessions.** The rule expressly authorizes it (§5.1: *"may require more than one meeting"*). Distribute by use case, which is the natural unit of the checklist.
5. **Reserve time for preparation.** Wiegers: *"at least half as much time on individual preparation as is scheduled for the team inspection meetings"*, and no meeting of more than **two hours**.

**What is reported**, always with its quote: size measured by type · review rate applied and where it comes from · estimated hours · suggested number of sessions · and if the package exceeds empirical limits.

---

## Self-testing: the review judges itself

No sister skill has this, and it solves a real problem that this pack already paid for: **a happy-path fixture with no findings cannot demonstrate that a check is active**. A disabled validator and a working one produce the same output on correct material.

Using **0.4 bugs/page** as the base rate measured in design documents, the review itself can be judged:

| Situation | Reading |
|---|---|
| Findings ≈ 0.4/page | **Expected** performance. Nothing to point out |
| Findings far below baseline in a large package | **Coverage recheck candidate.** Low density alone cannot distinguish a careful review of mature material from a superficial review |
| Findings far above | The artifact is **immature**: perhaps the CDR should not have been convened yet |

**Operational rule.** If the package exceeds **10 equivalent pages** and the review produces **less than 0.1 findings per page** - a quarter of the base rate -, the skill **says so in the minutes**: not as a design error, but as a warning about confidence in the review, with the recommendation to review the rules that came out clean.

**The thresholds of this rule are skill convention**, derived from real data: 0.4 failures/page is measured; The cut in a quarter and the minimum of 10 pages are set by us to avoid warnings about tiny packages, where zero findings is perfectly normal. It is declared.

**Scope of the standards connection.** IEEE 1028 §6.9 calls for review-process data analysis: *"The preparation times, meeting times, and number of participants **shall** be analyzed to determine connections between preparation (checking) rate, meeting rate, and number and severity of anomalies found."* That supports analyzing the review process in a formal inspection. It does not mandate the 0.1 threshold, a probabilistic conclusion that the review failed, or a repeated audit loop; those are local heuristics and must be labeled as such.

---

## What the evidence does NOT say

It is as valid as the above, because it marks where one should not invent.

- **There is no total duration for a CDR.** Rosenberg does not give it; It was searched and it is not there. What there is are review rates and size limits, from which an estimate is derived — which is an estimate, not a measured duration.
- **The diagram↔page equivalence is not in any source.** The 40 lines per page are a convention of this skill.
- **The cut of 0.1 findings/page is ours.** The 0.4 baseline is measured.
- **RITME data are from a specific industrial project**, not a meta-analysis. They converge with Grady (0.3 failures/page) and with AT&T (factor 20 vs. factor 25 measured), which gives confidence in the order of magnitude — not the decimal.
- **There is debate about whether a meeting adds value** beyond individual preparation. It is mentioned so as not to consider settled what is not settled: this skill automates **the preparation**, where the evidence is solid, and leaves the form of the meeting to the user.

---

## Origin

| Source | Locator |
|---|---|
| IEEE Std 1028-2008 §6.5.2 (rate table), §6.9 (process analysis), §5.1 (multiple meetings) | Primary text read |
| van Solingen & Berghout, *The Goal Question Metric Method*, Case B “Review and Inspection Measurement” | Lines 2776, 2799-2811, 2819-2842, 2866-2867, 3420-3425, 3440, 3453-3459, 3470-3471 |
| Wiegers & Beatty, *Software Requirements 3rd ed.*, chap. 17 | Lines 6297, 6306-6308, 6316 |
