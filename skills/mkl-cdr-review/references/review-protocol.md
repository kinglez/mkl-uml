<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Review protocol: how it is conducted

> **Operational scope.** Default work uses lightweight checks of the requested artifact and affected links. This reference retains the fuller **opt-in formal MKL review** recipe and its historical source material. Apply its meeting roles, minutes, package metrics, disposition thresholds, and full checklist only when a formal review is requested. Missing material outside the selected scope is a disclosed check limitation, not an automatic blocker. Check available evidence and report concrete findings; do not require the entire pipeline, repeated self-audits, or two clean passes for an ordinary create/update/check task. Source quotations remain source claims; adaptations and numeric thresholds are MKL conventions, not certification requirements.

Rosenberg says **what to review**. This reference tells **how the session is conducted**, and where each rule comes from.

**All quotes are transcribed in full here.** There is no need to open any rule or book to apply this skill: the line and clause numbers are there so that whoever has the sources can audit them, not because the skill needs them. The quotes are in their original language—so they are verifiable—with the English explanation next to them.

---

## First thing: this is a technical review, not an inspection

The distinction is not terminological. IEEE 1028 dedicates a clause to each type of review, with **different** roles, criteria, and outputs. Choosing the wrong clause produces a record with the wrong fields.

**The source of the method itself says it.** Rosenberg, line 4545:

> *"the customer should not be involved in the CDR—just the designers and developers. **It's a technical review session.**"*

And the course material repeats it: *"The CDR is a technical review whose objective is to ensure that the design is correct, consistent, and detailed enough to be implemented with confidence."*

**The standard confirms this through its stated purpose.** IEEE 1028 §5.1 lists the products subject to technical review, and among them is *"Software design description"* — exactly what the CDR examines.

> §5.1 — *"The purpose of a technical review is to evaluate a software product by a team of qualified personnel to determine its suitability for its intended use and identify discrepancies from specifications and standards. It provides management with evidence to confirm the technical status of the project. Technical reviews may also provide the recommendation and examination of various alternatives, which may require more than one meeting. The examination need not address all aspects of the product."*

Two phrases from there govern the design of this skill:

| Phrase | What authorizes |
|---|---|
| *"may also provide the **recommendation and examination of various alternatives**"* | **Act II**: presenting alternatives with recommendation is not an interface decoration, it is a function of the technical review |
| *"The examination **need not address all aspects** of the product"* | **Declare layers not executed** without invalidating the revision |
| *"which may require **more than one meeting**"* | **Split the package** into several sessions when the budget does not work |

**Difference from the PDR.** `mkl-pdr-review` was built on **clause 6 (inspection)**. It is consistent for what it does: verify that the use cases reflect what the customer wants, with the customer present. The CDR is the opposite — technical, without a client. That is why **the CDR minutes are governed by §5.7, not §6.7**. If you compare both skills and see different clauses, it is deliberate.

---

## What is borrowed from the inspection — and declared

Clause 5 does not include a review-rate table, a taxonomy of anomalies, or a scale of disposition. Clause 6 does. **Five pieces** are taken, and here it is said that they are loans:

| Piece | Clause | Why is it taken |
|---|---|---|
| Review Pacing Chart | §6.5.2 | It is the only normative data of how much material fits in a session |
| The nine categories of anomaly | §6.8.2 | Classify findings with normative rather than invented vocabulary |
| The ranking of anomalies in four levels | §6.8.3 | Severity Scale with Citable Definitions |
| The disposition scale in three states | §6.5.6.5 | Maintains symmetry with the PDR minutes |
| The “reviewed material size” field | §6.7 | Supports budget calculation |

None of these make the CDR an inspection. They supply vocabulary and scales; the procedure remains that of clause 5.

---

## Roles — §5.2, verbatim

> *"The following roles **shall** be established for the technical review: Decision maker · Review leader · Recorder · Technical reviewer. The following roles **may** also be established: Management staff · Other team members · Other stakeholders such as managers, technical staff, customers, and users. Individual participants may act in more than one role, but **no individual should act in all roles**."*

| Role | verbatim definition | Who occupies it here |
|---|---|---|
| **Decision maker** | *"the person for whom the technical review is conducted. The decision maker **shall determine if the review objectives have been met**."* | Formal organizational acceptance belongs to the authorized decision maker; the skill reports its technical assessment and carries out already authorized corrections |
| **Review leader** | *"shall be responsible for the review… ensuring that the review is conducted in an orderly manner, and ensuring that the review meets its objectives. The review leader shall issue the review outputs as described in 5.7."* | **The skill.** Conduct, prepare and write the minutes |
| **Recorder** | *"shall document anomalies, action items, decisions, and recommendations made by the review team."* | **The skill**, on the findings board |
| **Technical reviewer** | *"Staff in a technical role shall actively participate in the review and evaluation of the software product."* | The user and their team |

**The phrase that matters most for this skill is the last one in the general quote:** *"no individual should act in all roles"*. The skill conducts the review, records findings, and recommends action; **does not decide**. If the skill also decided, it would occupy all roles and compromise the review.

**About the client**, §5.2.6 leaves it as optional and at the discretion of the leader: *"The review leader should determine the need for a customer or user representative."* For the CDR, Rosenberg already answered no. It is declared and followed.

---

## Inputs — §5.3

> *"Input to the technical review **shall** include the following: a) A statement of objectives for the technical review; b) The software product being examined; c) Current anomalies or issues list for the software product; d) Documented review procedures."*

It is translated like this in this skill: **(a)** the ten rules of the CDR are the statement of objectives · **(b)** the `MC-XX` and the `DS-XX` · **(c)** the verdict of the PDR and any open findings · **(d)** this reference.

---

## Preconditions — §5.4.2, permission to stop

> *"A technical review **shall be conducted only when** the required review inputs are available and the people assigned to roles have been adequately **trained**."*

*(Accuracy note: an earlier version of this reference cited “adequately **prepared**”. This is incorrect — the standard says “trained”, and “adequately prepared” appears elsewhere in the document. It was corrected when checking against the primary text. It is recorded because a quote marked as literal that it is not taints confidence in all others.)*

This turns into a normative obligation what Rosenberg asks for practicality (line 4556):

> *"You need to have completed all of the sequence diagrams for the use cases that you're planning to implement in the current release. You should also have updated the class diagrams so that all of the operations that you assigned during sequence diagramming are reflected in the static model. **Having to update the diagrams during the review would be too much of a distraction**, so it's important to make sure all of that work is finished before the review begins."*

**Operational consequence:** If scope sequence diagrams are missing, or if the class model does not reflect the assigned operations, **the skill does not conduct the review**. It states the missing inputs and stops. Reviewing half-finished material produces a review that looks done and isn't — which is worse than not doing it at all.

---

## The seven determinations — §5.5.6, the agenda

This is what a technical review **should determine**. It is the agenda of Act I, and we do not have to invent it:

> *"The meetings shall accomplish the following goals: Decide on the agenda for evaluating the software product and anomalies. **Determine if**: The software product is complete · The software product conforms to the regulations, standards, guidelines, plans, specifications, and procedures applicable to the project · If applicable, changes to the software product are properly implemented and affect only the specified areas · The software product is suitable for its intended use · **The software product is ready for the next activity** · The findings of the inspection necessitates a change in the software project schedule · Anomalies exist in other system elements such as hardware or external/complementary software. **Identify anomalies and decide their criticality.** NOTE—Assignment of action items is left to management follow-up. **Generate a list of action items, emphasizing risks.** Document the meeting."*

| Determination | How the CDR responds |
|---|---|
| Is it **complete**? | Entry criteria + coverage of the ten rules |
| Does it **conform** to standards and plans? | Rules #3 and #6, and pipeline notation conventions |
| Are the **changes** well implemented and do they only affect what was intended? | Sewing with the PDR verdict: what has changed since then |
| Is it **suitable for its intended use**? | Rule #4 — human judgment, not automatable |
| Are you **ready for the next activity**? | **This is the CDR question.** The next activity is to code |
| Do the findings force us to move the calendar? | It is proposed in Act II as one of the alternatives |
| Are there **anomalies in other elements**? | Whatever appears out of reach is reported, without judging it |

**Two phrases in this clause govern what the skill DOES NOT do:**

- *"**Assignment of action items is left to management follow-up**"* — the skill generates the list; assign and execute is up to the user. That's why this skill **never edits artifacts**.
- *"Generate a list of action items, **emphasizing risks**"* — the list is sorted by risk, not by order of appearance.

---

## Exit criteria — §5.6

> *"A technical review shall be considered complete when the activities listed in 5.5.6 have been accomplished and the output described in 5.7 exists."*

That is to say: **the review is not complete until the record exists**. A commented word finding does not count.

---

## The minutes — §5.7, mandatory content

This is the structure of the `CDR-XX`. Verbatim:

> *"The output from the technical review **shall** consist of documented evidence that identifies the following: The project being reviewed · The review team members · The software product reviewed · Specific inputs to the review · Review objectives and whether they were met · A list of software product anomalies · A list of unresolved system or hardware anomalies or specification action items · A list of management issues · Action item status (open, closed), ownership and target date (if open), or completion date (if closed) · **Any recommendations made by the review team on how to dispose of unresolved issues and anomalies** · Whether the software product meets the applicable regulations, standards, guidelines, plans, specifications, and procedures without deviations. Although this standard sets minimum requirements for the content of the documented evidence, it is left to local procedures to prescribe additional content, format requirements, and media."*

**Three fields that inspection §6.7 does not ask for and that this skill needs:**

1. **«a list of management issues»** — what the CDR encounters and cannot technically resolve (scope, schedule, resources).
2. **«action item status, ownership and target date»** — each finding with owner and date, not a loose list.
3. **«any recommendations… on how to dispose of unresolved issues and anomalies»** — **Act II is mandatory content of the minutes**, not a courtesy of the skill.

From §6.7 a single field is taken, because §5.7 does not require it and the budget needs it: *"The size of the materials inspected (for example, the number of text pages)"*.

The last sentence permits local additions: *"it is left to local procedures to prescribe additional content"*. The optional formal minutes may therefore include the ten rules and an audit record. This permission does not mandate a certificate or repeated self-audits in ordinary scoped work.

---

## Classification of anomalies — §6.8.2, the nine categories

Inspection clause declared loan. Verbatim:

> *"⎯ Missing ⎯ Extra (superfluous) ⎯ Ambiguous ⎯ Inconsistent ⎯ Not conforming to standards ⎯ **Risk-prone**, i.e., the review finds that, although an item was not shown to be "wrong," the approach taken involves risks (and there are known safer alternative methods) ⎯ Incorrect ⎯ Unachievable (e.g., because of system, time, or technical constraints) ⎯ Editorial"*

There are **nine**, not eight: *Editorial* closes the list and is easy to overlook.

How typical CDR defects fall into these categories:

| Category | Typical CDR defect |
|---|---|
| **Missing** | Operation without declaring that the sequence requires · attribute without type · alternate course without fragment · lifeline without messages |
| **Extra (superfluous)** | Operation without origin · wrapper class · pattern that no message required |
| **Ambiguous** | `Object process(Object data)` · names like `doStuff()` · label that is unknown if it is an operation |
| **Inconsistent** | **The central flaw of the CDR**: the class model and the sequence do not say the same thing · operation in the wrong class |
| **Not conforming to standards** | Pipeline Notation Contract Violations |
| **Risk-prone** | God class · anemic model · deep hierarchy. **Be careful with this one**: the standard defines it as *"not shown to be wrong"* but risky — it is exactly the status of anti-patterns, which are not proven errors |
| **Incorrect** | Multiplicity that contradicts the business rule · upside down arrow |
| **Unachievable** | What rule #4 uncovers: programmers say you can't build it like that |
| **Editorial** | Names, spelling, diagram readability |

**The category `Risk-prone` deserves attention.** It is what saves this skill from a frequent excess: reporting an anti-pattern as if it were an error. The standard gives the exact status — it is not proven wrong, but there are known safer alternatives. That's the honest record for a God class or an anemic model.

---

## Severity — §6.8.3, verbatim

> *"Anomalies **shall** be ranked by potential impact on the software product, for example, as follows: a) **Catastrophic.** Anomalies that would result in software failure with grave consequences, such as loss of life, failure of mission, or very large economic or social loss; mitigation is not possible. b) **Critical.** Anomalies that would result in software failure with major consequences, such as injury, major system degradation, partial failure of mission, or major economic or social loss; partial to complete mitigation is possible. c) **Marginal.** Anomalies that would result in software failure with minor consequences; complete mitigation is possible. d) **Negligible.** Anomalies that would not result in software failure; mitigation is not necessary."*

**Calibration notice, and it's important.** This scale is defined by **impact on product in operation** — talking about loss of life and mission failure. A defect in a diagram doesn't kill anyone by itself. The skill uses the package's scale—**Critical · Major · Moderate · Minor**—which measures *impact on the design's ability to be passed to code*, and declares the mapping:

| Package Severity | CDR criteria | §6.8.3 Level |
|---|---|---|
| **Critical** | Invalidates the package to proceed to coding: the input criterion is not met, or the model and sequence contradict each other in the main flow | Catastrophic |
| **Major** | Break correspondence between artifacts or leave behavior unassigned | Critical |
| **Moderate** | Anti-pattern or `Risk-prone`: not proven to be a bug, but there are better alternatives | Marginal |
| **Minor** | Names, imprecise types, readability | Negligible |

The mapping is stated because **the two scales do not measure the same thing**, and using the standard names without saying so would suggest that a poorly drawn diagram can cost lives.

---

## Provision — §6.5.6.5, the three states

Declared loan. Verbatim:

> *"The purpose of the exit decision is to bring an unambiguous closure to the inspection meeting. The exit decision shall determine if the software product meets the inspection exit and quality criteria. As part of this decision, any appropriate rework and verification shall be prescribed. Specifically, the inspection team shall identify the software product disposition as one of the following:*
> *— **Accept with no verification or with rework verification.** The software product is accepted as is or with only minor rework (for example, that would require no further verification).*
> *— **Accept with rework verification.** The software product is to be accepted after the inspection leader or a designated member of the inspection team (other than the author) verifies rework.*
> *— **Reinspect.** The software product cannot be accepted. Once anomalies have been resolved a reinspection should be scheduled to verify rework."*

**Who issues it.** The skill reports the technical assessment with its evidence, selected scope, and limits. For an explicitly formal acceptance review, distinguish that recommendation from organizational sign-off by the designated decision maker. Act II is needed only when a real unresolved decision remains; existing user authorization is sufficient for supported corrections and requested headers.

| Proposed status | Condition |
|---|---|
| **Accepted** | Entry criterion met · zero critical and zero major findings · all layers executed or their absence justified |
| **Accepted with rework verification** | Only moderate or minor findings, **all** with agreed correction, responsible party and date |
| **Reinspection required** | Any open critical or major, or entry criteria not met |

**A phrase from the standard that should not be missed:** *"other than the author"*. The person who verifies the rework cannot be the one who did it. Applied here: if the user applies the corrections with the sister skills, the verification returns to the CDR — it is not considered good by the skill that corrected it.

---

## Improvement of the process itself — §6.9

The standard requires analyzing the review, not just the product:

> *"Frequently occurring anomalies **shall** be included in the inspection checklists or role assignments. The checklists themselves **shall** also be inspected regularly for superfluous or misleading questions… **The preparation times, meeting times, and number of participants shall be analyzed to determine connections between preparation (checking) rate, meeting rate, and number and severity of anomalies found.**"*

It is the normative foundation of two things about this skill: the **self-check of the review** against the empirical base rate (see `session-budget.md`), and the fact that the catalog of anti-patterns is **cumulative** — what appears repeatedly is added.

---

## Wiegers' five stages

Wiegers describes **five** stages, not six; what other methods call *overview* goes into the preparation.

| Stage | What happens | Quote |
|---|---|---|
| **Planning** | Author and moderator decide participants, material and pace | *"Two to four pages per hour is a practical guideline, although the optimum rate for maximum defect-detection effectiveness is about half that rate (Gilb and Graham 1993)."* |
| **Preparation** | Individual examination, before the meeting | *"**Up to 75 percent of the defects found by an inspection are discovered during preparation**, so don't omit this step (Humphrey 1989)… Plan on spending **at least half as much time on individual preparation** as is scheduled for the team inspection meetings."* |
| **Inspection meeting** | Consolidation and disposition | *"shouldn't last more than about **two hours**; tired people aren't effective inspectors."* |
| **Rework** | Correction by the author | — |
| **Follow-up** | Rework verification and closure | — |

**Wiegers' literal trap:** *"Don't proceed with an inspection meeting if the participants haven't already examined the work product on their own. Ineffective meetings can lead to the erroneous conclusion that inspections are a waste of time."*

**Why this matters here.** 75% of the defects are found in individual preparation — which is exactly the phase this skill automates. It is not a substitute for meeting or human judgment: it does well the part where the evidence says performance is there.

**And a brake that should be respected:** *"Don't ask anyone to review the same material more than three times… he won't spot major issues after a third cycle because of 'reviewer fatigue.'"* If on the third round the package still doesn't pass, the problem is not the review: it is the device or its scope.

---

## Who participates

From the course material, and it agrees with Rosenberg:

> *"The CDR is a technical review. Therefore, the following typically participate: Architects · Designers · Technical analysts · Developers · Design reviewers."*

About customer:

> *"Should the Client Participate? Generally not... The CDR analyzes technical implementation details that are not normally part of the client's knowledge or responsibilities. The client provides a lot of value in: Requirements · Use cases · Functional validation. But the review of patterns, classes, interfaces and responsibilities is usually the job of the technical team."*

**Rule #4 requires that programmers be there.** Rosenberg is blunt (4618): *"Programmers need to be involved in detailed design."* If the package is reviewed without anyone going to build it, rule #4 is **not executed** and is declared as such in the minutes — no pretense of coverage.

---

## Origin of quotes

| Source | Locator |
|---|---|
| IEEE Std 1028-2008 — §5.1, §5.2, §5.3, §5.4.2, §5.5.6, §5.6, §5.7, §6.5.2, §6.5.6.5, §6.7, §6.8.2, §6.8.3, §6.9 | Primary text read in full |
| Rosenberg & Stephens, *Use Case Driven Object Modeling with UML* | Lines 4545, 4556-4557, 4618 |
| Wiegers & Beatty, *Software Requirements 3rd ed.*, chap. 17 | Lines 6297, 6306-6308, 6314, 6316, 6356 |
| Course material, *Session 09 — Critical Design Review* | Sections “Who Should Participate?” and "Should the Client Participate?" |

Where each source lives is in `sources-and-methods.md`. **The skill does not need them to work**: everything that can be cited is transcribed above.
