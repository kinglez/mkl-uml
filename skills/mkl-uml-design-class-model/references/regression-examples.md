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
- **Domain trap:** an external `Librarian` role does not automatically imply a design class. A separately evidenced staff/account concept may be modeled; distinguish its identity and responsibilities from the actor role.
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
- **Trap:** choose the medical-record/consultation relationship from evidenced ownership and lifecycle constraints. A whole/part phrase or existential dependency alone does not establish UML composition.

## Logistics — “Dispatch shipment”

- **Classes:** `Shipment`, `Vehicle`, `Carrier`, `Waybill`, `Route`.
- **Composition candidate:** `Route` and its legs when the supplied constraints establish exclusive composite ownership and deletion of still-owned parts with the whole. State whether detachment is allowed; otherwise retain an association until ownership is resolved.
- **Expected solution classes:** tracking-service integration. Mark them explicitly.

## Industrial monitoring — “View alerts”

- **Classes:** `Device`, `Reading`, `Threshold`, `Alert`.
- **Must not appear:** `Buffer`, `Parser`, `MessageQueue` without `<<solution>>` **and** a requiring message. This domain has a high risk of infrastructure disguised as domain structure.
- **Class-swarm risk:** `Reading`, `RawReading`, `NormalizedReading`, and `AggregatedReading` often indicate overnormalization.

---

## Checks for every domain

**Provenance**, the skill's central concern:

1. Does every significant operation have a classified call, interface/framework contract, architecture constraint or justified design-decision origin within the selected scope?
2. Does every problem class exist in the domain under the same name or with declared drift?
3. For a class absent from the domain, is it a justified `<<solution>>` class or a documented late domain discovery awaiting reconciliation?
4. Does every attribute trace to domain/scenario/interface evidence or a documented architecture, configuration, framework contract or design decision? Technical/internal state need not be named in business use cases.
5. Does every relationship have domain, collaboration, navigation, ownership, interface or architecture/design-decision evidence?

**Method:**

6. Are trivial accessors omitted where they add no useful contract detail, with any necessary accessor behavior justified?
7. Complete operation signatures: typed parameters and return values?
8. Is modeled state appropriate to the class's role, with absent state investigated rather than invented?
9. No class left without operations without justification?
10. Multiplicities supported rather than assumed?
11. Does composition follow evidenced exclusive ownership and deletion semantics, including any permitted detachment, rather than assumed permanent lifetime dependency?

**Pipeline consistency:**

12. Are all sequence-delta operations present? *(CDR entry criterion)*
13. Did any domain class disappear without justification?
14. Are unexecuted layers declared, with degradation reflected in the verdict?

---

## Overfitting signals

Any signal indicates fixture reproduction instead of assembly from inputs:

- Classes, attributes or operations have no supported scenario, domain, interface, architecture, configuration or design-decision origin after checking the selected scope.
- Structure matches a listed domain without support: same class count or hierarchy shape.
- Refactoring delta proposes classes unsupported by text.
- A finding cites a nonexistent line or element. **Most serious and easiest to check:** every finding must identify a verifiable location.
- Incomplete inputs produce an unqualified completeness claim. A scoped model may have no located defects while dependent checks remain partial; report actual evidence gaps without inventing findings.
