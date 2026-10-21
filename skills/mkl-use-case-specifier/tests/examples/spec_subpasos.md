<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-05 Renew loan

| Field | Value |
|---|---|
| Primary actor | Student |

## Trigger
The Student requests renewal in the Library Portal.

## Preconditions
| ID | Precondition |
|---|---|
| PRE-01 | The Loan is active. |

## Basic flow
| Step | Responsible party | Action |
|---|---|---|
| 1 | System | Displays the Loan List. |
| 2 | Student | Selects the Loan and confirms renewal. |
| 3 | System | Records the new Return Date (RN-01). |

## Alternate flows
| ID | Name | Condition | Outcome |
|---|---|---|---|
| FA-01 | Copy reserved by someone else | An active Reservation exists | The System rejects renewal and ends the use case. |

### Alternate flow FA-01 detail
| Step | Responsible party | Action |
|---|---|---|
| FA-01.1 | System | Checks the active Reservation. |
| FA-01.2 | System | Informs the Student and ends the use case. |

## Postconditions
The Loan is renewed with a new Return Date.

## Business rules
| ID | Rule |
|---|---|
| RN-01 | A Loan may be renewed at most twice. |

## Prototypes, GUI, or interface references
| Element | Name |
|---|---|
| Visible endpoint | Student Loan Inquiry |

## Acceptance criteria
| ID | Criterion |
|---|---|
| CA-01 | Given an active Loan, when the Student confirms renewal, then the System displays the new Return Date. |
