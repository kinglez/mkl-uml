<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Regression expectations by domain

To check that the skill **generalizes** instead of reproducing its test set. They are not templates: they are expectations about what should appear, what should not, and what trap each domain has.

**Never move classes, operations, or findings from one domain to another.** If they appear in your review, it is because the user's material supports them.

---

## Methodological warning that this package paid dearly

A previous audit found that the "good" set of two sister skills was the **same skeleton with different vocabulary**. A validator whose happy path is pinned by a set **approves anything with that form**.

**And there is something worse, which this skill does solve.** A good set that comes out clean **does not distinguish** a working tool from a disabled one: both produce the same output on correct material. What signals are the sets that **must** fire, each their own and theirs alone — and, in the case of the CDR, the **self-check of the review**, which is the only defense against a review that passes over without seeing anything.

---

## Technical Support — "Manage issue" *(test set domain)*

Chosen because a CDR needs things that flat domains do not have: **multiple use cases in the same release** (the CDR is limited to a release, not a case), **rich alternative flows**, **traceable requirements** including non-functional ones, and **robustness controllers** that serve as an index of the journey.

- **Problem classes:** `Incident`, `Requester`, `Technician`, `Category`, `ServiceAgreement`.
- **Release use cases:** register incident · escalate incident · close incident. **Three**, so that the coarse traversal has more than one element.
- **Expected alternative flows:** unauthorized applicant · non-existent category · expired service agreement · technician without availability. Each one must have fragment in the sequence (rule #9) and test case (rule #1).
- **Non-functional requirement to plot:** the response time required by the service agreement. It's the hard case of rule #5 — it doesn't fall into a class, it falls into a design decision.
- **Domain Trap:** `Technician` is both an actor and an entity. As an actor, the escalation begins; As an entity it has availability and load. Confusing them produces either an actor with attributes or an entity that triggers use cases.
- **Second trap:** `ServiceAgreement` invites to be an attribute of `Incident` (a deadline). If the text talks about levels, calculations or history, it is class; If it only says "due on...", it can be an attribute. It is decided by the specification.
- **Anemia to watch for:** If the entire expiration and priority calculation ended in a `IncidentManager` and `Incident` only has attributes, it is anti-pattern #6.
- **Package to watch:** a `IncidentCommand` that only carries a `Incident` is anti-pattern #10, with the exact shape of the book case.

---

## Academic enrollment — "Subject enrollment"

- **Trap:** prerequisites invite a hierarchy that does not exist. A prerequisite is a **reflective relationship** between subjects.
- **Easy to fail rule #5:** The credit cap is usually in the requirements and does not appear in any class — requirement without implementation.
- **Rule #9:** the alternatives are almost the entire case (space full, prerequisite not met, outstanding debt). A design that only models the happy path is the error that Rosenberg calls the YAGNI.

## Banking — "Transfer funds"

- **High risk of anemia:** This is where you most tend to leave `Account` as a balance container and put everything in a `TransferService`. If `Account` does not know if it can debit, something was assigned wrong.
- **Critical Rule #3:** Imprecise type amounts are a real defect, not a cosmetic one.
- **Rule #5:** non-functional requirements (audit, operation traceability) have to fall somewhere in the design. If they don't fall, it's a discovery.

## Medical history — "Register consultation"

- **Sensitivity:** do not invent clinical entities. What the design needs and is not specified goes to Act II as a decision, it is not added.
- **Especially important rule #4:** That a design is constructible in a regulated domain is not evident from the diagram.

## Industrial monitoring — "Check alerts"

- **High risk of anti-pattern #14:** `Buffer`, `Parser`, `MessageQueue` are unstable abstractions. Without `<<solucion>>` they are mixed with the domain.
- **Rule #6:** is the domain where most behavior tends to occur “magically” — data acquisition is rarely drawn.

---

## What to check on any domain

**Entry criteria, first of all:**

1. Is there one `DS-XX` for each `CU-XX` in the release scope?
2. Does `MC-XX` reflect the operations assigned in the sequences?
3. Were missing prerequisites for the selected checks disclosed, while available independent checks and authorized corrections continued?

**The ten rules:**

4. Does each behavior phrase in the text have messages? *(#10)*
5. Does each `FA-XX`/`FE-XX` have fragment? *(#9)*
6. Does each significant operation within scope trace to an Operation-call addressed to that class, or to a declared contract/design delta? *(#8)*
7. Are there classes without operations, entities without attributes, or multiple personalities? *(#7)*
8. Is the important behavior drawn, without magic? *(#6)*
9. Does each requirement arrive at a class, and each class is explained by a requirement — **in both directions**? *(#5)*
10. Did anyone who was going to build it participate, or was the rule declared not executed? *(#4)*
11. Complete and accurate types, returns and parameters? *(#3)*
12. Were requested/authorized headers generated and inspected, with a new question only for a genuine unresolved scope decision? *(#2)*
13. Does each robustness controller have a test case? *(#1)*

**Of the procedure:**

14. Was the session budget calculated at the correct row pace?
15. Are the layers declared not executed, and do they **degrade** the verdict?
16. Were relevant alternatives with a recommendation presented only for decisions that actually needed resolution, with the technical result still reported?
17. Does the record have the fields that §5.7 requires, including *management issues* and the status of each action item?
18. Did the skill respect review-only scope, or apply and verify supported edits when review-and-fix was authorized?

---

## Signs of overfitting

Any of these means that you are playing an example instead of reviewing:

- Findings appear about elements **that are not in the input artifacts**.
- A finding cites a line or an element that does not exist. **It is the most serious and the easiest to verify**: each finding must point to a verifiable location.
- The findings look suspiciously similar to those from the technical support domain in a banking package.
- **The check comes out clean on a large packet.** It contradicts the base rate of 0.4 failures/page, and the skill should say so itself — if it doesn't, the self-check is broken.
- The verdict comes out `Accepted` with layers declared as not executed. It is the exact failure that `mkl-pdr-review` had and is explicitly tested here.
- A cyclomatic complexity threshold is proposed. **Does not exist in the corpus**; To propose it is to invent.
