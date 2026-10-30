"""Trusted snapshot and untrusted request adapters; construction is separate from quoting."""
from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
from types import MappingProxyType
from typing import Any, Callable, Mapping, Optional
from .core import Cart, CartLine, Coupon, Product, Refusal, utc_instant
from .policies import DiscountPolicy, FixedDiscount, PercentageDiscount, RegistryPolicyResolver
from .service import QuoteService


def parse_utc(value: Any, reason: str) -> datetime:
    try:
        if not isinstance(value, str):
            raise ValueError("An ISO-8601 UTC string is required")
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
        return utc_instant(parsed, reason)
    except (ValueError, TypeError, OverflowError):
        raise Refusal(reason) from None


class InMemoryCatalog:
    def __init__(self, products: Mapping[str, Any], coupons: Mapping[str, Any]):
        self._products = deepcopy(dict(products))
        self._coupons = deepcopy(dict(coupons))

    def lookup_product(self, code: str) -> Optional[Product]:
        raw = self._products.get(code)
        if raw is None:
            return None
        if not isinstance(raw, Mapping):
            raise Refusal("INVALID_PRODUCT_CONFIGURATION")
        price, currency = raw.get("unitPrice"), raw.get("currency")
        if type(price) is not int or price < 0 or currency != "CNY":
            raise Refusal("INVALID_PRODUCT_CONFIGURATION")
        return Product(code, price, currency)

    def lookup_coupon(self, code: str) -> Optional[Coupon]:
        raw = self._coupons.get(code)
        if raw is None:
            return None
        if not isinstance(raw, Mapping) or not isinstance(raw.get("kind"), str):
            raise Refusal("INVALID_COUPON_CONFIGURATION")
        expiry = parse_utc(raw.get("expiresAt"), "INVALID_COUPON_CONFIGURATION")
        return Coupon(code, raw["kind"], raw.get("minimumSubtotal"), expiry,
                      MappingProxyType(deepcopy(raw)), raw.get("currency", "CNY"))

    def snapshot(self) -> Mapping[str, Any]:
        return deepcopy({"products": self._products, "coupons": self._coupons})


class QuoteRequestPort:
    def __init__(self, service: QuoteService):
        self._service = service

    def handle(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        try:
            if not isinstance(request, Mapping):
                raise Refusal("INVALID_REQUEST")
            if request.get("currency") != "CNY":
                raise Refusal("UNSUPPORTED_CURRENCY")
            instant = parse_utc(request.get("evaluatedAt"), "INVALID_EVALUATION_TIME")
            code = request.get("couponCode")
            if isinstance(code, (list, tuple)) and len(code) > 1:
                raise Refusal("MULTIPLE_COUPONS_NOT_ALLOWED")
            if code is not None and not isinstance(code, str):
                raise Refusal("INVALID_COUPON_CODE")
            raw_lines = request.get("cart")
            if not isinstance(raw_lines, (list, tuple)):
                raise Refusal("INVALID_CART")
            if any(not isinstance(line, Mapping) for line in raw_lines):
                raise Refusal("INVALID_CART")
            # Allowlisted business fields only: submitted prices/catalogs never enter the service.
            cart = Cart(tuple(CartLine(line.get("productCode"), line.get("quantity")) for line in raw_lines))
            quote = self._service.quote(cart, "CNY", code, instant)
            return {"ok": True, **asdict(quote)}
        except Refusal as refusal:
            return {"ok": False, "reasonCategory": refusal.reasonCategory}


def default_registrations() -> Mapping[str, Callable[[Coupon], DiscountPolicy]]:
    return {"fixed": lambda coupon: FixedDiscount(coupon.config.get("fixedAmount")),
            "percentage": lambda coupon: PercentageDiscount(coupon.config.get("basisPoints"))}


def build_port(catalog: InMemoryCatalog,
               registrations: Optional[Mapping[str, Callable[[Coupon], DiscountPolicy]]] = None) -> QuoteRequestPort:
    resolver = RegistryPolicyResolver(default_registrations() if registrations is None else registrations)
    return QuoteRequestPort(QuoteService(catalog, catalog, resolver))
