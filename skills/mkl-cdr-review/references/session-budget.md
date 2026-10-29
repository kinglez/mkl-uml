<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Estimating formal review effort

Use a budget when the selected package or a requested formal review needs scheduling. Routine scoped checks need only an honest coverage statement. Estimates support planning; they do not prove that a review was effective.

## Measure and estimate

1. Record material by type: detailed diagrams, specifications, test design and any authorized generated headers.
2. State the unit. If converting PlantUML to equivalent pages, the historical **40 effective lines per page** is a local convention; exclude blank/comment lines and report actual counts too.
3. Apply an explicit project rate and show the resulting effort range. Historical upstream notes attribute **3–4 pages/hour** for detailed design and **5–7 pages/hour** for test plans to IEEE Std 1028-2008 §6.5.2. These are planning guidance inherited from the inspection clause, not mandatory CDR limits or a newly reverified transcription.
4. Estimate header inspection separately. The inherited source-code row mixed page/hour and line/hour units; that unresolved transcription must not become a conversion rule. Use a declared project assumption until the official table is checked.
5. Split large packages into coherent use-case groups and reserve actual preparation and follow-up time. Document any material that could not be examined.

Wiegers & Beatty, *Software Requirements* (3rd ed.), chapter 17 informs advance preparation, bounded meetings and avoiding fatigued repeat reviews. Its requirements-review rates do not become measured design-review rates by analogy.

## Historical empirical context

Van Solingen & Berghout, *The Goal Question Metric Method*, Case B (RITME review/inspection measurement) is the upstream source for observed review-volume and speed effects. The upstream record reports roughly **0.4 faults/page** for one project's design documents and reduced review yield on larger/faster-reviewed material. These observations justify considering package size and preparation; they do not establish universal defect density, duration or causal guarantees.

Historical suggestions to split around **20 equivalent pages** or flag very large packages around **50** are local planning prompts when transferred to PlantUML. Discuss actual complexity and reviewer capacity rather than treating these numbers as acceptance limits. The corpus provides no universal total CDR duration or validated diagram/page conversion.

## Assess coverage directly

Zero findings is a valid result at any package size. Confirm that selected artifacts were examined, applicable checks have evidence, and seeded negative cases show the automated checks can detect their intended defects. A clean positive fixture alone cannot demonstrate active checking.

The former density trigger below 0.1 findings/page on packages above 10 equivalent pages is not an acceptance criterion or a compulsory warning. Finding density alone cannot distinguish mature material from missed examination. Record an actual coverage concern only when evidence supports it; do not invent findings or repeat unchanged self-reviews to meet an expected rate.

IEEE 1028 §6.9 informs review-process learning. In a formal record, compare actual preparation, effort and outcomes over time, improve misleading checklist items, and state sampling/coverage limits. A single project's historical density is insufficient for a confidence claim about a new review.
