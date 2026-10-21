<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Review protocol: how a PDR is conducted

> **Operational scope.** Default work uses lightweight checks of the requested artifact and affected links. This reference retains the fuller **opt-in formal MKL review** recipe and its historical source material. Apply its meeting roles, minutes, package metrics, disposition thresholds, and full checklist only when a formal review is requested. Missing material outside the selected scope is a disclosed check limitation, not an automatic blocker. Check available evidence and report concrete findings; do not require the entire pipeline, repeated self-audits, or two clean passes for an ordinary create/update/check task. Source quotations remain source claims; adaptations and numeric thresholds are MKL conventions, not certification requirements.

Rosenberg tells **what** to review (the ten guidelines). It doesn't tell **how** to conduct a review. That is provided by IEEE 1028-2008 and chapter 17 of Wiegers, and everything in this file comes from there.

Checkmark: IEEE clauses 1028 and 1016 cited here were read over the primary text. What could not be verified is declared as such in `sources-and-methods.md`.

---

## What type of review is a PDR

IEEE 1028-2008 defines five systematic types: management review (clause 4), technical review (5), **inspection (6)**, walk-through (7), and audit (8). “Systematic” requires three things: team involvement, documented results, and documented procedures.

A PDR fits either as **inspection** or **technical review**, depending on its formality. The practical difference: the inspection requires a checklist of anomalies and mandatory classification of those found; the technical review no. Since the PDR **has** a checklist—the ten guidelines—and **must** classify findings, this skill treats it as an inspection and applies clause 6.

Annex A of the standard confirms this indirectly: in its comparison of types, inspection is the only one that marks "yes" in the use of the anomaly checklist; the others have it as optional.

**Note on honesty.** The method's reference material allows the PDR to be formal (structured meeting with minutes) or informal (whiteboard review), and what matters is covering all ten guidelines. Applying clause 6 in full to an informal review would be overreaching. The skill adapts: **the rigor of the review procedure is proportional to the declared formality**, for independent scoped work select the applicable checks and disclose the limits. The full ten-guideline/five-metric record belongs to a requested formal package review.

---

## Review Anatomy (IEEE 1028 §1.5)

Every review type in the standard follows the same seven-part structure. It is the skeleton of the record:

1. Introduction
2. Responsibilities
3. **Input** — what material is reviewed
4. **Entry criteria** — authorization and event that initiates it
5. **Procedures** — planning, presentation, preparation, examination and recording, rework and follow-up
6. **Exit Criteria**
7. **Output** — the review record

The entry criteria for an inspection (§6.4.3) include two that are directly applicable here: that automatic error detection has already been executed, and that previous milestones are satisfied. For the opt-in formal package recipe, run applicable available validators before the session and record prerequisites. For an independent check, use supplied artifacts and continue available checks; do not require every upstream skill to have approved the inputs.

---

## Roles

IEEE 1028 §6.2 defines for inspection: inspection leader, secretary, reader, author, and inspectors. Wiegers describes the same four roles in more operational detail:

| Role | What does it do | Source |
|---|---|---|
| **Author** | Present the material. *"The author should not assume any of the other assigned roles—moderator, reader, or recorder."* | Wiegers |
| **Moderator / leader** | *"plans the inspection with the author, coordinates the activities, and facilitates the inspection meeting."* | Wiegers |
| **Reader** | *"the reader paraphrases the requirements and model elements being examined one at a time."* | Wiegers |
| **Secretary** | *"uses standard forms to document the issues raised and the defects found during the meeting."* | Wiegers |
| **Inspectors** | They examine; represent the affected perspectives | IEEE 1028 §6.2 |

That the reader **paraphrases** instead of reading literally is not a detail of style: it is what forces interpretation and brings out ambiguities. It is the spoken version of the highlighter test.

**The client.** The method requires your presence (guideline #4) because the PDR is your last entry point. If there is no customer available, a product representative can take over the role; What cannot be missing is **someone who validates that the language is understood without being technical**.

**The author's boss.** Wiegers: *"The author's manager normally should not attend an inspection meeting."* A review where the person is evaluated no longer finds defects.

---

## Team size

| Source | Figure |
|---|---|
| IEEE 1028 §6.1 | 2 to 6 participants, including the author |
| IEEE 1028 Annex A (inspection) | 3 to 6 |
| Wiegers | *"Try to limit the team to seven or fewer inspectors."* |

The three converge in a very similar range, although not identical: the upper limits are 6, 6 and 7. And Wiegers adds a counterintuitive nuance with empirical support: *"Research has shown that multiple inspection teams find more requirements defects than does a single large group"* — if there are many people available, it is better to **two small teams than one large**.

---

## Revision rate — the most important number for this file

**IEEE 1028 §6.5.2** sets the pace by document type. For our artifact:

| Document type | Rate |
|---|---|
| Architecture | 2-3 pages/hour |
| Requirements | 2-3 pages/hour |
| **Preliminary design** | **3-4 pages/hour** |
| Detailed design | 3-4 pages/hour |
| Source code | 100-200 lines/hour |

**A PDR reviews preliminary design.** The standard covers exactly our class of artifact: **3-4 pages per hour**. Wiegers offers a figure of the same order from another source: *"Two to four pages per hour is a practical guideline"* — with the scope qualification that follows.

**Scope notice about Wiegers' figure.** His "two to four pages per hour" appears in a chapter titled *"Reviewing requirements"*, within the planning of an inspection **of requirements documents**; the book never states it for design documents nor does it segment by type of document as IEEE 1028 does. The numerical match is real but **approximate and not matched by type of artifact**: the governing number here is that of IEEE 1028 for preliminary design. Wiegers further adds that *"the optimum rate for maximum defect-detection effectiveness is about half that rate"*, citing Gilb and Graham.

**Why pace decides effectiveness.** This is not a convenience recommendation: detection ability **plumbs** when reviewed faster. The most cited data is from Russell (*"Experience with Inspection in Ultralarge-Scale Developments"*, IEEE Software, January 1991): the defects found per thousand lines fell from 50 to 15 when the inspection rate tripled. **Second-hand quote** — it was read reproduced in an SEI technical report, not in the original article; see `sources-and-methods.md`. Reviewing above the sustainable rate does not produce a quick review: it produces a review that finds nothing, with the aggravating circumstance that it **issues a verdict anyway**.

**Operational consequence for this skill:** calculate the volume of the package, compare it with 3-4 pages/hour, and if it doesn't fit in a reasonable session, **say so and propose splitting the package**. Don't let the verdict be rendered on material that no one was able to actually look at.

**Duration of the meeting.** Wiegers: *"The inspection meeting shouldn't last more than about two hours; tired people aren't effective inspectors."*

---

## The stages, and where this skill fits

Wiegers describes five: planning → preparation → meeting → rework → follow-up.

**The data that justifies the existence of this skill** is in the second: *"Up to 75 percent of the defects found by an inspection are discovered during preparation"*. The meeting is not where the defects are found; It's where they remember.

The validator and automatic checks for this skill **are** the preparation phase. Coming to the session with the non-domain entities already listed and the non-behavior alternates already noted is exactly what the evidence says produces performance.

**Documented return** (Wiegers, citing Grady and Van Slack 1994): *"Several companies have avoided as many as 10 hours of labor for every hour they invested in inspecting requirements documents…"* — the original continues *"and other software deliverables"*, so the figure is not stated only for requirements documents.

---

## Exit and decision criteria

**IEEE 1028 §6.5.6.5** defines the exit decision of an inspection in three states. It is the verdict model of this skill:

| Standard Status | Skill Verdict |
|---|---|
| Accept | **Accepted** |
| Accept with rework verification | **Accepted with rework verification** |
| Reinspect | **Reinspection required** |

That there are **three and not two** matters: the intermediate state exists for the case in which the defects are real but limited, and it is enough to verify that the rework was done. Collapsing it to "approved/rejected" forces it to lie in one of two directions.

Wiegers adds the closing criterion: *"All issues raised during the inspection have been addressed."* And a brake: *"Don't ask anyone to review the same material more than three times"* — hence the metric *# revisions necessary* with goal ≤ 3. If it doesn't pass the third time, the problem is not in the review.

---

## Anomaly classification

**IEEE 1028 §6.8** makes the collection of data and the classification and ranking of anomalies **mandatory** for inspection. The standard uses: Catastrophic · Critical · Marginal · Negligible.

This skill maintains the severity taxonomy of the skill pack, for consistency with its four sisters, and declares the mapping:

| Skill Severity | IEEE 1028 §6.8 | Criterion |
|---|---|---|
| **Critical** | Catastrophic | Violates a hard rule or invalidates the package for detailed design |
| **Major** | Critical | Break correspondence between artifacts or leave behavior unspecified |
| **Moderate** | Marginal | Anti-pattern, excess detail, vocabulary drift |
| **Minor** | Negligible | Names, readability, presentation |

**The record of the review.** The mandatory content of the output of an inspection is in **IEEE 1028 §6.7**, and is what structures the `PDR-XX` record. That clause is used, and not ISO/IEC/IEEE 15289, for the reason explained in `sources-and-methods.md`.

---

## Checklists

**IEEE 1028 Annex A**: inspection is the only type of review that requires a checklist of anomalies; In the others it is optional. The ten PDR guidelines **are** that checklist.

Wiegers advises keeping them short—on the order of six or eight items—because long lists get skipped. The ten guidelines are at the limit of that recommendation, and that is why the minutes present them as a status table instead of as prose: so they can be checked systematically.

**A nuance of empirical evidence that is worth knowing.** In the code and requirements inspection literature, perspective-based reading usually outperforms checklist-based reading. But in the only controlled experiment we found **on UML design documents**, the result is reversed: reading by checklist detected more defects. That's one of the reasons why this skill is built as a checklist engine and not as an insights panel. The reference and its confidence level are in `sources-and-methods.md`.

---

## Regulatory bridge

**IEEE 1016-2009 §3.2.3** comes full circle: verification of a design description *"will usually be performed via review, inspection, or analysis (see IEEE Std 1028-2008)"*. That is, the design description standard explicitly refers to the reviews standard to say how a design is verified.

The same standard (§4.4) gives usable definitions of the two most lightly used adjectives: a design description is **complete** when each design concern is covered by at least one view, and **consistent** when there are no known conflicts between the elements of its views. The second is literally what the PDR checks between artifacts.

**ISO/IEC/IEEE 29148:2018 §6.3.3.7, NOTE 1** also refers to IEEE 1028 for the conduct of reviews. Your §5.2.5 and §5.2.6—individual and aggregate requirement characteristics—are used as quality vocabulary when judging use case text.
