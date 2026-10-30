# Order pricing: a complete MKL UML example

This example follows one request, **CU-01 Quote cart**, from business rules to UML diagrams, design reviews and runnable Python code. Use it to see what each skill produces and how the outputs connect.

**New to the skills?** Read this guide, run the example, then follow the [eight-stage tutorial](../../docs/EXAMPLES.md) to create your own files. The completed files here are a reference you can compare with your work.

[Business scenario](#business-scenario-and-expected-results) · [Run it](#run-the-example) · [Follow the stages](#eight-stage-artifacts) · [Review findings](#what-the-reviews-actually-caught) · [Further reading](#further-reading)

## Business scenario and expected results

A Shopper asks for the price of a cart, optionally using one Coupon. The system reads trusted catalog prices and returns the subtotal, discount and payable amount, or a refusal with a reason. **A quote does not place an Order or change the cart, catalog or Coupon.**

The main cart contains two books at CNY 120.00 each and one pen at CNY 15.00. Its subtotal is **CNY 255.00**. The code calculates in integer cents: `25500` means CNY 255.00.

| Coupon | Rule | Discount, CNY | Payable, CNY |
|---|---|---:|---:|
| None | Pay the subtotal | 0.00 | 255.00 |
| SAVE30 | Spend at least 200.00; receive 30.00 off | 30.00 | 225.00 |
| TENOFF | Spend at least 100.00; receive 10% off | 25.50 | 229.50 |
| BIGSAVE | Receive 500.00 off, capped at the subtotal | 255.00 | 0.00 |

Unknown or expired Coupons, an unmet minimum, unknown Products and invalid quantities produce an explicit refusal. A separate rounding case uses a subtotal of CNY 3.33 and an eligible 10% Coupon: the discount is CNY 0.33 and payable is CNY 3.00.

The [requirements](00-input/requirements.md) define these fictional rules. The [acceptance expectations](00-input/ACCEPTANCE_ORACLE.md) explain 30 cases with [literal expected results](00-input/acceptance-oracle.json); the tests compare against those values.

## Run the example

You need **Python 3.9+** and a checkout of this repository. The code uses the standard library; no `pip install`, service or account is needed. Installing the skills alone does not download this example into your project.

In a terminal:

```bash
git clone https://github.com/kinglez/mkl-uml.git
cd mkl-uml
python3 examples/order-pricing/09-reference-implementation/run_example.py
```

If you already have the checkout, start from its root and run only the Python command. Use `python` instead of `python3` if that is your Python 3 executable.

The program prints six JSON lines: four successful quotes matching the table above, an unknown-Coupon refusal and an exact-expiry refusal. For example, the SAVE30 line is:

```json
{"coupon": "SAVE30", "result": {"ok": true, "subtotal": 25500, "discount": 3000, "payable": 22500, "currency": "CNY"}}
```

Then run the combined checks:

```bash
python3 examples/order-pricing/scripts/verify.py
```

A successful run ends with `Result: PASS`. Logs and the current result are written under `examples/order-pricing/validation/latest/`. The verifier checks the reviewed source baseline, runs the skill validators, compares generated inspection headers, and executes the implementation tests and examples.

It also reports `Formal gate: NOT FULLY VERIFIED; no human approval is claimed.` That is the declared review boundary: the technical example can pass while formal human/business acceptance is still absent. If the verifier reports a stale baseline, review the changed artifact before recording a replacement baseline.

## Eight-stage artifacts

Read the rows in order. Each stage answers a different question about the same pricing request. **PlantUML** (`.puml`) files are editable diagram source; PNG and SVG files are rendered previews.

| Stage | Question it answers | Start with this file | Diagram preview |
|---|---|---|---|
| Input | What must the pricing request do? | [Requirements](00-input/requirements.md) | — |
| 1. Domain model | What business concepts exist? | [Domain model](01-domain/domain.puml) and [glossary](01-domain/glossary.md) | [PNG](01-domain/domain.png) · [SVG](01-domain/domain.svg) |
| 2. Use cases | Who uses the system, and for what goal? | [Shopper and CU-01](02-use-cases/use-cases.puml) | [PNG](02-use-cases/use-cases.png) · [SVG](02-use-cases/use-cases.svg) |
| 3. Specification | What happens on success and refusal? | [CU-01 Quote cart](03-spec/CU01-quote-cart.md) | — |
| 4. Robustness analysis | Which interface, coordination responsibilities and business concepts realize the behavior? | [DR-01](04-robustness/robustness.puml) and [step correspondence](04-robustness/correspondence.md) | [PNG](04-robustness/robustness.png) · [SVG](04-robustness/robustness.svg) |
| 5. PDR | Is the analysis consistent enough for detailed design? | [PDR findings and handoff](05-pdr/PDR-01.md) | — |
| 6. Sequence design | Which participants collaborate, in which order? | [DS-01](06-interactions/sequence.puml), [operation allocation](06-interactions/operation-delta.md) and [test plan](06-interactions/test-plan.md) | [PNG](06-interactions/sequence.png) · [SVG](06-interactions/sequence.svg) |
| 7. Class design | Which class owns each typed value and operation? | [MC-01](07-class-model/classes.puml) and [member origins](07-class-model/provenance.md) | [PNG](07-class-model/classes.png) · [SVG](07-class-model/classes.svg) |
| 8. CDR | Do the detailed models, contracts and tests agree? | [CDR findings and conclusions](08-cdr/CDR-01.md) | — |
| Additional code evidence | Does the proposed design work for the tested cases? | [Runnable implementation](09-reference-implementation/README.md) | — |

**PDR** means Preliminary Design Review. It checks the analysis before detailed design. **CDR** means Critical Design Review. It checks the detailed design before implementation handoff. This example also supplies executable code as additional evidence for CDR.

For a concrete reading exercise, follow **SAVE30** through [TRACEABILITY.md](TRACEABILITY.md): the requirement becomes a use case branch, then responsibilities, calls, class operations and a test expecting `22500` cents payable.

### Conceptual domain

The first diagram names the business concepts before choosing implementation classes:

![Conceptual domain: Cart, CartLine, Product, Coupon and PriceQuote](01-domain/domain.png)

### Where the files live

```text
examples/order-pricing/
├── 00-input/                    Requirements and expected test results
├── 01-domain/                   Business concepts and glossary
├── 02-use-cases/                Shopper, system boundary and CU-01
├── 03-spec/                     Success/refusal flows and interface contract
├── 04-robustness/               Interface, coordination and entity analysis
├── 05-pdr/                      Analysis findings, corrections and handoff
├── 06-interactions/             Sequences, operation allocation and test plan
├── 07-class-model/              Typed classes, member origins and SOLID evidence
├── 08-cdr/                      Detailed-design review and inspection headers
├── 09-reference-implementation/ Runnable Python code, tests and extension
├── scripts/verify.py            Combined verification entry point
└── index.html                   Local offline reader
```

To regenerate diagrams, install PlantUML locally and run these commands from the repository root:

```bash
python3 examples/order-pricing/scripts/verify.py --render
python3 examples/order-pricing/scripts/build_viewer.py
```

Open `examples/order-pricing/index.html` locally for the tabbed reader. The PNG/SVG previews above are already included for GitHub readers. [DS-02](06-interactions/contract-observation.puml) is an additional before/after-state observation protocol for tests; it is separate from the Shopper's business interaction in DS-01.

## What the reviews actually caught

The example retains real corrections so you can see why the reviews matter:

| Review | Problem found | Correction |
|---|---|---|
| PDR | The analysis invented a rule rejecting a negative Coupon minimum. The requirements had left that policy unspecified. | Remove the invented rule and keep the policy outside the verified scope. |
| Interaction review and CDR | Refusal `break` fragments had incorrect enclosing scope or did not span all affected lifelines. | Correct their placement and frame coverage, then inspect the rendered diagrams. |
| CDR | A class-model multiplicity contradicted shared immutable CartLine values. | Correct the multiplicity and check the resulting declarations. |

Read [CHANGE_IMPACT.md](CHANGE_IMPACT.md) for the before/after artifacts and reinspection. A clean validator result did not establish that these semantic issues were absent.

## Continue with your own work

Use the [step-by-step tutorial](../../docs/EXAMPLES.md) to generate your own outputs under `uml/order-pricing/` while keeping this completed example available for comparison. You can use one skill on its own or follow all eight stages.

After that, try the [discount extension](09-reference-implementation/README.md#expected-evidence). It adds a half-off algorithm capped at CNY 20.00; the main cart's payable becomes CNY 235.00. The [SOLID record](07-class-model/SOLID.md) examines the responsibility, extension, substitution, client and dependency evidence behind this design. Finite tests support scoped conclusions; they do not prove universal SOLID conformance.

## Further reading

| When you need it | Read |
|---|---|
| Exact request/result fields and refusal categories | [Interface contract](03-spec/interface-contract.md) |
| Why a design class, state or operation was added | [Design decisions](06-interactions/DESIGN_DECISIONS.md) and [member origins](07-class-model/provenance.md) |
| Which checks were executed for the published example | [Validation record](VALIDATION.json) and [workflow assessment](WORKFLOW_REVIEW.md) |
| How to intentionally revise the reviewed reference example | [Advanced replay and maintenance](HOW_TO_REPLAY.md) |
| Original review and publication history | [Publication review](PUBLICATION_REVIEW.md), [origin notes](ORIGIN.json) and [source snapshot](SKILL_SOURCE.json) |

The current validator baseline is **1.0.3**. Historical review sections retain their original context; a local verification run supplies current execution evidence. Requirements, expected results and source baselines are recorded separately from formal acceptance.

This is a bounded teaching example. Tax, shipping, payment, authentication, persistence, concurrency, fault recovery and production time authority need additional design and verification in a real system. The technical review supports this example; formal human/customer/business acceptance remains **Not fully verified**. Inspection headers are review aids rather than executable Java implementations.
