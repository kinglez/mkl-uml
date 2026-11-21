# Message ordering evidence

Use `--ordering-evidence` when a requirement, contract or design decision states
that one modeled message must precede another. Check that the messages represent
the stated events. Select the reply that establishes a successful result when the
rule depends on success. A request to perform the check or a reply carrying an
unspecified decision does not establish success.

In this example, line 2 of `contract.md` reads “Publish the outcome only after
the commit has succeeded.” The adjacent record maps that rule to one sequence.

```json
{
  "schema_version": 1,
  "rules": [{
    "id": "ORD-01",
    "sequence": "interaction.puml",
    "source": "contract.md",
    "line": 2,
    "quote": "Publish the outcome only after the commit has succeeded.",
    "before": {"sender": "Store", "receiver": "Service", "label": "commitSucceeded"},
    "after": {"sender": "Service", "receiver": "Client", "label": "outcomePublished"}
  }]
}
```

```bash
python scripts/validate_cdr.py --clases path/to/classes.puml \
  --secuencia path/to/interaction.puml --ordering-evidence path/to/ordering.json
```

Use IDs unique within the record. Paths in the record are relative to its directory
and stay within that directory tree. Supply each reviewed sequence with
`--secuencia`. The source quote must match the complete indicated line, ignoring
surrounding whitespace. Select messages by the exact sender, receiver and label,
using the identifiers written on the arrows. For a left-pointing arrow, the sender
is on the right. Include any message-sort annotation in the label.

## Coverage

For each occurrence of `after`, every supported path that reaches it must have
already reached `before`. A `before` on a different alternative cannot satisfy the
rule. A path that terminates or omits the controlled message needs no prerequisite.
The check applies to the stated pair within one interaction. The prerequisite
remains satisfied once observed. The rule does not independently check whether it
needs to be renewed for another request, resource or loop iteration.

The literal profile uses the displayed order and checks nested `alt`, `opt`,
`group` and `loop` fragments. An `alt` without a bare `else` may skip all operands.
`opt` and `loop` may be skipped. A taken, guarded top-level `break` stops the
remainder of the interaction. Guards are named conditions whose truth the checker
does not infer. The profile leaves parallel or critical fragments, nested or
unguarded breaks, and unparsed or malformed statements unverified. Review those
interactions using their actual execution and guard semantics.

The tool reports each violation at the controlled message and returns exit 1.
An unmatched `after`, unsupplied sequence or unsupported profile leaves the rule
partial with a located diagnostic. Without the record, ordering appears as
unperformed and the existing standalone checks still run. Invalid records and
stale source quotes return exit 2. The reviewer checks source authority and the
meaning of the mapped events. Passing the check establishes the modeled order
within this profile. Runtime ordering still requires its own evidence.
