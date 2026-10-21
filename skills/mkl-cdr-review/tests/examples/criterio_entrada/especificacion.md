<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-07 — Register incident

*This release also includes CU-08 (escalate incident).*

**Primary Actor:** Requester
**Requirements realized:** RF-01, RF-02, RF-03
**Robustness diagram:** DR-07 · **Sequence diagram:** DS-07
**Class model:** MC-07

## Basic flow

1. The Requester opens the Incident Form and describes the problem.
2. The system checks that the Requester is authorized for the specified Category.
3. The system obtains the current ServiceAgreement for that Category.
4. The system calculates the due date by applying the deadline in the agreement.
5. The system registers the Incident with its description and its due date.
6. The system shows the Requester the Incident identifier.

## Alternative flows

### FA-01 — requester is not authorized for the category

1. The system detects that the Requester is not authorized for the specified Category.
2. The system reports the reason and does not register the incident.

### FA-02 — The Category does not exist

1. The system cannot find the indicated Category.
2. The system reports the problem and does not register the incident.

## Business rules

- **RN-01** — A Requester may register incidents only in
  categories for which they are authorized.
- **RN-02** — The deadline depends on the current service agreement
  for the category, rather than on the individual incident.
