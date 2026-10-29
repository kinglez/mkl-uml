<!-- mkl fixture. Copyright 2026 kingle.zhuang. -->
# CU-07 — Register incident

**Primary Actor:** Requester
**Requirements realized:** RF-01, RF-02, RF-03
**Robustness diagram:** DR-07 · **Sequence diagram:** DS-07
**Class model:** MC-07

## Preconditions

| ID | Precondition |
|---|---|
| PRE-01 | The Requester is authenticated. |

**Postconditions:** A registered Incident has an identifier and due date; rejected requests create no incident.

## Trigger

The Requester chooses to register an incident.

## Basic flow

1. The Requester opens the Incident Form and describes the problem.
2. The system checks that the Requester is authorized for the specified Category.
3. The system obtains the current ServiceAgreement for that Category.
4. The system calculates the due date by applying the deadline in the agreement.
5. The system registers the Incident with its description and its due date.
6. The system shows the Requester the Incident identifier and due date.

## Alternative flows

**FA-01** — Requester is not authorized for the category; the flow terminates.

1. The system detects that the Requester is not authorized for the specified Category.
2. The system reports the reason and does not register the incident.

**FA-02** — The Category does not exist; the flow terminates.

1. The system cannot find the indicated Category.
2. The system reports the problem and does not register the incident.

## Business rules

| ID | Rule |
|---|---|
| RN-01 | A Requester may register incidents only in categories for which they are authorized. |
| RN-02 | The deadline depends on the current service agreement for the category. |

## Acceptance criteria

| ID | Criterion |
|---|---|
| CA-01 | An authorized requester submitting an existing category receives an Incident identifier and due date. |
