<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-01 — Register vehicle entry

**Primary actor:** Operator
**Robustness diagram:** DR-01 · **Sequence diagram:** [pending PDR approval]

## Basic flow

1. The Operator registers the vehicle entry in the Entry Console.
2. The system identifies the Vehicle by its licensePlate.
3. The system checks availability of a ParkingSpace.
4. The system occupies the ParkingSpace with the Vehicle.
5. The system issues the entry Ticket.
6. The system presents the Entry Receipt to the Operator.

## Alternate flows

### FA-01 — No parking space available

1. The system detects that no ParkingSpace is available.
2. The system displays "Parking lot full" and does not issue a Ticket.
3. The system returns the Operator to the Entry Console.

## Business rules

- **RN-01** — A Vehicle cannot have two open entry Tickets simultaneously.
