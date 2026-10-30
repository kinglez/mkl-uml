"""Independent, code-only probes; writes no author/source files."""
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

CODE = Path(__file__).resolve().parents[1] / "09-reference-implementation"
sys.path.insert(0, str(CODE))

from pricing.core import Cart, CartLine, Coupon, Product
from pricing.policies import FixedDiscount, NoDiscount
from pricing.service import QuoteService

assert "pricing.adapters" not in sys.modules, "Service imported a concrete adapter"


class ProductLookupOnly:
    def __init__(self):
        self.values = {"BOOK-001": Product("BOOK-001", 12000, "CNY"),
                       "PEN-002": Product("PEN-002", 1500, "CNY")}

    def lookup_product(self, code):
        return self.values.get(code)


class CouponLookupOnly:
    def __init__(self):
        self.values = {"SAVE30": Coupon("SAVE30", "fixed", 20000,
                       datetime(2030, 1, 1, tzinfo=timezone.utc), {"fixedAmount": 3000})}

    def lookup_coupon(self, code):
        return self.values.get(code)


class ResolveOnly:
    def resolve(self, coupon):
        return NoDiscount() if coupon is None else FixedDiscount(coupon.config["fixedAmount"])


products, coupons, resolver = ProductLookupOnly(), CouponLookupOnly(), ResolveOnly()
business_before = deepcopy((products.values, coupons.values))
service = QuoteService(products, coupons, resolver)
cart = Cart((CartLine("BOOK-001", 2), CartLine("PEN-002", 1)))
instant = datetime(2026, 10, 29, tzinfo=timezone.utc)
assert asdict(service.quote(cart, "CNY", "SAVE30", instant)) == {
    "subtotal": 25500, "discount": 3000, "payable": 22500, "currency": "CNY"}
assert asdict(service.quote(cart, "CNY", None, instant)) == {
    "subtotal": 25500, "discount": 0, "payable": 25500, "currency": "CNY"}
assert (products.values, coupons.values) == business_before

from pricing.adapters import InMemoryCatalog, build_port

oracle = json.loads((CODE.parent / "00-input/acceptance-oracle.json").read_text())
catalog = InMemoryCatalog(oracle["fixtures"]["products"], oracle["fixtures"]["coupons"])
port = build_port(catalog)
request = deepcopy(oracle["cases"][1]["input"])
request["cart"][0]["unitPrice"] = 1
request["products"] = {"BOOK-001": {"unitPrice": 1, "currency": "CNY"}}
request["coupons"] = {"SAVE30": {"kind": "fixed", "fixedAmount": 25500, "minimumSubtotal": 0}}
before = deepcopy((request, catalog.snapshot()))
assert port.handle(request) == {"ok": True, "subtotal": 25500, "discount": 3000,
                                "payable": 22500, "currency": "CNY"}
assert (request, catalog.snapshot()) == before

effects = []


def audit(event, args):
    if event.startswith("socket."):
        effects.append(event)
    if event == "open":
        mode = args[1]
        if isinstance(mode, str) and any(flag in mode for flag in "wax+"):
            effects.append("open:" + mode)


sys.addaudithook(audit)
for _ in range(2):
    assert port.handle(request) == {"ok": True, "subtotal": 25500, "discount": 3000,
                                    "payable": 22500, "currency": "CNY"}
    assert (request, catalog.snapshot()) == before
assert effects == [], effects
print(json.dumps({"narrow_lookup_and_resolver_replacement": "passed",
                  "service_imports_no_concrete_adapter": True,
                  "request_cannot_override_product_or_coupon_catalog": "passed",
                  "business_values_unchanged": True,
                  "observed_file_write_or_socket_audit_events_during_quotes": effects,
                  "limit": "Finite runtime probes plus source inspection; no final model CDR disposition"}, indent=2))
