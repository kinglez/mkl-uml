<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-01 — Register vaccination

**Primary Actor:** Veterinarian
**Robustness diagram:** DR-01

## Basic flow

1. The Veterinarian opens the Pet Clinical Record and selects the Vaccine to administer.
2. The system checks the Pet's vaccination schedule against the Vaccine interval.
3. The system registers the vaccination by creating a VaccinationRecord with the administration date and dose.
4. The system issues a vaccination certificate.
5. The system displays the Vaccination Certificate to the Veterinarian.

## Alternative flows

### FA-01 — The Vaccine does not match the vaccination schedule

1. The system detects that the selected Vaccine does not correspond to the Pet's current vaccination schedule.
2. The system displays the message "Vaccine does not apply" and does not create the record.
3. The system returns the Veterinarian to the Pet Clinical Record.

## Business rules

- **RN-01** — A Vaccine must not be administered before its interval in months has elapsed since the last dose.
