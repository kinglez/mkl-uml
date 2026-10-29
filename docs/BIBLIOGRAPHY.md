<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Consolidated bibliography

This deduplicated index collects sources cited across the eight skills. Each skill's `references/sources-and-methods.md` or equivalent records the detailed contribution of each source, unsuccessful searches, and clauses checked against primary text. This index does not replace those records. [THIRD_PARTY_SOURCES.md](THIRD_PARTY_SOURCES.md) inventories content treatment and remaining rights/provenance uncertainty; source citation is not redistribution permission.

All citations in code and `SKILL.md` follow the same discipline: **concise attribution identifying the author, work, and chapter or clause; no extensive reproduction**.

## Books

- Rosenberg, D., & Stephens, M. (2007). *Use Case Driven Object Modeling with UML: Theory and Practice*. Apress. [Publisher/DOI](https://doi.org/10.1007/978-1-4302-0369-8). Primary method source for this MKL adaptation supporting robustness analysis, use case specifications, PDR, sequence diagrams, design class models, and CDR.
- Rosenberg, D., Stephens, M., & Collins-Cope, M. (2005). *Agile Development with ICONIX Process: People, Process, and Pragmatism*. Apress. [Publisher/DOI](https://doi.org/10.1007/978-1-4302-0009-3), ISBN 978-1-59059-464-3. Process context, milestones, agile and low-ceremony variants, and the Boundary-Control-Entity ↔ Model-View-Controller mapping.
- Fowler, M. (2004). *UML Distilled* (3rd ed.). Addison-Wesley. UML notation and diagram quality, particularly sequence diagrams and design class models. The skill source records explicitly identify no contribution to robustness analysis or PDR.
- Wiegers, K., & Beatty, J. (2013). *Software Requirements* (3rd ed.). Microsoft Press. Review roles, stages, entry and exit criteria, use case specifications, and requirements quality terminology.
- Cockburn, A. *Writing Effective Use Cases*. Addison-Wesley. Goal levels—user goal (sea), subfunction (fish), and summary (kite)—as a guide to use case granularity.
- Wirfs-Brock, R. (2004). *A Brief Tour of Responsibility-Driven Design*. Six role stereotypes and responsibility assignment guidance used in design class modeling and CDR.
- van Solingen, R., & Berghout, E. *The Goal Question Metric Method* (Case B). The RITME project provides the measured review evidence used in these skills to calibrate CDR session budgets.
- Ebert, C., & Dumke, R. *Software Measurement*. The 5/20/80 triage approach and CK metric definitions used in CDR.
- Giraldo, G. L. *Análisis, Diseño y Construcción de Productos de Software* [Analysis, Design, and Construction of Software Products], university software engineering course materials. Establishes the upstream Spanish terminology, including Critical Design Review and the Highlighter Technique, and contributes worked exercises and checks not found in the English-language books. The Spanish title is retained for source identification.

## Standards and specifications

These are the editions cited by the source package, not a claim that each is the latest edition.

- ISO/IEC/IEEE 12207:2017 — *Systems and software engineering — Software life cycle processes*.
- ISO/IEC/IEEE 90003:2018 — *Software engineering — Guidelines for the application of ISO 9001:2015 to computer software*.
- ISO/IEC 25040:2011 — *Systems and software Quality Requirements and Evaluation (SQuaRE) — Evaluation process*.
- ISO/IEC/IEEE 16326:2019 — *Systems and software engineering — Life cycle processes — Project management*.
- ISO/IEC 25010 — *Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models*.
- ISO/IEC 25023:2016 — *Measurement of system and software product quality*.
- ISO/IEC/IEEE 15939:2017 — *Systems and software engineering — Measurement process*.
- IEEE Std 1028-2008 — *IEEE Standard for Software Reviews and Audits*. Source for review roles, records and criteria. The local three-state verdict scale is explicitly borrowed from the inspection clause; fixed four-way menus and repeated self-audit cycles are MKL choices, not mandated by the standard.
- IEEE Std 1016-2009 — *IEEE Standard for Information Technology—Systems Design—Software Design Descriptions*.
- ISO/IEC/IEEE 29148:2018 — *Systems and software engineering — Life cycle processes — Requirements engineering*.
- ISO/IEC/IEEE 15289 — *Systems and software engineering — Content of life-cycle information items*. Most skills cite its purpose rather than a verified clause.
- ISO/IEC/IEEE 42010 — *Systems and software engineering — Architecture description*. Separation of viewpoints.
- ISO/IEC/IEEE 29119 — *Software and systems engineering — Software testing*.
- OMG UML 2.5 / 2.5.1 (`formal/2015-03-01`, `formal/17-12-05`). [UML 2.5.1 specification](https://www.omg.org/spec/UML/2.5.1/PDF). Normative semantics: Property §9.5.3, Messages §17.4.3, Actors §18.1.3.1.

## Empirical research

- Torre, D., Labiche, Y., & Genero, M. (2014). *UML Consistency Rules: A Systematic Mapping Study*. EASE 2014.
- Torre, D., Labiche, Y., Genero, M., et al. (2020). FormaliSE 2020. Class–sequence consistency rule enumeration.
- Torre, D., Labiche, Y., Genero, M., & Elaasar, M. (2018). *Journal of Systems and Software*, 144.
- Egyed, A. (2006). *Instant Consistency Checking for the UML*. ICSE 2006.
- Sabaliauskaite, G., Matsukawa, F., Kusumoto, S., & Inoue, K. (2002). ISESE 2002. Checklist-based versus perspective-based reading in UML design inspections.
- Shull, F., Carver, J., Vegas, S., & Basili, V. (2006). *What Do We Know about Defect Detection Methods?* IEEE Software.
- Russell, G. W. (1991). *Experience with Inspection in Ultralarge-Scale Developments*. IEEE Software, January 1991, pp. 25–31.
- Chidamber, S. R., & Kemerer, C. F. (1994). *A Metrics Suite for Object Oriented Design*. IEEE Transactions on Software Engineering, 20(6).
- Genero, M., & Piattini, M. Research on predicting class diagram maintainability from early structural measures.
- Lieberherr, K., & Holland, I. (1989). *Assuring Good Style for Object-Oriented Programs*. IEEE Software, 6(5). Law of Demeter.

## Verification status

Each skill's source record explicitly distinguishes citations checked against primary text from secondary citations reproduced through another source. It also records corrections to earlier verification errors. This distinction is deliberate and follows the repository's evidence discipline. Consult the individual skill's source record for the detailed verification status; this translation does not assert that those checks were repeated.

## Editorial and content policy

MKL names the adapted skill suite; it does not rename the original publications. Cite published titles for identification. The 2026-10-29 remediation replaces unnecessary book, standard and course transcriptions with independently worded operational guidance. Short technical terms and original local examples remain. This does not relicense external publications or establish permissions for old releases.

The publisher DOI links identify the two principal books. The 2005 book title/authors were checked against the [publisher record](https://link.springer.com/book/10.1007/978-1-4302-0009-3) on 2026-10-29. Historical private-corpus line numbers remain provenance notes, not independently resolvable public citations. The design source record separately identifies the limited 2026-10-29 primary UML check; no full re-verification of every inherited source claim is implied.
