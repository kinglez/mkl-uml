# Operation origins and explicit evidence

## Call matching

Exact call evidence uses the receiving classifier and complete, case-sensitive
operation name. A shared word, a name inside an argument, or a similar classifier
name cannot establish origin. Participant aliases resolve to their visible labels;
an explicit `instance : Classifier` label identifies its classifier. Inheritance
can forward actual calls to related declarations; an uninvoked ancestor declaration
does not itself provide call evidence.

For an overloaded operation, message argument expressions do not establish parameter
types. Keep its origin partial until an exact declared source disambiguates it.
Legacy natural-language labels provide review candidates using whole-label
normalization; token overlap never passes an operation. An unresolved natural-language
or receiver mapping produces a located partial check rather than a fabricated defect
or clean readiness. Wrong-receiver clues retain their historical warning.

## Origins outside an interaction

Use `--operation-evidence path/to/origins.json` when an operation belongs in the
model because of a requirement, contract or design decision outside the selected
interaction. This optional record is a local MKL checking convention, not a UML
requirement. Ordinary class-only modeling needs no record or invented sequence.

For example, put the actual contract in `contract.md`. If its second line is
`Worker.shutdown() is required by the framework lifecycle contract.`, this record
beside that file identifies the operation and its source:

```json
{
  "schema_version": 1,
  "operations": [{
    "classifier": "Worker",
    "operation": "shutdown",
    "kind": "contract",
    "source": "contract.md",
    "line": 2,
    "quote": "Worker.shutdown() is required by the framework lifecycle contract.",
    "rationale": "Required lifecycle operation outside the selected interaction."
  }]
}
```

Use the visible classifier name, not its PlantUML alias. `kind` is `requirement`,
`contract` or `decision`. Source files must be local, relative to the record and
contained in its directory tree; symlink escapes are rejected. `quote` matches the
complete indicated source line, ignoring surrounding whitespace. The rationale
states why that source supports this operation. Preserve the actual source instead
of manufacturing a contract to justify an unexplained member.

For overloaded operations, add `"parameters": "graceful : Boolean"`, using the
modeled parameter names, directions, types and defaults. Whitespace between tokens
does not matter. `"parameters": ""` selects the no-argument declaration. A name
that still selects multiple declarations is rejected. Each entry covers only the
selected declaration, never every overload or an operation in another classifier.

The checker validates the record, exact modeled declaration and current source
location. It reports **declared** origins; a reviewer still checks source authority
and semantic adequacy. Unknown/duplicate entries, stale excerpts and unreadable
sources are input errors (exit 2). Unlisted operations retain existing checks:
with a supplied interaction, missing origins remain findings (exit 1). Without an
interaction, declared origins can be inspected but interaction comparison remains
unverified. A located contract is not proof that a runtime implementation obeys it.

UML Operations and Messages follow OMG UML 2.5.1 §9.6 and chapter 17. Requiring an
MKL provenance record, selecting this JSON format and locating excerpts are local
tool conventions; UML does not require every operation in one selected interaction.
