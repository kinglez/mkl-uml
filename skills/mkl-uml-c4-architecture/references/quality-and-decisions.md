# Functional and quality questions

Read available answers first. Inputs can be tickets, conversation, images, documentation,
interfaces or observed systems. Preserve source references, versions and uncertainty.
Requirement classification aids coverage and need not be mutually exclusive.

| Area | Questions that can affect architecture |
|---|---|
| Functional behavior | Who does what, with which inputs/results, rules, state and alternatives? |
| Data and failure | Which source is authoritative? What happens on duplicate, concurrent or partially failed work? |
| Performance/capacity | What workload, data size, latency/throughput budget and resource constraints apply? |
| Availability/recovery | What outages, recovery time and data-loss bounds are acceptable? |
| Security/privacy | Which identities, isolation, data protection and audit obligations apply? |
| Observability/operations | How are failures detected, diagnosed, rolled back and recovered? |
| Maintainability/compatibility | Which actual changes/consumers must be supported, and with what compatibility expectations? |
| Deployment/cost | What existing stack, network, environment and budget constraints are authoritative? |

For each relevant quality scenario record context/environment/load, triggering event,
expected response, observable measure/criterion, verification method, source and priority.
Keep undefined targets open; recommendations do not establish confirmation. An irrelevant
dimension gets a source-based applicability reason, not a fictional numerical objective.

Relate confirmed inputs to design decisions, affected views/elements and planned checks.
A decision can retain the existing design. Record the reason, alternatives and costs.
Do not default to caching, queues, microservices or eventual consistency without a driver.

The optional checker only verifies declared nonempty scenario fields and reference
coverage. Reviewers must assess whether the criterion is specific, measurable, consistent
and sufficient. Runtime/load/failure/security checks must actually be executed before
claiming those qualities achieved.
