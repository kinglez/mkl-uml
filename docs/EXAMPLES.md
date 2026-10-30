<!-- Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Tutorial: design an order-pricing feature

Use the eight MKL skills to take **CU-01 Quote cart** from requirements to a reviewed design. Every step uses the same order-pricing scenario and links to a completed artifact you can compare with your result.

If you only want to read or run the finished example, start with the [example guide](../examples/order-pricing/README.md). This tutorial is for generating your own version alongside it. See the [documentation guide](README.md) for the reading order.

[Setup](#before-you-start) · [Scenario](#the-scenario) · [Eight steps](#1-name-the-business-concepts) · [Verify](#check-your-results) · [Your own project](#apply-this-to-your-project)

## Before you start

1. [Install the skills](INSTALLATION.md) for Codex or Claude Code.
2. Open a checkout of this repository in your agent. The tutorial reads input files from `examples/order-pricing/`; installing the skills alone does not copy those files.
3. Send the prompts below **one at a time in the agent chat**. Review each result before continuing.

If you do not have a checkout yet, run these commands in a terminal:

```bash
git clone https://github.com/kinglez/mkl-uml.git
cd mkl-uml
```

Prompts use Codex's `$skill-name` syntax. In Claude Code, replace it with `/skill-name`, for example `/mkl-uml-domain-modeler`.

**Path convention:** `examples/order-pricing/` is the completed, read-only reference. Your new outputs go under `uml/order-pricing/`, with one numbered folder per stage. Keep those outputs separate so you can compare them with the reference without changing its reviewed baselines. If that output folder already contains work, select another new folder and replace the prefix consistently in every prompt.

At each step, ask the agent to run the applicable bundled validator and report the command, result and missing checks. PlantUML source (`.puml`) is editable text; the reference includes PNG/SVG previews. Rendering your new diagrams additionally needs a renderer available to your agent.

## The scenario

A Shopper asks for a cart's item price, optionally using one Coupon. Product prices come from a trusted catalog. The system returns a subtotal, discount and payable amount, or a refusal. Quoting changes no cart or Coupon state and creates no Order.

The main cart is two books at CNY 120.00 each and one pen at CNY 15.00: **CNY 255.00** before discounts.

| Request | Expected result |
|---|---|
| No Coupon | Payable CNY 255.00 |
| SAVE30, a CNY 30.00 discount when subtotal is at least CNY 200.00 | Payable CNY 225.00 |
| TENOFF, a 10% discount when subtotal is at least CNY 100.00 | Payable CNY 229.50 |
| BIGSAVE, a CNY 500.00 discount capped at the subtotal | Payable CNY 0.00 |
| Unknown or expired Coupon, or an unmet minimum | Explicit refusal; no successful quote |

Use the full [requirements](../examples/order-pricing/00-input/requirements.md) and [independent expected results](../examples/order-pricing/00-input/ACCEPTANCE_ORACLE.md) for the remaining cases, including invalid inputs, exact expiry and rounding. Amounts are integer cents: `25500` means CNY 255.00. The expected results were derived from the requirements independently of the reference implementation.

The IDs let you follow the same item across files: RF = functional requirement, RN = business rule, RNF = quality/design constraint, CU = use case, FA/FE = its alternative/exception flows, DR = robustness diagram, DS = sequence diagram, MC = design class model, and CP = test case. Keep an existing ID when its title or diagram position changes.

<a id="1-domain-model"></a>

## 1. Name the business concepts

**Purpose:** agree on the meaning of Cart, Product and Coupon before choosing implementation classes.

**Input:** the supplied requirements and expected results. **Output:** `01-domain/domain.puml` and `01-domain/glossary.md` under your output folder.

```text
$mkl-uml-domain-modeler
Read examples/order-pricing/00-input/requirements.md and ACCEPTANCE_ORACLE.md
in that same directory. Work only under uml/order-pricing; keep reference
files unchanged. Create 01-domain/domain.puml and 01-domain/glossary.md there
for CU-01 Quote cart. Model business concepts, relationships and value
constraints. Distinguish them from software classes, record unresolved policy,
and run the applicable checks.
```

**Check before continuing:** the model explains Cart, CartLine, Product, Coupon and PriceQuote. Product prices are authoritative catalog values; a discount algorithm is not automatically a domain entity.

Compare: [domain preview](../examples/order-pricing/01-domain/domain.png) · [domain source](../examples/order-pricing/01-domain/domain.puml) · [glossary](../examples/order-pricing/01-domain/glossary.md).

<a id="2-use-case-diagram"></a>

## 2. Identify the user goal

**Purpose:** show who uses the system and what result they want.

**Input:** requirements and domain model. **Output:** `02-use-cases/use-cases.puml`.

```text
$mkl-uml-use-case-diagram
Read examples/order-pricing/00-input/requirements.md and the generated
01-domain files under uml/order-pricing. Create
uml/order-pricing/02-use-cases/use-cases.puml with the Order Pricing boundary,
Shopper actor and CU-01 Quote cart. Keep price lookup and discount calculation
inside that goal. Use only participating actors justified by the requirements;
the trusted internal demo catalog is not an external actor. Run the checks.
```

**Check before continuing:** the diagram shows a Shopper asking for a quote. It does not introduce checkout, payment or order creation as part of CU-01.

Compare: [use case preview](../examples/order-pricing/02-use-cases/use-cases.png) · [source](../examples/order-pricing/02-use-cases/use-cases.puml).

<a id="3-use-case-specification"></a>

## 3. Specify success and refusal behavior

**Purpose:** describe what happens, including paths a happy-path diagram can miss.

**Input:** requirements, domain model, user goal and expected results. **Output:** `03-spec/CU01-quote-cart.md` and `03-spec/interface-contract.md`.

```text
$mkl-use-case-specifier
Read the requirements and ACCEPTANCE_ORACLE.md in examples/order-pricing/00-input,
and the generated 01-domain and 02-use-cases files under uml/order-pricing.
Use examples/order-pricing/03-spec/CU01-quote-cart.md as a read-only behavior
and ID reference. Under uml/order-pricing, write 03-spec/CU01-quote-cart.md
and 03-spec/interface-contract.md. Preserve CU-01 and its FA/FE/RN/CA IDs. Cover the
no-Coupon basic flow, fixed/percentage/zero-subtotal alternatives and every
specified refusal. State triggers, system actions, return/termination points
and expected results. Retain trusted prices, integer cents and read-only
behavior. Run the specification checks.
```

**Check before continuing:** invalid data is handled by a stated refusal path, rather than hidden in a precondition. A zero-priced nonempty cart is valid; a Coupon's unmet minimum still refuses it. Do not invent a rule for an unresolved policy.

Compare: [CU-01 specification](../examples/order-pricing/03-spec/CU01-quote-cart.md) · [interface contract](../examples/order-pricing/03-spec/interface-contract.md).

<a id="4-robustness-analysis"></a>

## 4. Connect behavior to responsibilities

**Purpose:** discover the interaction interface, analysis responsibilities and domain information needed for each flow.

**Input:** specification, domain model and interface contract. **Output:** `04-robustness/robustness.puml` and `04-robustness/correspondence.md`.

```text
$mkl-uml-robustness-diagram
Read the generated 01-domain, 02-use-cases and 03-spec files under
uml/order-pricing. Create DR-01 in
uml/order-pricing/04-robustness/robustness.puml with boundary/control/entity
notation. Map basic steps and every FA/FE to responsibilities and data origins
in correspondence.md in that same folder. Identify any missing domain concept
before adding it. Run the applicable checks.
```

**Check before continuing:** each success and refusal path has actual system behavior. A boundary is an interaction interface, a control is an analysis responsibility, and an entity represents domain information. These are not yet a list of production services.

Compare: [robustness preview](../examples/order-pricing/04-robustness/robustness.png) · [source](../examples/order-pricing/04-robustness/robustness.puml) · [correspondence](../examples/order-pricing/04-robustness/correspondence.md).

<a id="5-pdr-preparation"></a>

## 5. Review the analysis: PDR

**PDR means Preliminary Design Review.** It asks whether the preceding analysis is consistent enough to support detailed design.

**Input:** the outputs of steps 1–4 and source expectations. **Output:** `05-pdr/PDR-01.md`, including the handoff to step 6.

```text
$mkl-pdr-review
Review the generated 01-domain through 04-robustness artifacts under
uml/order-pricing against examples/order-pricing/00-input/requirements.md
and ACCEPTANCE_ORACLE.md in that same input directory. Save a scoped PDR
preparation review to uml/order-pricing/05-pdr/PDR-01.md. Record located
findings, actual checks and missing evidence. Correct affected working files
and recheck them. End with CU-01/DR-01 scope, reviewed source versions,
open/closed/deferred actions, correction evidence, remaining constraints and
the technical basis for proceeding. Record only actual reviewer participation.
```

**Check before continuing:** resolve findings that would change detailed design. A “closed” label needs correction evidence. Formal human/business acceptance stays **Not fully verified** when that participation and decision evidence are absent.

Compare: [PDR findings and handoff](../examples/order-pricing/05-pdr/PDR-01.md). The reference PDR caught an invented negative-minimum business rule; the requirements had not authorized that rule.

<a id="6-sequence-diagram-and-tests"></a>

## 6. Allocate calls and derive tests

**Purpose:** decide how participants collaborate and what observable tests that behavior needs.

**Input:** the PDR handoff and the reviewed analysis. **Output:** `06-interactions/sequence.puml`, `operation-delta.md`, `test-plan.md` and `DESIGN_DECISIONS.md` in that folder.

```text
$mkl-uml-sequence-diagram
First read uml/order-pricing/05-pdr/PDR-01.md. Match its CU-01/DR-01 scope
and reviewed versions to current working files; recheck changed inputs or
blocking findings before relying on that handoff. Read requirements.md and
ACCEPTANCE_ORACLE.md in examples/order-pricing/00-input, plus the generated
01-domain, 03-spec and 04-robustness files under uml/order-pricing.
Create DS-01 for CU-01 in uml/order-pricing/06-interactions/sequence.puml,
covering the basic flow and all FA/FE paths. Use explicit guards and terminating
refusals. In that same folder save receiver/operation/source mappings to
operation-delta.md, observable cases to test-plan.md, and rationale plus carried
PDR constraints to DESIGN_DECISIONS.md. Distinguish calls from replies and
lifecycle messages. Run applicable checks against these generated files.
```

**Check before continuing:** every refusal ends without a successful quote; the no-Coupon branch does not require Coupon lookup. Expected test amounts come from the independent input, not the proposed implementation. A test plan describes tests; it is not an executed test result.

Compare: [DS-01 preview](../examples/order-pricing/06-interactions/sequence.png) · [source](../examples/order-pricing/06-interactions/sequence.puml) · [operation allocation](../examples/order-pricing/06-interactions/operation-delta.md) · [test plan](../examples/order-pricing/06-interactions/test-plan.md).

<a id="7-design-class-model"></a>

## 7. Build the design class model

**Purpose:** place typed state, operations and dependencies with justified responsibilities.

**Input:** domain, interactions, operation allocation, contracts and design constraints. **Output:** `07-class-model/classes.puml`, `provenance.md` and `SOLID.md` in that folder.

```text
$mkl-uml-design-class-model
Read examples/order-pricing/00-input/requirements.md and the generated
01-domain, 03-spec and 06-interactions artifacts under uml/order-pricing.
Create MC-01 in
uml/order-pricing/07-class-model/classes.puml with typed state, complete
operation signatures and justified relationships. In provenance.md, trace each
added member or software class to behavior, a contract or a design decision.
In SOLID.md, examine responsibility, discount extension, policy
substitution, client needs and dependency ownership. Separate diagram-supported
claims from claims needing source or execution. Run cross-artifact checks.
```

**Check before continuing:** the discount extension has an explicit reason from RNF-01/RNF-04. Interface notation alone does not establish SOLID. Association multiplicities must match actual ownership and sharing.

Compare: [class preview](../examples/order-pricing/07-class-model/classes.png) · [source](../examples/order-pricing/07-class-model/classes.puml) · [member origins](../examples/order-pricing/07-class-model/provenance.md) · [SOLID evidence](../examples/order-pricing/07-class-model/SOLID.md).

<a id="8-cdr-preparation"></a>

## 8. Review the detailed design: CDR

**CDR means Critical Design Review.** It asks whether the design, behavior and tests agree well enough for the requested implementation handoff.

**Input:** all working analysis/design artifacts and available test evidence. **Output:** `08-cdr/CDR-01.md` with findings, coverage and remaining actions.

```text
$mkl-cdr-review
Review the generated 07-class-model and 06-interactions artifacts under
uml/order-pricing against its 01-domain through 05-pdr artifacts and the source
requirements/expectations in examples/order-pricing/00-input. Include the SOLID
evidence record. Save uml/order-pricing/08-cdr/CDR-01.md. Check flow coverage,
signatures, responsibility allocation and test expectations. Correct affected
working files and recheck them. Record actual checks, located findings,
technical recommendation and missing implementation/execution evidence.
Keep formal acceptance separate; do not call a self-check independent review.
```

**Check before finishing:** the record says which checks ran and what remains unverified. A clean validator result does not establish full business correctness, SOLID conformance or formal approval.

Compare: [CDR record](../examples/order-pricing/08-cdr/CDR-01.md) · [code inspection](../examples/order-pricing/08-cdr/CODE-AUDIT-01.md). The reference adds a small Python implementation and executed tests as further evidence; generating that implementation is a separate task from these eight modeling/review steps.

## Check your results

Ask your agent to review the files in **`uml/order-pricing/`**, run the applicable validators against those files, and compare its actual outcomes with the checkpoints above. Different layouts or class names can be reasonable when their behavior and origins are justified.

To run the **maintained reference implementation**, use a terminal from this repository's root:

```bash
python3 examples/order-pricing/09-reference-implementation/run_example.py
python3 examples/order-pricing/scripts/verify.py
```

These commands require Python 3.9+ and the standard library. The first prints the example quotes/refusals. The second checks the maintained reference's models, reviewed baselines and executable tests; it does **not** verify your new `uml/order-pricing/` outputs. Add `--render` only when local PlantUML is available.

For the reference's additional technical-observation sequence, hash baselines and change/review maintenance, use [HOW_TO_REPLAY.md](../examples/order-pricing/HOW_TO_REPLAY.md). Those publication-maintenance steps are separate from this first-use tutorial.

## Apply this to your project

Replace the source requirements and expected outcomes with your own, choose one output folder, and retain your existing IDs. Run only the stages your task needs; a standalone diagram does not require all eight stages.

For example, after completing step 6 you can request a focused correction:

```text
$mkl-uml-sequence-diagram
Review uml/order-pricing/06-interactions/sequence.puml against
uml/order-pricing/03-spec/CU01-quote-cart.md. Check Coupon guards, refusal
termination and operation calls. Apply justified corrections, preserve
CU/DS/FA/FE IDs, and report checks actually run and gaps.
```

For Chinese explanations, append `Explain the result in Chinese; keep code identifiers unchanged.`
