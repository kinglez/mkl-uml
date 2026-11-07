# Order Pricing: architecture between analysis and detailed design

Start with [architecture-brief.md](architecture-brief.md). It explains the same CU-01 goal
at four zoom levels and hands explicit constraints to sequences, classes and code.

| Zoom | Editable source | Preview |
|---|---|---|
| L1 - system context | [context.puml](context.puml) | [PNG](context.png) / [SVG](context.svg) |
| L2 - containers | [container.puml](container.puml) | [PNG](container.png) / [SVG](container.svg) |
| L3 - components | [component.puml](component.puml) | [PNG](component.png) / [SVG](component.svg) |
| L4 - one component's code | [code.puml](code.puml) | [PNG](code.png) / [SVG](code.svg) |

The local program is the only runtime container; its in-memory catalog is an internal
object. L4 focuses on the discount calculation contract. Deployment and a state lifecycle
are not needed by the frozen read-only/local scope; the brief records why.

[Architecture record](architecture.json) links inputs to decisions and views.
[Component map](component-code-map.json) connects responsibilities to actual declarations.
[Review](REVIEW.md) records semantic inspection and limits. They are different kinds of
evidence: a rendered box or a matching hash is not approval of the architecture.

Run the complete example from the repository root:

```bash
python3 examples/order-pricing/scripts/verify.py
python3 examples/order-pricing/scripts/verify.py --render
```

The first command checks current reviewed handoffs, all nine skills, component-to-code
allocation, blocking/revalidation probes and reference behavior. The second also renders
local diagrams. Generated logs are under validation/latest/ and are not review baselines.
