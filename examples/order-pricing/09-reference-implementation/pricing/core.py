"""Business values and rules; no adapter, I/O, registry or framework imports."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Mapping, Tuple


class Refusal(Exception):
    def __init__(self, reasonCategory: str):
        super().__init__(reasonCategory)
        self.reasonCategory = reasonCategory


def utc_instant(value: Any, reason: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise Refusal(reason)
    return value


@dataclass(frozen=True)
class Product:
    code: str
    unitPrice: int
    currency: str


@dataclass(frozen=True)
class CartLine:
    productCode: str
    quantity: int


@dataclass(frozen=True)
class Cart:
    lines: Tuple[CartLine, ...]

    def validate(self) -> None:
        if not self.lines:
            raise Refusal("EMPTY_CART")
        for line in self.lines:
            if not isinstance(line.productCode, str):
                raise Refusal("INVALID_PRODUCT_CODE")
            if type(line.quantity) is not int or not 1 <= line.quantity <= 99:
                raise Refusal("INVALID_QUANTITY")

    def subtotal(self, products: Mapping[str, Product], currency: str) -> int:
        self.validate()
        total = 0
        for line in self.lines:
            product = products.get(line.productCode)
            if product is None:
                raise Refusal("UNKNOWN_PRODUCT")
            if (type(product.unitPrice) is not int or product.unitPrice < 0
                    or product.currency != currency or currency != "CNY"):
                raise Refusal("INVALID_PRODUCT_CONFIGURATION")
            total += product.unitPrice * line.quantity
        return total


@dataclass(frozen=True)
class Coupon:
    code: str
    kind: str
    minimumSubtotal: int
    expiresAt: datetime
    config: Mapping[str, Any]
    currency: str = "CNY"

    def check_eligibility(self, subtotal: int, evaluatedAt: datetime, currency: str) -> None:
        if type(self.minimumSubtotal) is not int or self.currency != currency or currency != "CNY":
            raise Refusal("INVALID_COUPON_CONFIGURATION")
        utc_instant(self.expiresAt, "INVALID_COUPON_CONFIGURATION")
        utc_instant(evaluatedAt, "INVALID_EVALUATION_TIME")
        # A negative minimum's business policy is deliberately outside the verified baseline.
        # No independent sign-rejection rule is added here.
        if evaluatedAt >= self.expiresAt:
            raise Refusal("EXPIRED_COUPON")
        if subtotal < self.minimumSubtotal:
            raise Refusal("COUPON_MINIMUM_NOT_REACHED")


@dataclass(frozen=True)
class PriceQuote:
    subtotal: int
    discount: int
    payable: int
    currency: str

    def __post_init__(self) -> None:
        if (any(type(value) is not int for value in (self.subtotal, self.discount, self.payable))
                or self.subtotal < 0 or not 0 <= self.discount <= self.subtotal
                or self.payable != self.subtotal - self.discount or self.currency != "CNY"):
            raise Refusal("POLICY_CONTRACT_VIOLATION")
