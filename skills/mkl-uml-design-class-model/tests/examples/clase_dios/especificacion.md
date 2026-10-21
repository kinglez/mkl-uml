<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-04 — Manage copy loan

**Primary actor:** Librarian · **Secondary actor:** Member
**Robustness diagram:** DR-04 · **Class model:** [assembly pending]

## Basic flow

1. The Librarian opens the Loan Console and searches for the Member by identityDocument.
2. The system verifies that the Member has no active Penalty.
3. The Librarian enters the callNumber of the requested Copy.
4. The system checks that the Copy is available.
5. The system calculates the dueDate from the material type of the Work.
6. The system registers the Loan with its startDate and dueDate.
7. The system displays the receipt to the Librarian.

## Alternate flows

### FA-01 — Member has an active penalty

1. The system detects a Member Penalty whose endDate has not passed.
2. The system displays the penalty reason and does not register the loan.

### FA-02 — Copy is unavailable

1. The system detects that the Copy status prevents a loan.
2. The system informs the Librarian and does not register the loan.

## Business rules

- **RN-01** — A Member with an active Penalty cannot borrow copies.
- **RN-02** — The loan period depends on material type: audiovisual copies
  have a shorter loan period than books.
