<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sources and methods

Methodological basis for this skill's rules and audit gate. Cite concisely when the user requests methodological or academic justification. The corpus and verification statements below describe the **upstream author's source review**; the source books and standards are not bundled with this translation, and those checks were not repeated here.

## Method sources: books

- **Rosenberg, D., & Stephens, M. (2007). *Use Case Driven Object Modeling with UML: Theory and Practice*. Apress.** **Primary source.** The robustness-analysis chapter supplies almost all directly applicable evidence: the use case's “object picture,” three stereotypes, permitted/prohibited connections, robustness and PDR guidelines, six steps toward better preliminary design, Highlighter Technique, object discovery, and worked-exercise anti-patterns.
- **Rosenberg, D., Stephens, M., & Collins-Cope, M. (2005). *Agile Development [abbreviated title]*. Apress.** Process context and supporting rationale: transitional artifacts, noun-to-noun connections as missing functions, omission of behaviorless controls, rogue controls, keeping GUI concepts outside the domain model, and BCE ↔ MVC mapping.
- **Wiegers, K., & Beatty, J. (2013). *Software Requirements* (3rd ed.). Microsoft Press.** Visual models expose incorrect, inconsistent, missing, and superfluous requirements; tool-based modeling-rule validation helps find syntax errors and inconsistencies missed by reviewers. Dialog maps relate to boundaries; state transition diagrams help when several use cases change one entity's state. **Terminology warning:** “robustness” in this source is a system quality attribute, not this diagram type.
- **Fowler, M. (2004). *UML Distilled* (3rd ed.). Addison-Wesley.** The upstream review found no robustness-analysis or BCE discussion and attributes no robustness-specific rules to it. Relevant contributions are the conceptual perspective separating analysis from detailed design; UML 2 stereotypes being formally defined through profiles, making BCE icons a method convention rather than universal UML notation; and communication diagrams, formerly collaboration diagrams, emphasizing links and alternative exploration.

## Applicable standards framework

The corpus standards do **not directly define a robustness diagram**. Their contribution is at **process level**; this skill explicitly maps those process expectations to the artifact.

### Selected standards

| Standard | Contribution | Application |
|---|---|---|
| **ISO/IEC/IEEE 12207:2017** | Design Definition (§6.4.5) iterates with requirements and architecture definition; design/requirement/entity traceability (§6.4.5.2 h, §6.4.5.3 d) and bidirectional verification links; inspection-based verification (§6.4.9); seven information quality criteria (§6.3.6) | Gate layers 5–6 and artifact context |
| **ISO/IEC/IEEE 90003:2018** | §8.3.4 design review/verification, including inspections and walkthroughs; §8.3.4.2 verified outputs before acceptance/use; §8.3.5 inputs correctly reflected in outputs | Overall audit gate and layer 7 |
| **ISO/IEC 25040:2011** | Design diagrams are evaluable intermediate products. Evaluation proceeds through requirements, measures/decision criteria, evaluation design, and execution | Gate structure |
| **ISO/IEC/IEEE 16326:2019** | Artifact as a managed information item, with template, author, reviewer, and information-quality expectations | Audit certificate and layer 6 |

### Excluded standards and reasons

Adding inapplicable standards weakens rather than strengthens the rationale.

- **ISO/IEC/IEEE 15939 and GQM:** measurement processes, without a prescribed concrete measure set; relevant to a process metrics program rather than diagram correctness.
- **ISO/IEC 25010 / 25022 / 25023 / 25020 and BS ISO/IEC 25024:** runtime software or data quality rather than this analysis artifact. 25010 may supply vocabulary when tracing nonfunctional requirements.
- **ISO/IEC 25030-2:** secondary relevance only when tracing quality requirements to components.
- **PMBOK 7:** project management.
- **ISO 9001:2015:** covered here through 90003, which adds software-specific interpretation.
- **Course notes on quality models:** pedagogical material, not normative evidence.

### Source availability qualification

**ISO/IEC/IEEE 15289 was absent from the original corpus** and appeared only through citations in other standards. No direct clauses are attributed to it. Content and consistency criteria are supported through 12207 §6.3.6 and 16326 instead.

### Upstream clause-verification record

| Citation | Recorded status |
|---|---|
| **12207 §6.4.5**, Design Definition process | **VERIFIED** against `libros_y_normas_markdown/ISO_IEC_12207_2017_en.md`, line 2863 in the upstream author's corpus |
| **12207 §6.4.5.2 h)** | **VERIFIED:** traceability between design characteristics and architectural entities |
| **12207 §6.4.5.3**, task 2) | **VERIFIED:** detailed design element traceability to system/software requirements and architectural entities |
| **12207 §6.4.9**, Verification process | **VERIFIED**, source line 3239 |
| **12207 §6.3.6**, Information Management process | **VERIFIED:** explicitly gives unambiguous, complete, verifiable, consistent, modifiable, traceable, and presentable information criteria |
| **90003 §8.3.4 / §8.3.4.2 / §8.3.5**, **25040:2011**, **16326:2019** | **NOT VERIFIED at clause level.** Documents were present in the upstream corpus (`90003_2018.md`, `ISO_IEC_25040_1_2011_…md`, `ISO_IEC_IEEE_16326_2019.md`); verification was pending, not impossible |

**15289 qualification:** a note in 12207 §6.3.6.3 points to 15289 for life-cycle information item content requirements. Although 15289 was absent from the corpus, 12207 §6.3.6 itself supports the criteria used here.

**Recorded correction:** an earlier upstream version incorrectly marked the 12207 clauses as secondary and claimed primary text was absent. The file `ISO_IEC_12207_2017_en.md` had actually been available throughout. The author had generalized a failed web/paywall search without checking the repository. The correction is retained because unjustified uncertainty is also inaccurate evidence reporting.

## Combining method and standards

MKL provides **what to draw and which modeling rules apply**. The selected standards provide **verification expectations and deliverable quality criteria**. Layers 1–4 apply method checks; layers 5–7 apply process and information-quality criteria. The audit certificate makes the recorded evidence inspectable rather than relying on an unsupported compliance claim.
