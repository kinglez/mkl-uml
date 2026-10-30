# Actor / goal / source map

| Stable identity | Name | Responsibility or goal | Source |
|---|---|---|---|
| ACT-01 | Shopper | Requests an item-amount quote and receives a result or refusal | Baseline 1 user goal; RF-01, RF-06–RF-09 |
| CU-01 | Quote cart | One user-level goal; subordinate validation, lookup and calculation remain internal behavior | [requirements](../00-input/requirements.md), [specification](../03-spec/CU01-quote-cart.md) |

There is one goal. An optional Coupon creates alternative flows inside CU-01. It does not justify a separate extension use case because the supplied requirements define no separately reusable actor goal. There is no forced include/extend, login, checkout or order-placement use case.

The trusted catalog snapshot and in-memory data adapter are inside Order Pricing for this local demo, so they are not external actors. External catalog integration is explicitly excluded. Shopper participation is undirected; the textual trigger records who initiates.

CU-01 is preserved from the supplied baseline. ACT-01 is an initially allocated local identity, with no previous actor registry to overwrite. Display order and diagram aliases are not trace identities.
