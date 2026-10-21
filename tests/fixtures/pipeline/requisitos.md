<!-- mkl fixture. Copyright 2026 kingle.zhuang. -->
# Requirements — Technical Support Desk, release 1

## Functional

- **RF-01** — The system must allow a requester to register an incident
  with its category and a description of the problem.
- **RF-02** — The system must calculate each incident's due date
  from the current service agreement for its category.
- **RF-03** — The system must reject registration when the requester
  is not authorized for the specified category.

## Non-functional

- **RNF-01** — The due date calculation must apply the current deadline policy
  independently of the client's calendar, so that the policy
  can change without modifying the incident.
