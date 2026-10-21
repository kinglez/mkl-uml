<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Domain-specific regression expectations

Check that the skill **generalizes** rather than reproduces its fixture. These are not templates: they describe expected elements, exclusions, and domain-specific traps. **Never transfer classes, attributes, or operations between domains**; their presence must be supported by the user's material.

**A costly methodological lesson.** An earlier audit found that two sibling skills' “good” sets used the **same skeleton with different vocabulary**: identical participants, topology, and branch count. A validator whose happy path is fixed to a fixture **approves anything with that shape**. This skill's good set deliberately differs: nested branching, real inheritance in the output, and a legitimate solution class. Expectations therefore emphasize **structure**, not only names.

**The good set alone is insufficient.** A clean happy path cannot distinguish a working tool from a disabled one: both pass. The signal comes from sets that **must** trigger a specific finding and only that finding. Audit-discovered defects—the self-certifying empty model, operation on the wrong class, directional inheritance arrows, and silently lost members with defaults—now have dedicated `tests/examples/` sets. A fix without a persistent regression set can break unnoticed.

---

## University library — “Manage loan” *(fixture domain)*

Chosen because it requires structures absent from flat domains: **real inheritance in the output** (book and audiovisual loans share behavior but issue different receipts), **two branches with nesting** in the sequence, and a **legitimate solution class** (loan policy is a design strategy, not a domain concept).

**Post-audit correction:** an earlier version said “two actors.” **That was inaccurate**: `Member` appears in the specification, but is an entity lifeline in the sequence, not an actor. The input **domain** model has no inheritance; the hierarchy arises during design, exactly where the method locates it. The real structural differences are nested branching and output inheritance, not actor count.

- **Problem classes:** `Member`, `Copy`, `Work`, `Loan`, `Penalty`.
- **Expected inheritance:** material-specific `Loan` subtypes **if and only if** sequences show varying behavior; otherwise the hierarchy is invented.
- **Expected solution class:** a policy or due-date calculator, marked `<<solution>>` and justified; without that stereotype it is anti-pattern #2.
- **Typical operations:** `Copy.checkAvailability()`, `Member.checkActivePenalty()`, `Loan.register(...)`. Each must originate in a message **addressed to that class**. Due-date calculation belongs to the loan policy, not `Loan` or `Member`. Misplacing it is anti-pattern #15, covered by `operacion_clase_equivocada`.
- **Domain trap:** `Librarian` is an actor, **not a class**. A design class with that name confuses an actor with an object.
- **Second trap:** `Penalty` tempts a boolean attribute on `Member`. Dates, amounts, or history in the text imply a class; “penalized member” alone may imply an attribute. Decide from the specification.
- **Anemia risk:** all calculation in `LoanManager` while `Loan` has only attributes: #4.

## Academic enrollment — “Enroll in course”

- **Classes:** `Student`, `Course`, `Group`, `Enrollment`, `Term`.
- **Trap:** prerequisites suggest an often unjustified hierarchy. A prerequisite is a **reflexive relationship** among courses, not a subclass.
- **Useful multiplicity:** the credit limit is a validation rule, precisely where the source considers multiplicity useful.
- **Likely solution class:** an enrollment-rule validator.

## Banking — “Transfer funds”

- **Classes:** `Account`, `Transaction`, `Beneficiary`, `LedgerEntry`.
- **Frequent real inheritance:** account types with different balance rules; a domain where inheritance is often justified.
- **High anemia risk:** putting all logic in `TransferService` and reducing `Account` to a balance container. If `Account` cannot decide whether it can be debited, behavior was misallocated.
- **High premature-pattern risk:** `TransactionFactory`, `FeeStrategy`. Apply provenance: did a message require it?

## Medical record — “Record consultation”

- **Classes:** `Patient`, `Practitioner`, `Consultation`, `Diagnosis`.
- **Domain sensitivity:** do not invent clinical entities missing from the domain model. Put candidates in the delta with supporting text.
- **Trap:** the full medical record may look like a class but often **aggregates** consultations. Use existential dependency to decide.

## Logistics — “Dispatch shipment”

- **Classes:** `Shipment`, `Vehicle`, `Carrier`, `Waybill`, `Route`.
- **Clear composition:** `Route` and its legs; a leg cannot exist without a route. Good for distinguishing composition from aggregation.
- **Expected solution classes:** tracking-service integration. Mark them explicitly.

## Industrial monitoring — “View alerts”

- **Classes:** `Device`, `Reading`, `Threshold`, `Alert`.
- **Must not appear:** `Buffer`, `Parser`, `MessageQueue` without `<<solution>>` **and** a requiring message. This domain has a high risk of infrastructure disguised as domain structure.
- **Class-swarm risk:** `Reading`, `RawReading`, `NormalizedReading`, and `AggregatedReading` often indicate overnormalization.

---

## Checks for every domain

**Provenance**, the skill's central concern:

1. Does every operation originate in a sequence message?
2. Does every problem class exist in the domain under the same name or with declared drift?
3. Does every class **absent** from the domain carry `<<solution>>` and a rationale?
4. Does every attribute trace to specification, prototype, or domain?
5. Does every relationship come from the domain or an operation requirement?

**Method:**

6. No *getters* or *setters*?
7. Complete operation signatures: typed parameters and return values?
8. No entity left without attributes?
9. No class left without operations without justification?
10. Multiplicities supported rather than assumed?
11. Aggregation/composition decided using existential dependency?

**Pipeline consistency:**

12. Are all sequence-delta operations present? *(CDR entry criterion)*
13. Did any domain class disappear without justification?
14. Are unexecuted layers declared, with degradation reflected in the verdict?

---

## Overfitting signals

Any signal indicates fixture reproduction instead of assembly from inputs:

- Classes, attributes, or operations appear **in no input artifact**.
- Structure matches a listed domain without support: same class count or hierarchy shape.
- Refactoring delta proposes classes unsupported by text.
- A finding cites a nonexistent line or element. **Most serious and easiest to check:** every finding must identify a verifiable location.
- Incomplete inputs produce a clean model on the first pass. An honest assembler **finds** upstream gaps; none can be more suspicious than several.
