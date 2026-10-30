"""Pure calculation contract and a registration seam; eligibility stays on Coupon."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Mapping, Optional, Protocol
from .core import Coupon, Refusal


def require_subtotal(subtotal: int, currency: str) -> None:
    if type(subtotal) is not int or subtotal < 0 or currency != "CNY":
        raise ValueError("Policy input requires nonnegative integer CNY cents")


class DiscountPolicy(Protocol):
    def discount(self, subtotal: int, currency: str) -> int:
        """For every accepted subtotal, return integer cents in [0, subtotal], without mutation."""
        ...


@dataclass(frozen=True)
class NoDiscount:
    def discount(self, subtotal: int, currency: str) -> int:
        require_subtotal(subtotal, currency)
        return 0


@dataclass(frozen=True)
class FixedDiscount:
    amount: int

    def __post_init__(self) -> None:
        if type(self.amount) is not int or self.amount < 0:
            raise Refusal("INVALID_COUPON_CONFIGURATION")

    def discount(self, subtotal: int, currency: str) -> int:
        require_subtotal(subtotal, currency)
        return min(self.amount, subtotal)


@dataclass(frozen=True)
class PercentageDiscount:
    basisPoints: int

    def __post_init__(self) -> None:
        if type(self.basisPoints) is not int or not 0 <= self.basisPoints <= 10000:
            raise Refusal("INVALID_COUPON_CONFIGURATION")

    def discount(self, subtotal: int, currency: str) -> int:
        require_subtotal(subtotal, currency)
        return subtotal * self.basisPoints // 10000


class RegistryPolicyResolver:
    def __init__(self, registrations: Mapping[str, Callable[[Coupon], DiscountPolicy]]):
        self._registrations = dict(registrations)

    def resolve(self, coupon: Optional[Coupon]) -> DiscountPolicy:
        if coupon is None:
            return NoDiscount()
        factory = self._registrations.get(coupon.kind)
        if factory is None:
            raise Refusal("INVALID_COUPON_CONFIGURATION")
        return factory(coupon)
