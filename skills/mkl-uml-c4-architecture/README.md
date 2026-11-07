# MKL C4 Architecture

Model the official C4 zoom: system context → containers → components → code.
Draw the first three with C4-PlantUML; use scoped UML classes for code, and sequences
for complementary behavior. Deployment is a supporting view. See the code route in SKILL.md.

Read [SKILL.md](SKILL.md) for input handling, view selection, quality questions and handoffs.
External inputs can be any source or combination; no PRD template is required.

- [Modeling and review](references/modeling-and-review.md)
- [Quality requirements and decisions](references/quality-and-decisions.md)
- [Checker profile and record format](references/validation-profile.md)
- [Architecture brief](assets/architecture-brief.md)
- [Draft JSON record](assets/architecture-record.json)

From this skill directory, replace paths with actual files:
```bash
python3 scripts/validate_c4.py path/to/view.puml --level container
python3 scripts/validate_c4.py --record path/to/architecture.json --require-ready
```

Exit 0 means no detected structural errors; without the strict flag a draft can remain
unready. Exit 1 means findings or a failed strict gate. Exit 2 means an input/usage error.
The output separately states that rendering was not run and architecture semantics were
not verified. A ready declaration does not approve an architecture or certify quality.

Use an authorized local PlantUML installation for syntax/rendering:
```bash
plantuml -failfast2 -tsvg path/to/view.puml
```

The bundled C4 includes work without fetching remote macros. Preserve the source and
visually inspect rendered previews. A syntax pass cannot establish correct boundaries,
quality trade-offs or consistency with supplied business evidence.
