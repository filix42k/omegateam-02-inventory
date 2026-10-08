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


def test_sell_exactly_available_quantity_leaves_zero_stock(inventory):
    inventory.add_item("Pencil", 4, 5.0)

    assert inventory.sell("Pencil", 4) == 0
    assert inventory.low_stock_items(0)[0].quantity == 0


def test_sell_reduces_stock_and_returns_new_balance(inventory):
    inventory.add_item("Pencil", 8, 5.0)

    assert inventory.sell("Pencil", 3) == 5


@pytest.mark.parametrize("amount", [0, -1])
def test_sell_rejects_zero_or_negative_quantity_without_changing_stock(inventory, amount):
    inventory.add_item("Pencil", 4, 5.0)

    with pytest.raises(ValueError, match="จำนวนที่ขายต้องมากกว่าศูนย์"):
        inventory.sell("Pencil", amount)

    assert inventory.low_stock_items(10)[0].quantity == 4


def test_sell_rejects_more_than_available_stock_without_changing_stock(inventory):
    inventory.add_item("Pencil", 4, 5.0)

    with pytest.raises(ValueError, match="ไม่เพียงพอ"):
        inventory.sell("Pencil", 5)

    assert inventory.low_stock_items(10)[0].quantity == 4


def test_sell_missing_item_raises_key_error(inventory):
    with pytest.raises(KeyError, match="ไม่พบสินค้า"):
        inventory.sell("Missing", 1)


@pytest.mark.parametrize("amount", [1.5, "2"])
def test_sell_rejects_non_integer_quantity(inventory, amount):
    inventory.add_item("Pencil", 4, 5.0)

    with pytest.raises(TypeError, match="quantity must be an integer"):
        inventory.sell("Pencil", amount)

    assert inventory.low_stock_items(10)[0].quantity == 4
