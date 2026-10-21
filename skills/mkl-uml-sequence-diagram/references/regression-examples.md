<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Domain-specific regression expectations

These examples assess **generalization**, rather than reproduction of a familiar design. They are expectations, not templates. Introduce participants, messages, and operations only when supported by the user's `DR-XX` and specification.

The test unit is an **artifact set**: sequence, robustness, specification, and domain model. Check consistency across all four, not merely one `.puml` file. Fixture identifiers may retain their original spellings for compatibility; the English names below describe their roles.

## Parking facility: Record Vehicle Entry

The fixture domain was selected because it did not appear in the skill's source examples or the five preceding skills' regressions.

- **Participants:** Operator (actor); Entry Console and Entry Receipt (boundaries); Vehicle, ParkingSpace, Ticket (entities).
- **Unused domain class:** Rate. Informational, not defective; it belongs to vehicle exit.
- **Appropriate allocation:** ParkingSpace marks itself occupied and issues the Ticket; the console does not do everything. Concentrating these responsibilities in the console is centralized control.
- **Alternative:** no available space.
- **Domain trap:** the barrier and license-plate reader are infrastructure, declared as `participant` rather than `entity`.

## Academic enrollment: Enroll in Subject

- **Entities:** Student, Subject, Section, Enrollment, Term.
- **Typical allocation:** prerequisite checking belongs to Student or Enrollment, not an EnrollmentController. Responsibility follows knowledge of the academic record.
- **Required alternatives:** no capacity, unmet prerequisite, credit limit exceeded. Derive a `CP-XX` for each.
- **Anemic-model risk:** an EnrollmentManager does everything while Student and Subject only return data.

## Banking: Transfer Funds

- **Entities:** Account, Transaction, Beneficiary, AccountMovement.
- **Typical allocation:** Account knows whether its balance is sufficient. Moving that check into a service separates behavior from the relevant knowledge.
- **Required alternatives:** insufficient funds, invalid recipient, failed authorization, daily limit exceeded.
- **Legitimate infrastructure:** a payment gateway or interbank network may participate in detailed design, declared as `participant` and recorded as solution-space classes in the delta.
- **Premature-detail risk:** transaction handling, sessions, and retries appear before domain responsibilities have been allocated.

## Clinical care: Schedule Appointment

- **Entities:** Patient, Professional, Schedule, Appointment.
- **Typical allocation:** Schedule determines time-slot availability. The screen should not own that decision.
- **Domain sensitivity:** report required new clinical classes in the delta **with justification**, rather than inserting unsupported participants absent from `DR-XX`.
- **Vocabulary caution:** Session may mean a therapy session and therefore be a domain concept. **The domain model decides**, rather than a technical-term blacklist.

## Logistics: Dispatch Shipment

- **Entities:** Shipment, Vehicle, Carrier, ShippingDocument, Route.
- **Typical allocation:** Route calculates its estimated duration; ShippingDocument assigns its number.
- **Alternatives:** no available vehicle, invalid address, already-dispatched shipment.
- **Trap:** include an external tracking service as infrastructure **only when the design interacts with it**. Merely retrieving an already-stored tracking value does not justify a new participant.

## Industrial monitoring: View Device Alerts

- **Entities:** Device, Reading, Threshold, Alert.
- **Typical allocation:** Threshold decides whether a Reading exceeds it—a clear information-expert example.
- **Exclude from domain messages:** frame parsing, buffer updates, and persistence mechanics. These implementation details are particularly easy to introduce prematurely here.
- **Size risk:** growing packages in this domain often call for splitting the use case.

## Checks for every domain

1. Every `DR-XX` control is covered by at least one message **or** explicitly represented as a participant.
2. Participant names remain consistent with `DR-XX`.
3. Every entity exists in the domain model.
4. New solution-space participants are **recorded and justified in the delta**.
5. Infrastructure uses `participant`/`database`, never `entity`.
6. Actors exchange messages **only with boundaries**.
7. Every specified `FA-XX`/`FE-XX` has a fragment labeled with its identifier.
8. No participant is orphaned.
9. Return messages convey useful information rather than being drawn mechanically for every call.
10. Activation bars appear only when requested under this skill's default convention.
11. Check whether one participant sends most messages.
12. Check whether any entity has no behavior beyond getters/setters.
13. Every delta operation identifies its receiving class **and the reason for that allocation**.
14. Every control yields at least one `CP-XX`, and every path is covered.

## Signs of overfitting

The following indicate example copying rather than actual design:

- Unsupported participants, messages, or operations appear.
- Message names match an example domain without support in the user's text.
- New delta classes have no design rationale.
- **Every control maps to exactly one identically named message**, suggesting copying rather than behavior allocation.
- A `CP-XX` cites a path absent from the diagram.
- A finding cites a nonexistent line or step.

The last issue is particularly serious and straightforward to check: **every finding must identify a verifiable location**.
