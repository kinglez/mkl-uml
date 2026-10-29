<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sources and verification boundaries

This record distinguishes historical upstream research from checks performed for this revision. Supporting instructions are independently worded operational guidance; references identify influences and do not grant redistribution rights for the original works. The private source corpus and source artwork are not bundled. See the repository's `docs/THIRD_PARTY_SOURCES.md` for the content inventory.

## Historical method research

| Source | Contribution | Evidence boundary |
|---|---|---|
| Rosenberg & Stephens (2007), *Use Case Driven Object Modeling with UML: Theory and Practice*, chapters 8–9 and 11 | Synchronizing interactions/classes, problem versus solution space, pre-CDR cleanup, responsibility candidates and later model updates. | Upstream research; historical extraction locators include 4035–4058, 4270–4365 and 4521–4963. No new full-book comparison in this revision. |
| Fowler (2004), *UML Distilled* (3rd ed.), chapters 1, 3 and 5 | Software/conceptual perspectives, properties, operations, associations, composition, generalization and detail limits. | Upstream research. The extraction had OCR damage; this revision does not retain normalized quotations or certify the whole extraction. |
| Rosenberg, Stephens & Collins-Cope (2005), *Agile Development with ICONIX Process: People, Process, and Pragmatism* | Model refactoring, domain/static separation, architectural detail and model/code synchronization. | Upstream research; historical extraction locators 1755–1817, 1902–1948, 2128–2145 and 3508–4189. |
| Wiegers & Beatty (2013), *Software Requirements* (3rd ed.) | Analysis/design handoff and traceability context. | Limited upstream contribution; no detailed-class-model checklist or operation-allocation method attributed to it. |

Corpus line numbers locate the original author's extraction and cannot be resolved from this package. Use the edition and chapter for source consultation; do not portray a private locator as a public citation. Fowler's third edition uses conceptual/software perspectives rather than the older three-perspective split.

## Historical standards framing

The upstream record reports primary-text checks of ISO/IEC/IEEE 12207:2017 §6.4.5 (design definition/traceability), §6.4.9 (verification) and §6.3.6 (information management). Annex F.2.2 discusses a static model, but **Annex F is informative** and belongs to architecture definition. Applying that description to a detailed design class model is this method's synthesis, not a direct mandated notation.

No UML class-diagram requirement was established from the ISO corpus. Process expectations can inform review while the selected UML specification defines notation/semantics. This revision does not newly verify the complete ISO texts.

## Current limited UML verification — 2026-10-29

The earlier upstream attempt recorded that the UML 2.5.1 URL was located but its text could not be extracted. That remains a historical result, not the current status of the clauses used here.

For this remediation, the PDF was downloaded directly from [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF), file ID `formal/17-12-05`, and the following primary-text portions were inspected:

| Clause | Scope checked | Relevant instruction |
|---|---|---|
| §9.5.3, printed pp.111–112 | Property derivation; shared/composite aggregation; at most one composite at a time; deletion of attached parts and permitted prior detachment; intentionally unspecified lifecycle details. | `notation-rules.md`: derivability does not select storage/caching; composition does not imply immutable lifetime ownership. |
| §9.9.17, Property | `isDerived` and Property metamodel description. | `notation-rules.md`: preserve derived-property meaning. |
| §17.4.3, printed pp.574–575; §17.12.18, Message | Operation calls, synchronous replies, Signal signatures and message arguments. | `provenance-rules.md`: classify message semantics before deriving receiving-class operations. |

PDF SHA-256: `416b57e1933780eb48bd60fe513e031da220c28a521bdd334a366bebc78a463e`. The source PDF/extracted text were inspected in temporary files and are not added to the package. This check establishes only the stated semantics; it is not a complete UML audit or a redistribution license for its text.

## Research and local conventions

CK metrics (Chidamber & Kemerer, 1994), Genero/Piattini maintainability research and model-smell literature supply inherited secondary context. The historical attempt did not reverify the Torre, Labiche & Genero EASE 2014 class/sequence figure. Keep those limits rather than implying current primary verification.

Class-only inputs do not supply complete method complexity, dynamic response sets or every cohesion variant. Describe actual structural proxies instead of claiming all CK metrics are computed. Numeric size/coupling/readability thresholds are local warning conventions, not standards or empirical acceptance limits.
