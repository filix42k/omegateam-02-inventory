import datetime

import pytest

import pricing_refactored as pricing


@pytest.fixture(autouse=True)
def reset_legacy_state():
    pricing.member_points.clear()
    pricing.LOG.clear()
    yield
    pricing.member_points.clear()
    pricing.LOG.clear()


def test_regular_price_adds_tax_and_logs_result():
    assert pricing.calc([("Pen", 2, 10)]) == 21.4
    assert pricing.LOG == [(None, 21.4)]


@pytest.mark.parametrize(
    ("quantity", "expected"),
    [(50, 101.65), (100, 192.6)],
)
def test_bulk_discount_thresholds_are_inclusive(quantity, expected):
    assert pricing.calc([("Pen", quantity, 2)]) == expected


def test_zero_quantity_is_ignored():
    assert pricing.calc([("Pen", 0, 10)]) == 0.0


def test_member_discount_and_points_are_recorded_after_member_discount():
    assert pricing.calc([("Pen", 10, 20)], member="member-1") == 203.3
    assert pricing.member_points == {"member-1": 1}
    assert pricing.LOG == [("member-1", 203.3)]


def test_save50_coupon_subtracts_fifty_before_tax():
    assert pricing.calc([("Pen", 10, 10)], coupon="SAVE50") == 53.5


def test_half_coupon_halves_subtotal_before_tax():
    assert pricing.calc([("Pen", 10, 10)], coupon="HALF") == 53.5


def test_newyear_coupon_applies_in_january():
    assert pricing.calc(
        [("Pen", 10, 10)], coupon="NEWYEAR", today=datetime.date(2026, 1, 15)
    ) == 85.6


def test_newyear_coupon_does_not_apply_in_february():
    assert pricing.calc(
        [("Pen", 10, 10)], coupon="NEWYEAR", today=datetime.date(2026, 2, 15)
    ) == 107.0


def test_unknown_coupon_has_no_effect():
    assert pricing.calc([("Pen", 10, 10)], coupon="UNKNOWN") == 107.0


def test_total_below_zero_is_clamped_before_tax():
    assert pricing.calc([("Pen", 1, 10)], coupon="SAVE50") == 0.0


def test_log_records_each_call_in_call_order():
    pricing.calc([("Pen", 1, 10)])
    pricing.calc([("Pencil", 1, 20)], member="member-2")

    assert pricing.LOG == [(None, 10.7), ("member-2", 20.33)]


def test_bulk_discount_is_applied_per_line_before_total_discounts():
    assert pricing.calc([("Pen", 49, 2), ("Pencil", 50, 2)]) == 206.51


def test_member_points_and_coupon_keep_the_legacy_order():
    assert pricing.calc([("Pen", 10, 100)], member="member-3", coupon="SAVE50") == 963.0
    assert pricing.member_points == {"member-3": 9}


def test_newyear_uses_current_date_when_date_is_omitted(monkeypatch):
    class JanuaryDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2026, 1, 1)

    monkeypatch.setattr(pricing.datetime, "date", JanuaryDate)
    assert pricing.calc([("Pen", 10, 10)], coupon="NEWYEAR") == 85.6
