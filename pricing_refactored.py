"""Readable replacement for the instructor's legacy pricing calculation.

The public ``calc`` function and its observable module state are preserved so
existing callers and characterization tests keep the same behavior.
"""

import datetime
from collections.abc import Iterable

TAX_RATE = 0.07
MEMBER_DISCOUNT_RATE = 0.05
POINTS_PER_CURRENCY = 100
BULK_DISCOUNTS = ((100, 0.9), (50, 0.95))
COUPON_RATES = {"HALF": 0.5}
NEW_YEAR_COUPON = "NEWYEAR"
FIXED_DISCOUNT_COUPON = "SAVE50"
FIXED_DISCOUNT_AMOUNT = 50

member_points: dict[str, int] = {}
LOG: list[tuple[str | None, float]] = []


def _line_total(quantity: int, unit_price: float) -> float:
    if quantity <= 0:
        return 0

    subtotal = quantity * unit_price
    for minimum_quantity, discount_multiplier in BULK_DISCOUNTS:
        if quantity >= minimum_quantity:
            return subtotal * discount_multiplier
    return subtotal


def _subtotal(items: Iterable[tuple[str, int, float]]) -> float:
    return sum(_line_total(quantity, unit_price) for _, quantity, unit_price in items)


def _apply_member_discount(total: float, member: str | None) -> float:
    if member is None:
        return total

    member_points.setdefault(member, 0)
    discounted_total = total * (1 - MEMBER_DISCOUNT_RATE)
    member_points[member] += int(discounted_total / POINTS_PER_CURRENCY)
    return discounted_total


def _apply_coupon(
    total: float,
    coupon: str | None,
    today: datetime.date | None,
) -> float:
    if coupon is None:
        return total
    if coupon == FIXED_DISCOUNT_COUPON:
        return total - FIXED_DISCOUNT_AMOUNT
    if coupon in COUPON_RATES:
        return total * COUPON_RATES[coupon]
    if coupon == NEW_YEAR_COUPON:
        coupon_date = today if today is not None else datetime.date.today()
        if coupon_date.month == 1:
            return total * 0.8
    return total


def calc(
    items: Iterable[tuple[str, int, float]],
    member: str | None = None,
    coupon: str | None = None,
    today: datetime.date | None = None,
) -> float:
    """Return the rounded, taxed total and preserve legacy side effects/order."""
    total = _subtotal(items)
    total = _apply_member_discount(total, member)
    total = _apply_coupon(total, coupon, today)
    total = max(total, 0)
    total = total + total * TAX_RATE
    total = round(total, 2)
    LOG.append((member, total))
    return total
