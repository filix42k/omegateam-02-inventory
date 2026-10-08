import pytest

from inventory import Inventory


@pytest.fixture
def inventory():
    return Inventory()


def test_returns_empty_when_every_item_is_above_threshold(inventory):
    inventory.add_item("Pencil", 8, 5.0)
    inventory.add_item("Ruler", 12, 10.0)

    assert inventory.low_stock_items(3) == []


def test_includes_item_equal_to_threshold(inventory):
    inventory.add_item("Pencil", 3, 5.0)

    assert [item.name for item in inventory.low_stock_items(3)] == ["Pencil"]


def test_returns_qualifying_items_sorted_by_name(inventory):
    inventory.add_item("Ruler", 1, 10.0)
    inventory.add_item("Eraser", 2, 3.0)
    inventory.add_item("Pencil", 20, 5.0)

    assert [item.name for item in inventory.low_stock_items(2)] == ["Eraser", "Ruler"]


def test_returns_empty_for_empty_inventory(inventory):
    assert inventory.low_stock_items(5) == []


def test_zero_threshold_returns_only_zero_quantity_items(inventory):
    inventory.add_item("Pencil", 0, 5.0)
    inventory.add_item("Ruler", 1, 10.0)

    assert [item.name for item in inventory.low_stock_items(0)] == ["Pencil"]


def test_negative_threshold_returns_empty_list(inventory):
    inventory.add_item("Pencil", 0, 5.0)

    assert inventory.low_stock_items(-1) == []
