<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Requirements — Technical Support Desk, release 1

## Functional

- **RF-01** — The system must allow a requester to register an incident
  with its category and a description of the problem.
- **RF-02** — The system must calculate each incident's due date
  from the current service agreement for its category.
- **RF-03** — The system must reject registration when the requester
  is not authorized for the specified category.

- **RF-90** — The system must export a quarterly digest in a portable
  format for the supplier's external audit.

## Non-functional

- **RNF-01** — The due date calculation must apply the current deadline policy
  independently of the client's calendar, so that the policy
  can change without modifying the incident.
