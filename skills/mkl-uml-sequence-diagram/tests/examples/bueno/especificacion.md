<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-01 — Register vehicle entry

**Primary actor:** Operator
**Robustness diagram:** DR-01 · **Sequence diagram:** DS-01

## Basic flow

1. The Operator registers the vehicle entry in the Entry Console.
2. The system identifies the Vehicle by its licensePlate.
3. The system checks that the Vehicle has no open entry Ticket (RN-01).
4. The system checks availability of a ParkingSpace.
5. The system occupies the ParkingSpace with the Vehicle.
6. The system issues the entry Ticket.
7. The system presents the Entry Receipt, including the Ticket and ParkingSpace, to the Operator.

## Alternate flows

### FA-01 — No parking space available

**Trigger:** basic-flow step 4 finds no available ParkingSpace.

1. The system detects that no ParkingSpace is available.
2. The system displays "Parking lot full" and does not issue a Ticket.
3. The system returns the Operator to the Entry Console.

### FA-02 — Vehicle already has an open entry Ticket

**Trigger:** basic-flow step 3 detects an existing open Ticket.

1. The system identifies the existing open Ticket.
2. The system tells the Operator that entry is rejected and creates no new Ticket.
3. The use case terminates.

## Business rules

- **RN-01** — A Vehicle cannot have two open entry Tickets simultaneously.
