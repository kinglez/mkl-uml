<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Checks between artifacts

What `scripts/validate_pdr.py` checks, which guideline supports each check, and—most importantly—**what it cannot detect**. A validator whose limits are not written invites you to trust it beyond its demonstrated capabilities.

## Invocation

```bash
python scripts/validate_pdr.py --robustez caso_03_robustez.puml \
                               --spec caso_03_especificacion.md \
                               --dominio modelo_dominio.puml \
                               --casos-uso casos_uso.puml
```

`--robustez` and `--spec` are repeated to review a complete package. Only `--robustez` is required; each absent input **deactivates specific layers**, which are declared as not executed in the output.

Exit codes: `0` no errors · `1` there are errors, the package does not pass · `2` usage error or file not found.

## Check table

| Check | Guideline | Level | Metric that feeds | Deterministic |
|---|---|---|---|---|
| Forbidden links between stereotypes | #5 | Error | syntax violations | Yes |
| Diagram without Controllers | #5 | Error | syntax violations | Yes |
| Robustness disguised as sequence | #2 | Error | — | Yes |
| Robustness entity absent from domain | #9 | Error | entities without domain | Yes |
| `FA`/`FE` flow of text without branch in diagram | #7 | Error | alternates without behavior | Yes |
| Enumerated flow without system behavior | #7 | Error | alternates without behavior | Heuristics |
| Basic flow without any system response | #6 | Error | — | Yes |
| Long streak of steps without system response | #6 | Warning | — | Heuristics |
| Design-pattern-itis in Controllers | #2 | Warning | — | Yes |
| Boundary object without its own name | #3 | Warning | — | Yes |
| Vocabulary drift | #3 | Warning | — | Heuristics |
| Actor absent from use case diagram | #3 / #5 | Warning | — | Yes |
| Unused domain classes | #9 | Information | — | Yes |
| Highlighter coverage | #10 | Warning by step | highlighter coverage | **Approximate** |
| Session budget | — | Information | — | Estimation |

**Diagnostic level and semantic certainty are different.** The proposed verdict uses reported errors, which include both deterministic profile violations and heuristic failure to recognize specified behavior. Inspect the diagnostic's basis before making a transition decision; neither an error nor a clean run replaces the semantic review. Preserve supported behavior and document representation limits rather than changing business rules to obtain a passing result.

---

## Detail and limits of each check

### Prohibited links (#5)

Consumes the nine connection rules defined by `/mkl-uml-robustness-diagram`; They are not redefined here. Count each arc that joins a forbidden pair: Actor↔Controller, Actor↔Entity, Boundary↔Entity, Entity↔Entity, Boundary↔Boundary, Actor↔Actor.

**Limit:** You only see relationships whose two ends are declared in the same file. A misspelled alias does not produce a syntax error, it produces a relationship that is silently ignored. If the relationship count seems low, suspect aliasing.

### Robustness disguised as sequence (#2)

Look for two families of signals:

- **Fragments and sequence directives:** `alt`, `else`, `opt`, `loop`, `par`, `critical`, `break`, `group`, `activate`, `deactivate`, `autonumber`, `participant`.
- **Messages with method signatures:** A tag containing `identifier(...)`, such as `checkStock(isbn)`.

Either of the two is enough to mark the diagram. A legitimate robustness diagram has none: its objects are declared once, its arcs have no direction, and its labels are phrases, not calls.

**Limit:** does not detect the subtle case of a diagram with correct robustness notation whose *level of detail* is already sequence. You judge that with step 6.

### Entity absent from the domain (#9)

Compares the set of entities from all diagrams against the classes of the domain model, using a normalized key: no accent marks, no capital letters, no separators and no stop words. Thus `VaccinationRecord`, `Vaccination Record` and `vaccination_record` count as the same concept.

**The report shows the names as they appear on each artifact**, not the normalized key, so you can break the tie.

**Limit:** normalization can unify two genuinely different concepts with very similar names. It is an accepted risk and the reason for showing the original names.

**The reverse sense is information, not defect:** Domain classes that the package does not use can be the scope of other use cases.

### Vocabulary drift (#3)

When an entity is missing from the domain, it is compared to each existing class by bigram similarity. If it exceeds the threshold, it is proposed as a **candidate** to be the same concept with another name — never as a certainty, and in the form of a question.

**Important and stated limit: this detects orthographic drift, not synonymous drift.** `VaccinationRecords` vs. `VaccinationRecord` is detected. **`Order` versus `Purchase` is not reliably detected**, because they share too little vocabulary: they are synonyms, and no lexical measure is going to match them. That case—which is the canonical example of the anti-pattern—requires human reading or a glossary. Don't rely on this check to rule out vocabulary drift; use it only for what you find.

### Coverage of alternative flows (#7)

Extracts the identifiers `FA`/`FE` from the specification and looks for them in the diagram's relationship tags and its notes. **Spellings are normalized**: `FA-01`, `FA1`, `FA 1` and `fa_01` count as the same identifier, on both artifacts and in any combination.

This matters more than it seems: a check that requires an exact spelling is **mute** with the other, and a silent check is worse than none because it produces reassuring silence. Spelling conventions vary between teams and documents; the validator should not impose one.

**Advantage over the robustness validator:** this checks against the actual specification file, not against a note embedded in the diagram. It doesn't depend on whether someone remembered to paste the text.

### Flow without behavior (#7)

The supported profile recognizes numbered system steps and substantive compact Markdown flow tables. In a flow section, a table's action/behavior column must identify system behavior through its heading, an explicit System/Sistema role, or the action text. A flow row also needs an anchor/condition/trigger or outcome column. For example:

```markdown
## Alternative flows
| Flow | Trigger | System behavior | Exit |
| --- | --- | --- | --- |
| FA-01 | Coupon is eligible | Applies the capped discount | Resume basic step 6 |
| FE-01 | Coupon is unknown | Emits an unknown-Coupon refusal | Terminate without a quote |
```

English and existing Spanish headers/roles are supported. Inline-code and escaped pipes do not split a cell. Source/reference/traceability cells, ID-only content, empty/TBD action cells, comments, quoted examples and fenced/indented code do not establish behavior. An outcome column cannot substitute for an explicitly unfinished action column. The specification still needs usable numbered basic behavior for its dependent full-specification checks.

**Limit:** this is structured lexical recognition, not a semantic action parser. It cannot prove that a guard, effect or continuation is correct or complete; vague non-placeholder prose may still be recognized. Inspect those meanings and cross-artifact correspondence even when the table passes. An unsupported representation remains a declared coverage limit, not a reason to invent or remove business behavior.

### Completeness of the dialogue (#6)

Only on **basic flow** — alternates are judged with guideline #7. Two checks of different nature:

- **No step mentions system:** error. It is the anti-pattern of the unilateral use case and is unambiguous.
- **Streak of consecutive steps without system response above threshold:** warning. It can be legitimate if the user fills out a form in several steps.

**Limit:** detects the system by the word "system". A specification that says "the application validates" or "the module registers" will not be recognized. It's a real limitation; is offset by the writing convention required by `/mkl-use-case-specifier`.

### Design-pattern-itis (#2)

Searches for solution space terms in the Controller names: `factory`, `singleton`, `strategy`, `proxy`, `observer`, `dao`, `repository`, `impl`, `handler`, `servlet`, `dto`, `orm` and so on.

**Two symmetrical errors, both made and both corrected**, which explain why this check is the way it is:

1. Searching for **substring** produces false positives: flag `Show payment form` for containing `form`.
2. Searching by **whole word without further ado** produces false negatives: `RecordDAOFactory` collapses to a single word when normalizing, and `\bdao\b` never finds a boundary. The check remains **mute just in the names that need it most**.

The solution is to separate the CamelCase **before** searching by word: `RecordDAOFactory` → `Record DAO Factory`. The `pattern_itis` and `falsos_positivos` fixtures protect both directions at the same time.

### Boundary object without its own name (#3)

Marks a Boundary object only if its name **is** generic —`screen`, `page`, `form`, `window`— not if it **contains** it. `Reservation Page` and `Main Menu` are proper names and are not marked.

### Highlighter Coverage (#10)

For each step of the text, its significant terms are searched among the element names and diagram labels. A step counts as covered if there is an overlap.

**It is the least reliable check of the set and the output says it every time.** Its limits:

- 100% does not prove that the diagram is correct: it proves that the words match.
- The legitimate synonyms—the text says "verifies", the diagram "validates"—lower the figure without any defect.
- The reverse direction, an element of the diagram that is left over, is detected worse than an uncovered step.

It is published as a number **accompanied by the warning**, and feeds the verdict only by threshold, never as a sole criterion. You perform the actual highlighter test phrase by phrase.

### Session budget

Estimates equivalent pages from the file volume and divides it by the rate of **3-4 pages/hour** that IEEE 1028 §6.5.2 sets for preliminary design. If the result exceeds a sustainable meeting, notify and propose splitting the package.

**Limit:** The equivalence of lines to pages is a convention declared in the script itself, not a measurement. It is used to detect a disproportionate package, not to plan up to the minute.

---

## What no automatic check can do

Four guidelines are, wholly or partially, outside the scope of a script. They are in the record as layers that **you** run:

- **#4, technical and non-technical.** No script knows who was in the room or if they understood. It is verified in the list of participants.
- **#3, the right level of abstraction.** Technical jargon can be detected; You cannot measure whether a customer understands the use case. That's only what the client says.
- **#1, step 3: logical flow and not implementation.** It requires judging whether the sequence described is that of the problem or that of the solution.
- **#8 on the GUI-dependent part.** Without wireframe there is no way to check that a screen field exists. With wireframe, the matrix is completed by hand.

The validator is the preparation phase, and that is where the evidence places most defect detection of an inspection. But **preparation is not review**: a verdict issued only with the output of the script is a half-verdict, and the record must say which of the two things happened.

## Scope of cross-artifact checks

Run applicable checks for the selected artifact scope. A missing optional domain model or actor diagram means the related comparison was not performed; independent checks still proceed. Entity closure compares only domain concepts. Human/machine interface names trace to interface evidence and actor-role names to external participation evidence, not the domain class list. A newly discovered supported entity may be recorded as a pending delta when upstream editing is outside scope. Lexical matches, generic-name heuristics, and vocabulary similarity are review candidates rather than semantic proof.
