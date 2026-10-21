<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Act II: deliberate before deciding

Use this optional formal decision-management recipe when findings require a real scope, business, or risk-acceptance decision. Ordinary scoped checks report their evidence-based result immediately. Existing user authorization covers supported corrections and requested headers; do not withhold a result or require a new approval ceremony.

---

## Why does this act exist?

It might seem like a courtesy—“show your findings before acting”—and it is not. There are three sources coinciding:

**IEEE 1028 §5.1** attributes exactly this function to the technical review:

> *"Technical reviews may also provide the **recommendation and examination of various alternatives**, which may require more than one meeting."*

**IEEE 1028 §5.7** makes the recommendation **mandatory content of the record**:

> *"…**any recommendations made by the review team on how to dispose of unresolved issues and anomalies**"*

**IEEE 1028 §5.2.1** says who decides, and is not the one who reviews:

> *"The decision maker is the person for whom the technical review is conducted. **The decision maker shall determine if the review objectives have been met.**"*

For a formal technical review these quotations distinguish reviewer recommendations from organizational acceptance decisions. They do not require a conversational pause for every finding or revoke the user's existing instruction to make corrections. The skill may report an evidence-based technical assessment and execute authorized work; it records unresolved organizational decisions separately. Preserve the formal role distinction when organizational sign-off is actually requested.

**And the structure of the deliberation** is given by ISO/IEC/IEEE 12207:2017 §6.3.3, *Decision Management process*, in its four outputs:

> *"a) Decisions requiring alternative analysis are identified. b) Alternative courses of action are identified and evaluated. c) A preferred course of action is selected. d) **The resolution, decision rationale and assumptions are identified.**"*

(d) is the one that is usually lost: it is not enough to decide, you have to write down **why** and **under what assumptions**. Without that, three months from now no one will know whether a decision was deliberate or careless.

---

## How the findings are presented

**Grouped, not in a flat list.** A list of thirty findings without structure is impossible to decide. They are grouped by **recipient**—the sister skill that owns the artifact—because this way each group becomes a coherent task.

Within each group, ordered by **risk**, not by order of appearance. Required by §5.5.6: *"Generate a list of action items, **emphasizing risks**."*

**Each finding comes with the minimum to be able to decide on it:**

| Field | Why is it necessary |
|---|---|
| What was observed | Without the symptom there is nothing to judge |
| **Where**, verifiable | File and line or element. A finding that cannot be located cannot be verified — and it is the most serious mistake this skill can make |
| Supporting rule | A finding without a rule is an opinion |
| Anomaly category | §6.8.2 Vocabulary: Distinguish a demonstrated error from a `Risk-prone` |
| Severity | Critical · Major · Moderate · Minor |
| What happens if it is not corrected | The concrete consequence, not the abstract one |

**About `Risk-prone` in particular:** when a finding is an anti-pattern and not a demonstrated error, it must be said in the words of the standard — *"although an item was not shown to be 'wrong,' the approach taken involves risks"*. Presenting a God class as if it were a proven bug erodes the credibility of findings that are.

---

## Possible dispositions

The four examples below are MKL decision aids, not a fixed menu mandated by IEEE or ISO. IEEE §5.1 says alternatives **may** be examined. Present only genuinely relevant choices with a recommendation when a user decision is needed. If the correction is supported and already authorized, apply it and report the evidence without asking again.

### 1. Fix now
It is routed to the owning skill and corrected before coding.
**When recommended:** critical or major findings; anything that breaks the correspondence between artifacts. The argument is the same as always and is measured — correcting in the design costs much less than correcting in the code (Wiegers: *"an average of 30 minutes to fix a defect discovered during the requirements phase… 5 to 17 hours during system testing"*).

### 2. Defer with accepted risk
It is recorded, it is implemented as designed, and the risk is registered with an owner.
**When it is recommended:** moderate or minor findings whose correction costs more than the risk it avoids. **Never** for critical or major findings.
**Condition that ISO 90003 §8.3.4.1 sets, and must be respected:** *"further design and development activities should proceed only when **the consequences of all known deficiencies are understood**, or **the risk of proceeding otherwise is known and agreed**"*. Deferral is legitimate only when its consequences are understood.

### 3. Reopen the previous artifact
The finding is not fixed here: it reveals that something upstream was wrong.
**When is it recommended:** when the defect **does not have a local fix**. The case of `Queue` is the example — the asymmetric class is not fixed by adding a method, it is fixed by correcting the arrow in the sequence. Patching the class model would leave the two artifacts at odds.

### 4. Declare false positive
The finding is not such, and the reason is recorded.
**When is recommended:** when the user provides context that the skill did not have. **It is recorded the same**, with the reason: a documented false positive improves the catalog; a muted one will repeat each time.

**A fifth solution that is not an alternative but a consequence:** if the findings force the calendar to be moved, it is said. §5.5.6 includes it among the determinations of every technical review and it is a *management issue* that §5.7 requires to be listed separately.

---

## The question about code headers

Rule #2 proposes generating headers and inspecting them. Generate them when requested or already included in the user-authorized work. Ask only when a real unresolved scope decision affects whether headers belong in the deliverable; do not ask again for already authorized generation.

When asking, it is advisable to say what is gained and what it costs, so that the decision is informed:

- **Benefits:** is the highest performing CDR check, because an inconsistent model becomes evident when viewed as code — missing attributes, mismatched parameters, duplicate operations appear.
- **Cost:** inspection adds time based on actual header volume. The upstream source-code rate has inconsistent units; use a declared project estimate until verified (see `session-budget.md`).
- **And it must be said that they are NOT:** review instrument, not production code. It is explained in `traceability-and-headers.md`.

---

## What is recorded at the close of deliberation

The **decision report**, which is output (d) of §6.3.3. For each group:

- The alternatives that were presented
- Which one was recommended and why
- The existing authorization or actual decision taken; request a new user choice only for an unresolved decision beyond that authorization
- **The reasoning and assumptions**, which is what §6.3.3 (d) requires and what makes the decision auditable months later
- For the deferred: the accepted risk, with owner and review date

---

## Errors that this act should avoid

**Conflate a technical assessment with organizational approval.** Report the technical result and coverage when known. If a genuinely unresolved decision prevents a formal acceptance disposition, identify that decision precisely and keep that formal acceptance pending; do not withhold the completed review or its findings.

**Present alternatives without a recommendation.** Offloads onto the user a task that the skill has just done. If the package was reviewed, you have an opinion: it is given, with its reason, and it is accepted that the user decides otherwise.

**Negotiate the verdict due to fatigue.** If the package does not pass, the result is *Reinspection required* — not a downgraded *Accept* because the turns are exhausted. Wiegers puts the complementary brake: *"Don't ask anyone to review the same material more than three times."* If the third time it still doesn't pass, the problem is not the review: it is the artifact or its scope, and that is also a finding.

**Silently exceed the authorized correction scope.** In a review-only request, report corrections rather than applying them. In an authorized review-and-fix task, apply supported changes and recheck affected evidence; the quotation *"assignment of action items is left to management follow-up"* describes formal organizational follow-up, not a ban on executing the user's existing instruction.

---

## Origin

| Source | What it contributes |
|---|---|
| IEEE Std 1028-2008 §5.1, §5.2, §5.2.1, §5.5.6, §5.7 | The function of recommending alternatives, the role of the decision-maker, the distribution of roles, the content of the minutes |
| ISO/IEC/IEEE 12207:2017 §6.3.3 | The four outputs of the decision management process |
| ISO/IEC/IEEE 90003:2018 §8.3.4.1 | The condition to proceed with known deficiencies |
| Wiegers & Beatty, *Software Requirements 3rd ed.*, chap. 17 | The comparative cost of correcting late (line 6189) and the limit of three revisions (6356) |
