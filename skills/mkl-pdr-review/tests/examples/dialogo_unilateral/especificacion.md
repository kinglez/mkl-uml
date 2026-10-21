<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# CU-01 - Register vaccination

**Primary Actor:** Veterinarian
**Robustness diagram:** DR-01

## Basic flow

1. The Veterinarian opens the Pet Clinical Record.
2. The Veterinarian searches for the Pet by name.
3. The Veterinarian selects the Vaccine to administer.
4. The Veterinarian enters the dose and notes.
5. The Veterinarian confirms the vaccination record.
6. The Veterinarian downloads the Vaccination Certificate.

## Alternative flows

### FA-01 - The vaccine does not match the vaccination schedule

1. The system displays the message "Vaccine not applicable."
2. The system returns the Veterinarian to the Pet Clinical Record.
