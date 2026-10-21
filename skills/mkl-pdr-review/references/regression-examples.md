<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Regression expectations by domain

To verify that the skill **generalizes** and does not overfit to a domain. They are not templates: they are expectations about what a PDR should find in each context. **Never move objects, actors, or findings from one domain to another** — if they appear in your review, it is because the user's material supports them, not because they are here.

Unlike sisters, here the test unit is a **set of artifacts**, not a file. A set can be coherent or incoherent on purpose, and what is tested is the **verdict** in addition to the findings.

---

## Veterinary clinic — "Register vaccination"

Mastery of fixtures. Deliberately chosen outside of the skill material.

- **Entities expected in robustness:** Pet, Vaccine, Vaccination Registry. They must all exist in the domain.
- **Unused domain class:** Owner. It is **information**, not a defect: it belongs to other use cases.
- **Expected alternatives:** the vaccine does not correspond to the scheme; the pet is not registered.
- **Domain trap:** the Veterinarian is an actor, not an entity. If it appears as `entity`, it is a stereotype defect, not a missing entity.
- **Expected verdict of the coherent set:** Accepted.

## Academic enrollment — "Subject enrollment"

- **Entities:** Student, Subject, Group, Enrollment, Period.
- **Alternates that are almost always missing:** no quota, prerequisite not met, credit limit exceeded. All three are the typical case of "enumeration without behavior": it is said that an error is shown and not what happens to the current enrollment.
- **Data flow to verify:** the credits and quota appear on the screen; Check that they have an attribute where to land.
- **Derived from frequent vocabulary:** `Subject` versus `Course`. **Warning: it is synonymous drift and the validator does not detect it** — you must read it.

## Banking — "Transfer funds"

- **Entities:** Account, Transaction, Beneficiary, Movement.
- **Mandatory alternatives:** insufficient balance, invalid recipient, failed authorization, daily limit exceeded. A PDR that approves a transfer with less than these four is missing half the complexity.
- **High risk of design-pattern-itis:** it is the domain where `TransactionDAO`, `PaymentStrategy`, `AccountRepository` appear most easily.
- **High robustness-as-sequence risk:** the interaction with the payment network invites the exchange of messages with signatures and `alt` blocks.

## Medical history — "Schedule appointment"

- **Entities:** Patient, Professional, Schedule, Appointment.
- **Domain sensitivity:** if the text mentions clinical data, **do not invent clinical entities** that the domain model does not have; They go to the delta as candidates, with the phrase that justifies them.
- **Alternate:** no availability, cancellation, ineligible patient.
- **Guideline Note #4:** In regulated domains, the non-technical participant may be a healthcare professional. The criteria does not change: if you do not understand the use case, the contract does not exist.

## Logistics — "Dispatch shipment"

- **Entities:** Shipping, Vehicle, Carrier, Guide, Route.
- **Alternatives:** no vehicle available, invalid address, shipment already dispatched.
- **Domain trap:** the external tracking service is a secondary actor **only if the text describes an interaction with it**. If you only consult internally, you are not an actor.

## Industrial monitoring — "Check device alerts"

- **Entities:** Device, Reading, Threshold, Alert.
- **Alternate:** device offline, reading out of range, alert already attended.
- **Should not appear:** "parse frame", "refresh buffer", "persist read" as Controllers — they are implementation, and in this domain they sneak in especially easily.
- **Session Budget:** Packages from this domain tend to be large; This is where the message about leaving the package is most often correct.

---

## What to check on any domain

Regardless of the context, a well-done PDR answers these twelve questions, and the minutes should allow each answer to be verified:

1. Does every entity in every diagram exist in the domain model? *(meta: yes, no exceptions)*
2. Were unused domain classes reported as information and not as a defect?
3. Does each `FA`/`FE` in the specification have a branch in the diagram?
4. Does each alternate specify **behavior**, not just the condition that triggers it?
5. Does the basic flow alternate between actor and system?
6. Zero prohibited links between stereotypes?
7. Is no diagram actually a sequence diagram?
8. Are no Controllers named after a design pattern?
9. Does every screen have its own name and does every actor come from the use case diagram?
10. Does the data on the screens have attributes to land on?
11. Does each finding have severity, recipient, owner and date?
12. Is each layer declared as executed or **not executed**, without gaps?

And two that are not about the artifacts but about the review itself:

13. Was there a non-technical person who validated the language? If not, guideline #4 goes as **not executed**.
14. Did the volume of the package fit into the session time at a sustainable pace?

## Signs that the skill is overfitting

Watch for these symptoms when checking out a new domain. Any of them means that you are reproducing an example instead of analyzing the material:

- Entities, screens or actors appear that are **not** in the user's artifacts.
- The proposed alternates coincide with those of a domain on this list without the text mentioning them.
- The delta to the domain model proposes classes that the text does not justify with a specific phrase.
- The verdict is issued without the validator output supporting it.
- A finding cites a line or step that does not exist in the file.

The last one is the most serious and the easiest to verify: **each finding must point to a verifiable location**. It is a condition of the internal audit cycle precisely for this reason.
