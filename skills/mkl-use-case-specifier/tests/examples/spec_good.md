<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-03 Register support request

| Field | Value |
|---|---|
| ID | CU-03 |
| Primary actor | Customer |

## Trigger
The Customer selects "New request" in the Support Portal.

## Preconditions
| ID | Precondition |
|---|---|
| PRE-01 | The Customer has an active account. |

## Basic flow
| Step | Responsible party | Action |
|---|---|---|
| 1 | System | Displays the Request Form. |
| 2 | Customer | Describes the problem and selects a Category. |
| 3 | System | Determines the Priority from the Category (RN-01). |
| 4 | Customer | Confirms registration. |
| 5 | System | Creates the Support Request and displays its reference number. |

## Alternate flows
| ID | Name | Condition | Outcome |
|---|---|---|---|
| FA-01 | Category no longer available | At basic-flow step 3, the selected Category is no longer available. | The System requests another Category, returns to step 2 and then rechecks the selection at step 3 before continuing. |

## Exception flows

No exception behavior is specified for this bounded example. Attachments are outside its scope; an attachment exception would require a supported submission/validation step and an explicit continuation or termination.

## Postconditions
The Support Request exists with an assigned reference number.

## Business rules
| ID | Rule |
|---|---|
| RN-01 | The Priority is derived from the Category. |

## Acceptance criteria
| ID | Criterion |
|---|---|
| CA-01 | Given an active Customer, when the Customer confirms a valid request, then the System displays its reference number. |
