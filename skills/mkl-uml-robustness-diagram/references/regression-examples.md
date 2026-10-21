<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Domain-specific regression examples

These expectations assess whether the skill **generalizes** across domains. They specify what should and should not appear, rather than providing complete diagrams. Treat them as domain-specific regression data, not reusable templates: carry an object into another example only when that use case text supports it.

## Hotel reservation: Reserve Room

- **Actor:** Customer; payment gateway only if the text specifies external validation.
- **Boundaries:** actual search, selection, guest-details, and confirmation pages. Use distinct names when the text distinguishes screens.
- **Controls:** check availability; calculate amount; record reservation; confirm payment; send confirmation.
- **Entities:** Room, Reservation, Customer, Payment, Rate, as present in the domain model.
- **Alternatives:** unavailable room → alternative dates; rejected payment → no reservation created.
- **Typical discoveries:** a Customer Session or Reservation Status implied by the text.
- **Exclude:** button boundaries, “Save to database” controls, Reservation operations, and payment-type inheritance, which belongs in the domain model.

## Academic enrollment: Enroll in Subject

- **Actor:** Student; external academic system only if explicitly specified.
- **Boundaries:** course-offering page, selection page, enrollment receipt.
- **Controls:** retrieve offerings; check prerequisites; check capacity; record enrollment; issue receipt.
- **Entities:** Student, Subject, Section, Enrollment, Term.
- **Alternatives:** no capacity; prerequisite unmet; credit limit exceeded.
- **Exclude:** a bare “Validate” control without an object, or separate controls for each business rule when the text specifies one combined check.

## Medical appointment: Schedule Appointment

- **Actor:** Patient; healthcare professional or external calendar only when participating in interactions.
- **Boundaries:** availability search page, appointment confirmation page.
- **Controls:** query schedule; select time slot; reserve appointment; send reminder.
- **Entities:** Patient, Professional, Schedule, Appointment.
- **Alternatives:** no availability; cancellation; ineligible patient.
- **Domain sensitivity:** if clinical data is mentioned, report missing clinical entities in the delta rather than inventing them silently.

## Banking: Transfer Funds

- **Actor:** Customer; payment network or external banking system as secondary actor.
- **Boundaries:** transfer page, confirmation page, receipt screen.
- **Controls:** check balance; validate recipient; authorize transaction; record account movement; issue receipt.
- **Entities:** Account, Transaction, Beneficiary, AccountMovement.
- **Alternatives:** insufficient funds; invalid recipient; failed authorization; daily limit exceeded.
- **Note:** identity validation is a legitimate control. An external interaction may justify a secondary actor; an internal check does not require one.

## IoT monitoring: View Device Alerts

- **Actor:** Operator; device/sensor only if **external to the system**.
- **Boundaries:** monitoring dashboard, alert detail page.
- **Controls:** query readings; evaluate threshold; generate alert; notify operator.
- **Entities:** Device, Reading, Threshold, Alert.
- **Alternatives:** disconnected device; out-of-range reading; alert already handled.
- **Exclude:** implementation details such as frame parsing, buffer updates, or persisting a reading.

## Logistics: Dispatch Shipment

- **Actor:** Dispatcher; carrier and external tracking service as secondary actors.
- **Boundaries:** dispatch page, assignment page, shipping document.
- **Controls:** check vehicle availability; assign carrier; generate shipping document; send dispatch notification.
- **Entities:** Shipment, Vehicle, Carrier, ShippingDocument, Route.
- **Alternatives:** no available vehicle; invalid address; shipment already dispatched.

## Academic administration: Create Course

This domain comes from the worked course example and supports assessment of academic deliverables.

- **Actor:** Administrator or Coordinator. A Professor merely selected from a list is an **entity**, not an actor.
- **Boundaries:** actual creation window, such as “Create Course,” and confirmation screen/message.
- **Controls:** load professors and display window; check required fields; check code uniqueness; save course; show result message.
- **Entities:** Course, Professor.
- **Alternatives:** incomplete fields → “Incomplete fields” message and return to window; existing code → corresponding message and return. **Color both alternative-only paths.**
- **Typical discoveries:** a course catalog/list or course status implied by text but absent from the domain model.
- **Exclude:** a Create button boundary (it is an action from the window), database actors/entities, and Course operations.
- **Naming check:** replace repeated “Show” controls with names containing the actual message, as in the corrected course example.

## Checks for every domain

1. Entities derive from the supplied domain model; missing ones appear in the delta.
2. Actors agree with the use case diagram.
3. Every textual alternative has a diagram branch.
4. No noun-to-noun connection remains.
5. No technology, widget, or design-pattern names appear at the wrong abstraction level.
6. Controls read as specifically named actions.
7. The validator reports **zero errors**.
