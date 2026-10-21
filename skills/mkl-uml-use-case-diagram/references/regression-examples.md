<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Cross-Domain Regression Examples

Use these examples to test whether the skill generalizes and avoids overfitting to one domain. These are not complete diagrams; they define expectations. Treat every example as domain-specific regression data, never as a reusable default template. Do not transfer actors, use cases, packages, or relationships from one example to another unless the current verbal model explicitly supports them.

## Hotel reservation

Verbal signal: `Use case: Reserve room`.

Expected compact version:

- Primary actor: Customer.
- Possible secondary actor: Payment gateway/service if external payment validation is mentioned.
- Dominant use case: Reserve room.
- Allowed supporting use cases: Check availability, Select accommodation option, Submit reservation details/request, Validate payment or guarantee, Confirm reservation, Generate electronic confirmation if externally meaningful.

Expected enriched academic version:

- Suggested packages: Accommodation search and selection; Reservation management; Payment, guarantee, and communication.
- Additional allowed use cases when traceable: View accommodation options, Submit reservation request, Evaluate reservation conditions, Get reservation quotation, Report reservation inconsistency.
- Possible secondary actors: Payment gateway/Financial institution; Electronic notification service if the verbal model mentions electronic confirmation or external delivery.
- `Evaluate reservation conditions` is allowed as an aggregate service for tariff validity, real availability, occupancy, special dates, and promotions; do not split those rules into separate use cases unless independent external interaction exists.
- `Get reservation quotation` is allowed when the total value is visible to the client before confirmation.
- Usually forbidden as use cases: Validate rate validity, validate actual availability, validate restrictions individually, update availability, generate identifier, save reservation, record in database.

## Academic enrollment

Verbal signal: student enrolls in courses for a term.

Expected:

- Actors: Student, External academic system only if stated, Coordinator/Administrator only if they interact.
- Dominant use case if one scenario: Enroll in course / Complete enrollment.
- Allowed supporting use cases: View academic offering, Select course, Confirm enrollment.
- Usually forbidden: validate capacity, update schedule, save enrollment, check prerequisites unless external service or independent actor goal.

## Healthcare appointment

Verbal signal: patient schedules a medical appointment.

Expected:

- Actors: Patient, Healthcare professional/external scheduling system only if interacting, Payment gateway only if stated.
- Dominant use case: Schedule medical appointment.
- Allowed: Check availability, Select professional/specialty, Confirm appointment, Send confirmation if meaningful.
- Usually forbidden: validate internal availability, update appointment schedule, generate code, save appointment.

## Banking transfer

Verbal signal: customer transfers funds.

Expected:

- Actors: Customer, External banking system/Payment network if external.
- Dominant use case: Transfer funds.
- Allowed: Log in only if authentication explicit, Validate identity/OTP if external/security interaction is stated, Confirm transfer, Issue receipt.
- Usually forbidden: debit account, update balance, persist transaction as separate use cases unless actor-visible service requires explicit modeling.

## E-commerce order

Verbal signal: buyer places an order.

Expected:

- Actors: Buyer, Payment gateway, Shipping service if external and interacting.
- Dominant use case: Place order.
- Allowed: Search product, Select product, Pay for order, Check shipment status if independent.
- Usually forbidden: calculate tax, update inventory, save order, generate ID.

## IoT monitoring

Verbal signal: device transmits sensor data and user monitors alerts.

Expected:

- Actors: User/Operator, Device/Sensor if external to the system, Notification service if external.
- Dominant use case depends on narrative: Monitor condition, Synchronize device, Receive alert.
- Allowed: Configure threshold if actor goal, View history if actor goal.
- Usually forbidden: parse frame, calculate internal average, update buffer, persist reading.

## Logistics dispatch

Verbal signal: dispatcher schedules shipment delivery.

Expected:

- Actors: Dispatcher, Carrier, External GPS system/provider if interacting.
- Dominant use case: Dispatch shipment / Schedule delivery.
- Allowed: Assign carrier, Check vehicle availability, Send dispatch notification.
- Usually forbidden: update internal state, recalculate route unless actor explicitly requests it or external service is modeled.

## HR recruitment

Verbal signal: recruiter manages candidate hiring process.

Expected:

- Actors: Recruiter, Candidate, External assessment service if interacting.
- Dominant or multi-use-case depending on scenario: Publish vacancy, Apply for vacancy, Evaluate candidate.
- Usually forbidden: save resume, filter internally, calculate score unless actor-visible service.

## Manufacturing incident report

Verbal signal: operator reports production incident.

Expected:

- Actors: Operator, Supervisor, External maintenance system if interacting.
- Dominant use case: Report incident.
- Allowed: Attach evidence if actor goal, Check incident status, Assign owner if supervisor goal.
- Usually forbidden: update logbook, generate sequential number, validate fields.
