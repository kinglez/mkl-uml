<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Third-party sources and content inventory

Inventory date: **2026-10-29**. Baseline: commit `f6f21221ef950371700e0db5860f3e94e077bc07`. This record separates the upstream software license from external publication provenance. It documents content remediation and remaining uncertainty; it does not assert legal clearance or permission that has not been established.

## Distributed source classes

| Class / sources | Where used | Treatment and evidence boundary |
|---|---|---|
| Upstream software, instructions and fixtures by Jonatan Estiven Sánchez Vargas | Eight skills, scripts and inherited examples; root and skill `LICENSE`/`NOTICE` files. | Apache-2.0 notices and upstream snapshot attribution retained. This inventory does not replace those files or extend that grant to third-party publications. |
| Rosenberg & Stephens (2007), *Use Case Driven Object Modeling with UML: Theory and Practice* | Robustness/PDR, sequence/design and CDR guidance; historical figure/source records. | Book sentences, repeated numbered checklists and diagram-Note quotations were replaced with independently worded operational checks. Author, work, edition/year, chapters and historical extraction locators remain. Source pages/artwork are not bundled. |
| Rosenberg, Stephens & Collins-Cope (2005), *Agile Development with ICONIX Process: People, Process, and Pragmatism* | Workflow, model refactoring, BCE/MVC and test design context. | Verbatim sentences removed in favor of local procedures; full bibliographic title and publisher DOI retained. |
| Fowler (2004), *UML Distilled* (3rd ed.) | Perspectives, class/sequence notation and responsibility/readability guidance. | Source sentences and normalized OCR quotations replaced with original instructions. Historical OCR limitations retained without distributing a corrected text extract. |
| Wiegers & Beatty (2013), *Software Requirements* (3rd ed.); Cockburn, *Writing Effective Use Cases* | Specification structure, goal levels, reviews and traceability. | Review-role/stage/rate sentences replaced with original guidance. Concise technical vocabulary, bibliographic titles and original local templates/examples remain. Empirical observations are contextual, not guarantees. |
| van Solingen & Berghout, *The Goal Question Metric Method*, Case B; Ebert & Dumke, *Software Measurement* | Review planning, RITME observations, triage and metrics. | Long source transcriptions and tables of quoted definitions removed. Limited attributed factual context remains; thresholds/transfers to this tool are local heuristics. No expected defect quota. |
| IEEE Std 1028-2008 and IEEE Std 1016-2009 | Formal review process/records and design-description context. | Long clause extracts, verbatim role tables, severity definitions and copied disposition text removed. Clause locators and short technical category/status terms remain, with local wording and declared adaptations. Current full primary-text verification was not performed. |
| ISO/IEC/IEEE 12207:2017, 90003:2018, 16326:2019, 15939:2017, 29148:2018; ISO/IEC 25040:2011, 25010, 25023:2016; purpose-only references to 15289, 42010 and 29119 | Source/method records, requirements/design/review quality context. | Standard definitions and clause sentences used as quotations were replaced with operational guidance or concise summaries. Editions/clauses and inherited verified/secondary/unverified distinctions remain. Informative annexes and local synthesis are identified. |
| OMG UML 2.5 / 2.5.1 | UML Property, composition, Message and actor semantics. | Clause links and independently written semantic guidance remain; no PDF, XMI, copied table or source artwork is distributed. Limited 2.5.1 checks are recorded in the design/sequence source records. Public availability alone is not redistribution permission. |
| Gloria L. Giraldo, *Análisis, Diseño y Construcción de Productos de Software*, including robustness/sequence chapters and Session 09 | Historical Spanish terminology, style defaults, worked exercises and review prompts. | Translated/quoted course passages replaced with independently worded instructions. Exact private PDF edition/date and redistribution permission are unavailable in repository records. Course figures are not bundled; remaining historical figure descriptions are paraphrased provenance notes. |
| Research papers/presentations: Torre et al., Egyed, Sabaliauskaite et al., Shull et al., Russell, Chidamber/Kemerer, Genero/Piattini, Lieberherr/Holland and Wirfs-Brock | Consistency research, inspection/metrics/responsibility context. | Bibliographic metadata, technical terms and attributed summaries remain. Upstream primary/secondary distinctions are retained; no paper pages or long quotations are distributed. Incomplete bibliographic metadata remains explicitly limited to the known record. |
| Indirect references: Larman/GRASP, Wirfs-Brock & McKean, Booch/Halbert/O'Brien, Rosenberg & Scott, SEI reports, Grady/AT&T, Gilb/Graham/Humphrey and Fagan | Historical source chains and terminology. | Keep attribution as indirect context; no claim that this revision read the original works. Do not promote an indirect citation into a verified clause or reproduce unavailable source text. |
| Context-only/excluded identifiers: ISO 9001:2015, ISO/IEC 25020/25022/25024/25030-2, PMBOK 7 and related course quality notes | Exclusion/history portions of source records. | Mentioned to explain scope; no grant, substantive source excerpt or conformance claim inferred. |
| Contributor Covenant 2.1 | Condensed community-conduct wording in root and skill notices. | Existing source attribution and adaptation notice retained. It is distinct from software Apache attribution; see the source link in `NOTICE`. No source text was removed from `LICENSE` or `NOTICE` during this remediation. |
| Eight SVG skill icons and local PlantUML/Markdown examples | `skills/*/assets/icon.svg` and fixture directories. | Existing repository-authored/adapted artifacts retained with repository notices; no bundled third-party PDF, photograph, screenshot, font or extracted book image was found in this tracked asset set. This is a file inventory, not independent certification of every asset's ownership. |

See [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md) for the source index. Historical corpus locators identify a private extraction and are not publicly resolvable citations or proof of permission.

## Quotation-marker baseline and remediation

A reproducible baseline count selected lines beginning with Markdown `>` in skill references and counted words with `\b[\w'-]+\b` after removing the marker. It found **22 files / 4,443 words**. This includes original scope banners, local rules and prompt examples, so it is **not** a rights-holder-specific quotation total, a legal threshold or an infringement determination. Inline book/standard/course sentences and copied lists were reviewed separately and remediated as well.

The baseline spans below refer to the pinned commit, not current line numbers. No source passages are reproduced in this inventory.

| Baseline reference (`skills/`) | Blockquote words | Baseline quoted-line span(s) | Content/treatment |
|---|---:|---|---|
| `mkl-cdr-review/references/cdr-rules.md` | 942 | 16, 20, 26, 36–37, 52, 56, 71, 75, 88, 92, 96–97, 101, 114, 118–120, 143, 147, 160, 177, 181, 193, 210, 214, 226, 230, 248, 252, 262, 268, 278, 290 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-cdr-review/references/deliberation-protocol.md` | 93 | 14, 18, 22, 28 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-cdr-review/references/figure-notes.md` | 11 | 31 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-cdr-review/references/metrics-and-triage.md` | 300 | 4, 16, 20, 67–68, 84, 106–107 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-cdr-review/references/review-protocol.md` | 1111 | 4, 18, 24, 56, 73, 81, 87, 97, 118, 128, 146, 170, 189–192, 210, 240, 244 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-cdr-review/references/session-budget.md` | 139 | 4, 16, 29 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-cdr-review/references/sources-and-methods.md` | 28 | 4 | Original historical-status banner; replaced by explicit evidence record. |
| `mkl-cdr-review/references/traceability-and-headers.md` | 55 | 10, 78–79 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-pdr-review/references/pdr-guidelines.md` | 200 | 12, 33, 45, 57, 73, 83, 97, 111, 125, 137 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-pdr-review/references/pdr-metrics.md` | 104 | 4 | Original operational-scope banner retained/updated; disposition contradiction corrected. |
| `mkl-pdr-review/references/review-protocol.md` | 104 | 4 | Original scope banner; reference rewritten as concise procedure. |
| `mkl-pdr-review/references/sources-and-methods.md` | 28 | 4 | Original historical-status banner retained; inline book wording replaced. |
| `mkl-uml-design-class-model/references/notation-rules.md` | 160 | 25, 27, 39, 81, 105, 127, 129, 131, 133, 137 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-uml-design-class-model/references/provenance-rules.md` | 180 | 12, 16, 59, 65 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-uml-design-class-model/references/sources-and-methods.md` | 34 | 73 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-uml-design-class-model/references/static-model-guidelines.md` | 234 | 12, 16, 20, 34, 44, 63, 67, 83, 117 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-uml-robustness-diagram/references/audit-gate.md` | 104 | 4 | Original operational-scope banner retained/updated. |
| `mkl-uml-sequence-diagram/references/behavior-allocation.md` | 102 | 12–13, 21, 31, 50, 91, 93 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-uml-sequence-diagram/references/notation-rules.md` | 19 | 78 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-uml-sequence-diagram/references/sequence-guidelines.md` | 338 | 14, 22, 28, 34, 40, 46, 52, 58, 64, 70, 80, 113–115, 131, 133 | Source quotations replaced with independent operational wording; attribution retained. |
| `mkl-uml-sequence-diagram/references/test-derivation.md` | 90 | 14, 16, 18, 28 | Source sentences replaced; local flow-coverage rule retained in original operational wording. |
| `mkl-use-case-specifier/references/minimal-examples.md` | 67 | 8, 23, 37 | Original illustrative prompts retained; not publication quotations. |

Inline-text remediation also covers the CDR/design/sequence anti-pattern catalogs, design source table, use-case standards-alignment practitioner list, domain-rubric data-model quotation, and PDR source-record sentences. Short work/section titles, identifiers, category names and original example utterances remain where needed for identification or instruction. Retaining a term does not imply an external endorsement.

## Remaining uncertainty and maintenance

This revision removes unnecessary external expression instead of relying on an undocumented quotation allowance. It retains source-informed methods, original operational wording, attribution, factual summaries, technical terms and some historical paraphrased figure descriptions. There is no repository evidence of individualized permission for the removed book, IEEE/ISO or private-course excerpts. Their removal does not establish permission for old releases, authorize reintroduction, or complete legal clearance of every adaptation or asset.

If distribution requires a legal rights conclusion, the remaining source-inspired adaptations, course provenance, source-dependent figure descriptions and inherited asset authorship need assessment under the actual distribution terms/jurisdictions. No ownership or legal-exception conclusion is inferred from a word count, an Apache notice or a source being publicly readable.

Keep `LICENSE`/`NOTICE` attribution and any source-specific conditions with distributed artifacts. Before adding source expression or artwork, record its exact location, rights holder, applicable grant/basis and required notices. When only an operational principle is needed, write a concise task-specific instruction and cite the source rather than reconstructing its prose/table.
