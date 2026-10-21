<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Figure notes: visual evidence supporting the rules

This record identifies source figures **opened and visually checked during the original skill's development**, and the rules each supports. It makes provenance auditable and avoids repeating the same evidence search. These checks are upstream records, not new verification performed for this translation.

The figures come from the original author's personal copy of Rosenberg and Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice*. That copy is not distributed here. The robustness-analysis chapter contains most of the applicable visual evidence.

## Verified warning about filenames

Figure numbers embedded in extracted filenames **do not reliably match the actual figures**: extraction associated images with following Markdown text rather than their own captions. The upstream author observed this in six of ten opened examples.

**Open the image before citing a figure number.** Filenames are useful for locating evidence, not establishing citation numbers.

## Three-stereotype notation

| Source filename | Observed content | Supported rule |
|---|---|---|
| `..._p126_figure_5_2_5_2_however_a_robustness_reads_more_like_an_activity.png` | Jacobson boundary/entity/control icons, with nouns over boundary/entity and a verb/action over control | Noun/verb distinction underlying connection rules |

The filename misleadingly mentions “activity”; the image actually shows notation.

## Valid and invalid connections

| Source filename | Observed content | Supported rule |
|---|---|---|
| `..._p126_figure_5_8_5_8_all_of_possible_valid_relationships_shown_even_though.png` | Enterprise Architect's “Robustness Broken Rules” tab displays five illegal connections and validator messages: actor–entity, actor–control, boundary–entity, boundary–boundary, and entity–entity | Most direct source formulation for the validator's hard rules |
| `..._p126_figure_5_5.png` | “Robustness Rules” tab shows actor → page → control → entities, MKL palette, and zero validation errors | Positive counterpart demonstrating compliant structure |
| `..._p151_figure_5_24_..._violates_a_robustness_diagramming_relationship.png` | “Create New Account” excerpt circles a boundary-to-boundary connection and identifies the violation | Anti-pattern 1: noun-to-noun connection and its visual diagnosis |

## Complete examples

| Source filename | Observed content | Supported rule |
|---|---|---|
| `..._p176_diagram_finished_write_customer_review_robustness.png` | The strongest corpus example, “Write Customer Review,” has adjacent use case text, actual screen names, yes/no control branches, entities, invoked use cases, and red alternative-only objects | Attached text note; all alternatives in one diagram; inclusion of invoked use cases |
| `..._p126_diagram_1_remember_a_robustness_is_an_object_picture_of_a.png` | Complete “Login” example with side text, decision controls, and red alternatives for locked account, password sent, and invalid credentials | Alternative courses with distinct outcomes |

## Error examples before and after correction

| Source filename | Observed content | Supported rule |
|---|---|---|
| `..._p151_figure_5_20_..._excerpt_a_robustness_showing_an_invalid_relationship_exercise.png` | BEFORE: “Add External Books to Catalog” includes an `Extends` relationship and entity notes containing `save(): void` / `validate(): void` | Misplaced inheritance and premature operation assignment |
| `..._p151_figure_5_26_..._errors_highlighted_5_27.png` | AFTER: removes inheritance/operations, adds a red error boundary for alternatives, and redirects validation controls | Corrected abstraction level and required validation failure paths |
| `..._p151_figure_5_22_..._shows_at_least_five_modeling_errors_including_at.png` | “Search Catalog” invokes another use case but has no entities although text names Catalog, Criteria, and Results | Omitted textual entities |
| `..._p151_figure_5_21_..._robustness_add_external_books_to_catalog_use_case.png` | “Checkout” actor directly touches two boundaries, one a button with no control connection | Widget boundary and diagram/text mismatch |

## Course material: robustness-analysis chapter

This second visual source supplies Spanish terminology and worked exercises absent from the English books. **The following four figures were individually opened and visually checked in the original development.**

| Figure | Observed content | Supported rule |
|---|---|---|
| **5.3 — Robustness rules** | Colored **4×4 YES/NO matrix** for actor, boundary noun, entity noun, and control verb | Confirms four permitted/four prohibited combinations and explicitly marks actor–actor NO, supporting rule 9 |
| **5.20 — Complete Create Course example** | Use case text on the left, yes/no control branches, **red error-message controls**, and a long action label originating at the actor | Alternative coloring, two/three-zone layout, actor-origin action convention |
| **5.13 — Exercise 2 with errors marked** | Four red annotations identify missing validation alternatives, no basic-course correspondence, extension relationships, and excessive implementation detail such as `insert():void` / `validate():void` | Independently confirms anti-patterns 9, 9-bis, 13, and 14 |
| **5.14 — Corrected Exercise 2** | Each validation gains a no branch to a **red** control with the actual error message in its name; removes extension and operation notes | Canonical anti-pattern 9 correction and specific presentation-control names |

**Cataloged without individual image inspection:** incremental example construction (figures 5.15–5.19); three-zone layout (figure 5.5); and the two action-origin conventions (figures 5.6/5.7). Their content was read in extracted text, rather than verified from images. This distinction preserves the inspection boundary.

## Evidence absent from the corpus

- No dedicated figure demonstrates actor or use case generalization in robustness diagrams; those topics are described only in prose.
- *Agile Development [abbreviated title]* supplies process context. Its robustness figures are case-study illustrations, not a notation tutorial.
