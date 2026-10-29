<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Traceability and review headers

Use traceability to explain why the design exists and header inspection to check how its modeled contracts translate. This original guidance is informed by Rosenberg & Stephens (2007), chapter 9, and the course material recorded in [sources-and-methods.md](sources-and-methods.md). It does not reproduce the source text.

## Traceability matrix

For each selected requirement, identify its use cases, interactions or architecture decisions, responsible classes/operations and tests. Inspect the reverse direction too: a design element without a literal business requirement may still be justified by an interface, framework or technical design decision. Record that actual origin.

| Requirement/decision | `CU-XX` | `DS-XX` | Classes/operations | `CP-XX` | Evidence status |
|---|---|---|---|---|---|
| Cited obligation or justified decision | Realizing scenario | Interaction or scoped link | Responsible contract | Observable verification | Verified, unresolved or unavailable |

Report missing realization and unjustified structure separately. Nonfunctional requirements may be realized by architecture, configuration and constraints across several classes rather than a single named operation. A vocabulary match only suggests where to inspect; it cannot establish full realization, and synonyms can be missed.

Preserve IDs across edits. Allocate new IDs for new identities, retire deleted identities without reuse, and record replacement/alias links. Verify references resolve to current or explicitly retired/replaced items. A standalone review reports available links without inventing the full pipeline.

## Generate and inspect headers

Generate headers when requested or included in the user's existing authorization. Use an output path distinct from every input, including equivalent filesystem identities. Treat the result as an inspection artifact rather than production code; unresolved signatures and unsupported fidelity must remain visible.

Compare generated output with the model:

- Every intended class, significant property and operation remains represented.
- Aliases resolve to their displayed types and relationships.
- Each parameter and nested generic type is preserved.
- Derived properties retain their derivation intent.
- Relationship roles and target multiplicities produce an appropriate reference/collection or an explicit unresolved representation.
- Unmodeled types and unsupported constructs are reported rather than guessed.

Inspect the design meaning too: duplicate members, inappropriate dependencies or unclear contracts can become easier to see as signatures. Successful generation alone is not completed header inspection and does not supply human sign-off.

## Effort and boundary

Estimate inspection from actual output size and a declared project rate when scheduling matters. The upstream IEEE 1028 §6.5.2 source-code row has unresolved page/line units; it is not a mandatory budget. See [session-budget.md](session-budget.md).

CDR assesses readiness of the selected design for implementation. Reconciling a model with already implemented code belongs to the requested code-review/model-update scope. Retain model provenance and report any scope limits at that handoff.
