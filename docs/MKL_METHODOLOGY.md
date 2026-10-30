<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# How the MKL workflow fits together

The workflow connects **requirements → behavior → design → tests**. Each stage answers a new question while checking its result against the preceding work. You can use one skill for one artifact or explicitly ask for the full workflow.

This page explains why the stages exist. To perform them, use the **[order-pricing tutorial](EXAMPLES.md)**. For other documents, see the [reading guide](README.md).

## One problem, eight questions

In the example, a Shopper requests a price quote for a cart with an optional coupon. Two books and a pen cost CNY 255.00; an eligible SAVE30 coupon reduces payable to CNY 225.00. The system creates no Order.

| Stage | Question | What order pricing produces |
|---|---|---|
| 1. Domain model | What do the business words mean? | Cart, CartLine, Product, Coupon and PriceQuote, with relationships and a glossary. |
| 2. Use case diagram | Who wants what from the system? | Shopper asks Order Pricing to perform CU-01 Quote cart. Price lookup is an internal step. |
| 3. Use case specification | What happens for each input and outcome? | Basic behavior, discount alternatives and explicit refusal paths. |
| 4. Robustness analysis | Which interface, responsibilities and domain information realize those steps? | Boundary/control/entity analysis and correspondence to the specified flows. |
| 5. PDR | Does the analysis agree well enough to design from it? | Findings, corrections, reviewed inputs and a detailed-design handoff. |
| 6. Sequence design | Who collaborates, and which operations and tests follow? | Guarded interactions, operation allocation, test plan and design rationale. |
| 7. Class design | Where do typed state, operations and dependencies belong? | Design classes, justified relationships, member origins and scoped SOLID reasoning. |
| 8. CDR | Do the detailed models, contracts and test evidence agree? | Findings, coverage, remaining actions and an implementation-handoff recommendation. |

See the [completed artifacts](../examples/order-pricing/README.md#eight-stage-artifacts) to inspect the files for each row. The reference adds Python code and executed tests after modeling so that readers can challenge the design; generating implementation code is a subsequent task.

## Why the two reviews matter

**PDR — Preliminary Design Review** catches problems in the analysis before they become detailed design. In this example, it caught an invented rule rejecting a negative coupon minimum. The requirements had not defined that policy. The correction removed the invented rule and kept the unresolved question visible.

The PDR record tells the next stage which inputs were reviewed, what was corrected, what remains open and whether those issues affect detailed design. Sequence design reads that record first and rechecks changed inputs or unresolved blockers.

**CDR — Critical Design Review** compares the detailed design with behavior, requirements and tests. The reference reviews caught incorrect sequence termination/frame coverage and a class multiplicity inconsistent with shared immutable CartLine values. These required semantic examination as well as tool execution.

A technical recommendation supports the reviewed scope. Formal acceptance also needs its applicable decision evidence and actual decision maker. In this teaching example, formal human/business acceptance remains **Not fully verified**. A missing formal decision is recorded separately from a useful technical review.

## How the files stay connected

Consider the SAVE30 rule. Its requirement states the minimum and discount. The specification states when that branch applies and what it returns. Robustness identifies the information and responsibilities involved. The sequence allocates calls, the class model defines the required operations, and a test compares the result with the independently expected **22500 cents** payable.

That chain is **traceability**. Explicit links establish it; matching diagram numbers or similar class names alone do not. The [traceability guide](../examples/order-pricing/TRACEABILITY.md) shows the actual links. When a requirement changes, review and update the affected links while preserving unchanged identities.

Domain concepts and implementation classes serve different purposes. Cart and Coupon describe the problem; a discount strategy or catalog adapter needs a design reason. Replies, signals and lifecycle messages also retain their semantics rather than all becoming ordinary class operations.

## Use only the scope you need

For a single diagram, supply the relevant goal, behavior or target artifact. The agent can complete independent work and report which comparisons lack evidence. A full eight-stage run is an explicit request, not a prerequisite for every task.

Automated validators check supported syntax, local rules and selected heuristics. Rendered diagrams, semantic review, source inspection and executed behavioral tests answer different questions. Use the [operating contract](OPERATING_CONTRACT.md) when you need the exact input, coverage and ID rules. For SOLID claims, consult the example's [evidence record](../examples/order-pricing/07-class-model/SOLID.md); passing validators or drawing interfaces does not prove all five principles.

## Method and sources

MKL is this edition's branding for an adapted use-case-driven modeling workflow. Its methodological sources include Rosenberg and Stephens, *Use Case Driven Object Modeling with UML: Theory and Practice* (2007), and related work identified in the [bibliography](BIBLIOGRAPHY.md). Original sources remain attributed to their authors; the [source notes](THIRD_PARTY_SOURCES.md) distinguish verified references from unverified material.
