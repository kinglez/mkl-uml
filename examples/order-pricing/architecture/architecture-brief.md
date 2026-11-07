# Order Pricing high-level architecture

## Purpose, inputs and review boundary

This is a **2026-11-07 architecture replay** of the existing bounded teaching example.
It uses the frozen [business requirements](../00-input/requirements.md), independent
[oracle](../00-input/ACCEPTANCE_ORACLE.md), analysis and [PDR](../05-pdr/PDR-01.md), then
compares the architecture with existing detailed design and code. It does not claim
that architecture diagrams existed during the original October implementation, or
that code was independently regenerated from unseen requirements in this replay.

Confirmed means part of the frozen fictional demo baseline. The user authorized this
technical example; no customer, architect or human business acceptance is invented.
The baseline excludes unresolved negative-minimum policy and simultaneous-fault priority.

## From the goal to a runtime boundary

CU-01 receives Product codes, quantities, CNY, an optional Coupon code and explicit UTC.
It returns an immutable successful amount or a refusal, without changing inputs or
creating an Order. Product prices and Coupon definitions belong to trusted setup data.

Retain **one local Python program**, the already supplied reference runner plus library.
RNF-03 permits an in-memory adapter and requires no live service. The library is not
promoted into a fictitious web application. The trusted catalog is an object in the
same process, not a database or remote service. The Shopper remains an external role;
Product/Coupon data are not external actors or software systems.

| View | Scope / stable identity | Next design question |
|---|---|---|
| [L1 context](context.puml) | `order_pricing`, Shopper | What is inside the quoting goal? |
| [L2 containers](container.puml) | `order_pricing` contains `pricing_app` | Which runtime boundary owns this behavior? |
| [L3 components](component.puml) | `pricing_app` contains six responsibility groups | Where are trust, calculation, orchestration and extension seams? |
| [L4 code](code.puml) | `discount_engine` contract-focused projection of MC-01 | Which types realize the common calculation contract? |
| Deployment | Not applicable for this delivery | No infrastructure question or production host is specified. |

For a new implementation, L1-L3 establish the high-level handoff; L4 is refined
with detailed class design and shown here in the completed zoom gallery. The current
replay inspects existing code at all levels.

The official C4 levels are context, containers, components and code; deployment is a
supporting view. L4 uses ordinary UML classes. The full [MC-01](../07-class-model/classes.puml)
is an application design view spanning components, so it is not relabeled as one
component's L4. The scoped code view omits resolver detail intentionally.

## Responsibilities and ownership

| Component | Owns | Concrete implementation / detailed consumer |
|---|---|---|
| `request_boundary` | Allowed request fields, request UTC decoding, success/refusal representation | QuoteRequestPort using the shared adapter decoder; DS-01 entry and refusal exits |
| `quote_workflow` | CU-01 coordination and application-owned ProductCatalog, CouponCatalog, PolicyResolver ports | QuoteService / Protocols; DS-01 ordering |
| `domain_rules` | Validation, cents arithmetic, Coupon eligibility, immutable result invariants | Cart, CartLine, Product, Coupon, PriceQuote, Refusal; MC-01 |
| `discount_engine` | Registered policy resolution and pure discount contract | DiscountPolicy, NoDiscount, FixedDiscount, PercentageDiscount, RegistryPolicyResolver; scoped L4 |
| `catalog_snapshot` | Detached trusted setup data and validated domain lookup results | InMemoryCatalog, snapshot observation; DS-02 |
| `composition` | Setup wiring and policy-factory registration | build_port / default_registrations; the extension exercise |

[component-code-map.json](component-code-map.json) links all six components, all 17
modeled classifiers and actual Python declarations. Logical responsibilities may share
one module: adapters.py contains boundary, catalog and setup responsibilities. Its
parse_utc function is an explicitly shared adapter helper used by both request decoding
and trusted Coupon expiry decoding, with caller-specific refusal categories. The map
records both consumers; no extra component or domain-rule ownership is implied. A component
is not mechanically one source file, BCE control, microservice or class. Runtime arrows
in L3 describe calls/wiring, not source dependency direction.

Request data cannot become authoritative catalog data. A policy sees a validated CNY
subtotal; Coupon configuration/eligibility and the pure calculation contract are distinct.
An eligibility refusal must terminate before discount invocation. A malformed injected
discount must produce no successful quote. Registration may change; service/core behavior
must remain unchanged when adding the demonstrated algorithm.

## Decisions and alternatives

The [architecture record](architecture.json) contains ARC-01 through ARC-06, each linked
to driving RF/RN/RNF inputs and actual views. These are explicit retention decisions
against current evidence, not new business policies.

| Choice | Alternative / cost |
|---|---|
| Single local program | Separate services/database add runtime/failure boundaries without an in-scope driver. No distributed or HA claim is made. |
| Decode untrusted input before coordination | Passing client-supplied catalog/prices into the service breaks data authority. Local demo authority is not production authentication. |
| Immutable domain cents and invariants | Floating-point amounts or mutable results would contradict the baseline. Validation has the declared bounded input domain. |
| Registered policy seam | A kind switch in QuoteService couples extension to workflow edits. Factory/configuration/wiring changes remain allowed. |
| Small application-owned ports | Exposing a whole adapter/service locator adds capabilities clients do not need. This is supported by source and replacement tests, not interface symbols alone. |
| Read-only snapshot | No order/persistence/redemption capability or state lifecycle is introduced. A future write goal requires fresh requirements and design. |

## Functional and quality questions actually resolved

Functions and failures come from RF-01 through RF-10 and the CU-01 FA/FE branches.
The five quality scenarios QS-01 through QS-05 refine RNF-01 through RNF-05. Each records
context, stimulus, response, observable measure and an executable verification method.

| Quality | Observable evidence required |
|---|---|
| Extension | Capped-half fixture/registration returns literal payable 23500; service.py/core.py unchanged. |
| Determinism and read-only behavior | Both executions of every one of 30 oracle cases match literal expectations and leave all observed state unchanged. |
| Local portability | Standard-library tests and runners exit 0 on the actual tested Python 3.9/3.12 environments. |
| Substitution | Shared policy vectors and invalid-input preconditions hold; a broken injected result cannot produce a successful quote. Finite evidence is bounded. |
| Replaceable small contracts | Spies show eligibility refusal does not call discount; replacement collaborators expose only required capabilities. |

No latency, throughput, concurrency, recovery-time, data-loss or availability target was
provided. These are **outside this example's accepted scope**, rather than silently
satisfied or assigned plausible numbers. Production authentication/privacy, persistence,
remote catalog failure, clock authority, deployment and cost need new scope/evidence.

## Detailed-design handoff and revalidation

Read this brief, architecture.json, the component map and [architecture review](REVIEW.md)
before relying on the existing DS-01/DS-02, MC-01 or implementation. The reviewed snapshot
is [handoffs/architecture.json](../handoffs/architecture.json); the design handoff includes
it as an input. Hashes detect a changed baseline, not semantic approval.

Detailed design must preserve the responsibility/ownership table, trusted-price origin,
integer cents, explicit UTC, separate eligibility/calculation, refusal termination and
shared policy contract. The existing sequence and class decisions have a dated replay
section documenting that comparison. CDR additionally compares architecture with actual
code and tests; its current CLI does not parse C4 automatically.

No state diagram is needed for a read-only quote with no persistent lifecycle. Deployment
is omitted for a stated scope reason. A source change reopens affected architecture and
design evidence. Strict mechanical checks, real rendering, semantic review, executed
behavior and formal approval remain distinct results.
