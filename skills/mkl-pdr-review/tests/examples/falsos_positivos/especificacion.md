<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-02 — Register reservation request

**Primary Actor:** Requester
**Robustness diagram:** DR-02

Test note: the alternative flow is written here as **FA1**, without a hyphen,
while the diagram labels it **FA-01**. The normalization of flow identifiers must
match them; Otherwise, the coverage check would miss the mismatch.

## Basic flow

1. The Requester opens the Main Menu.
2. The system displays the consent form.
3. The Requester confirms and the system opens the Reservation Page.
4. The system checks for the available capacity.
5. The system registers the request by creating a Request.
6. The system displays the Request Certificate.

## Alternative flows

### FA1 — No capacity available

1. The system detects that there is no capacity is available.
2. The system displays the message "No capacity".
3. The system returns the Requester to the Reservation Page.
