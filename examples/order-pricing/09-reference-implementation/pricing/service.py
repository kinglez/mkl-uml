"""Application-owned collaborator contracts and the CU-01 coordinator."""
from __future__ import annotations
from datetime import datetime
from typing import Optional, Protocol
from .core import Cart, Coupon, PriceQuote, Product, Refusal, utc_instant
from .policies import DiscountPolicy


class ProductCatalog(Protocol):
    def lookup_product(self, code: str) -> Optional[Product]: ...


class CouponCatalog(Protocol):
    def lookup_coupon(self, code: str) -> Optional[Coupon]: ...


class PolicyResolver(Protocol):
    def resolve(self, coupon: Optional[Coupon]) -> DiscountPolicy: ...


class QuoteService:
    def __init__(self, product_catalog: ProductCatalog, coupon_catalog: CouponCatalog,
                 policy_resolver: PolicyResolver):
        self._product_catalog = product_catalog
        self._coupon_catalog = coupon_catalog
        self._policy_resolver = policy_resolver

    def quote(self, cart: Cart, currency: str, couponCode: Optional[str],
              evaluatedAt: datetime) -> PriceQuote:
        cart.validate()
        if currency != "CNY":
            raise Refusal("UNSUPPORTED_CURRENCY")
        utc_instant(evaluatedAt, "INVALID_EVALUATION_TIME")
        if couponCode is not None and not isinstance(couponCode, str):
            raise Refusal("INVALID_COUPON_CODE")
        products = {}
        for line in cart.lines:
            product = self._product_catalog.lookup_product(line.productCode)
            if product is None:
                raise Refusal("UNKNOWN_PRODUCT")
            products[line.productCode] = product
        subtotal = cart.subtotal(products, currency)
        coupon = None
        if couponCode is not None:
            coupon = self._coupon_catalog.lookup_coupon(couponCode)
            if coupon is None:
                raise Refusal("UNKNOWN_COUPON")
        policy = self._policy_resolver.resolve(coupon)
        if coupon is not None:
            coupon.check_eligibility(subtotal, evaluatedAt, currency)
        discount = policy.discount(subtotal, currency)
        if type(discount) is not int or not 0 <= discount <= subtotal:
            raise Refusal("POLICY_CONTRACT_VIOLATION")
        return PriceQuote(subtotal, discount, subtotal - discount, currency)
