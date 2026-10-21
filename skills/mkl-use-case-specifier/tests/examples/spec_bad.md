<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-07 View history

| Field | Value |
|---|---|
| Primary actor | User |

## Trigger
The User opens the screen.

## Preconditions
| ID | Precondition |
|---|---|
| PRE-01 | A session is active. |
| PRE-01 | The User has permission. |

## Basic flow
| Step | Responsible party | Action |
|---|---|---|
| 1 | System | Displays the screen. |
| 2 | User | Enters the data. |
| 3 | System | The information is validated against the database. |
| 4 | System | The result is saved in the audit table. |
| 5 | System | Displays a dropdown with the options. |
| 6 | User | Selects an item (RN-05). |
| 7 | System | Queries the reporting endpoint. |
| 8 | System | Displays the fields. |
| 9 | User | Confirms. |
| 10 | System | The event is registered. |
| 11 | System | The counter is updated. |
| 12 | User | Reviews the message. |
| 13 | System | The report is generated. |
| 14 | User | Downloads. |
| 15 | System | The copy is stored. |
| 16 | System | Closes. |

## Alternate flows
| ID | Name | Condition |
|---|---|---|
| FA-01 | No results | No matches exist |

## Business rules
| ID | Rule |
|---|---|
| RN-01 | Only the user's own records may be viewed. |
