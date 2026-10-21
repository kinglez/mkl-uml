<!-- mkl fixture. Copyright 2026 kingle.zhuang. -->
# Test plan — release 1, CU-07 Register incident

The cases are derived from the controllers in robustness diagram DR-07,
the verification unit defined by the method.

## Cases derived from controllers

- **CP-01** — Verify Requester Authorization: a requester authorized for the
  category passes the check.
- **CP-02** — Verify Requester Authorization, negative path (**FA-01**): a
  requester without authorization for the category is rejected, and the
  incident is not registered.
- **CP-03** — Resolve Agreement: the category returns the current
  service agreement.
- **CP-04** — Resolve Agreement, negative path (**FA-02**): an unknown category
  stops the flow without registering the incident.
- **CP-05** — Calculate Due Date: the due date is the registration date
  plus the deadline in the agreement.
- **CP-06** — Register Incident: the incident is registered with its
  description, registration date and due date, and an identifier is returned.

## Coverage

| Flow | Cases |
|---|---|
| Basic | CP-01, CP-03, CP-05, CP-06 |
| FA-01 | CP-02 |
| FA-02 | CP-04 |
