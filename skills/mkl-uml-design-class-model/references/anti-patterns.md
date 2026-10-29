<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Design-class review candidates

This original catalog adapts responsibility and model-quality concerns from Rosenberg & Stephens (2007), chapters 8–9; Fowler, *UML Distilled* (3rd ed.), chapters 3–4; and Rosenberg, Stephens & Collins-Cope (2005). Inspect the user's actual material rather than transplanting source examples.

| # | Candidate | Evidence-based response |
|---|---|---|
| 1 | An operation, attribute or relationship has no supported origin. | Check domain/scenario/interface evidence, architecture, configuration, framework contracts and design decisions. Technical state need not be named in business text. Record a real gap rather than manufacturing provenance. |
| 2 | A non-domain class lacks a declared solution role. | Identify whether it is a justified technical collaborator, late domain discovery or undeclared alias. A stereotype requires an actual rationale. |
| 3 | Names drift between domain and design. | Preserve concept identity or document the intentional rename and affected links. Similarity is only a lexical clue. |
| 4 | Domain classes hold data while all state-dependent decisions occur elsewhere. | Inspect the architectural style and contracts before moving behavior to the state owner. Data carriers can be legitimate. |
| 5 | A class holds unrelated state or operations. | Examine independent responsibilities and change reasons; consider a supported split. Counts cannot measure semantic cohesion. |
| 6 | A class has no significant operations. | Check value-object, interface and contract roles before treating the class as incomplete. |
| 7 | A domain Entity has no attributes. | Compare required data and intended scope; recover supported state or record missing evidence. |
| 8 | Many tiny classes fragment a coherent responsibility. | Investigate collaboration and change coupling; a small service may still have a clear purpose. |
| 9 | One class dominates operations/state/relationships. | Inspect actual responsibilities rather than declaring it incorrect from size alone. |
| 10 | A pattern or technical collaborator has no demonstrated need. | Check scenarios and architecture/framework contracts; justify it or remove unsupported structure within scope. |
| 11 | Generated accessor detail hides significant operations. | Omit trivial accessors when inferable; retain those with a meaningful contract. Ordinary business verbs remain ordinary operations. |
| 12 | Low-level helpers couple the diagram to incidental implementation. | Show the significant contract and include internal behavior only when needed to assess the selected design. |
| 13 | Excessive detail makes the model difficult to use. | Retain the properties, operations and dependencies needed to answer the design question. |
| 14 | Classified calls require operations absent from their receiving classifiers. | Verify actual signatures and selected scope, then reconcile the supported operation delta. Word overlap is only a candidate check. |
| 15 | An operation belongs to a different receiver than its originating call. | Verify call sort, signature and responsibility before changing either artifact; replies and Signals do not create reverse operations. |
| 16 | Layout work displaces unresolved content. | Close evidence-backed content gaps before polishing presentation. |

## Heuristic boundaries

Size, coupling and vocabulary-similarity thresholds are local warning criteria, not UML/ISO limits or proof of a defect. Use the installed validator's actual configuration/output rather than copying a historical numeric cache. A solution stereotype does not exempt unsupported state, and absence from a business use case does not invalidate justified technical state.

Use [provenance-rules.md](provenance-rules.md) for the accepted origin categories and [notation-rules.md](notation-rules.md) for message, property and relationship semantics. Correct the originating scenario, vocabulary or design decision when needed; do not conceal the gap by editing only the class-model name.
