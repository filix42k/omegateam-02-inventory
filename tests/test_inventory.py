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


@pytest.mark.parametrize(
    ("name", "quantity", "price", "message"),
    [
        (" ", 0, 5.0, "ชื่อสินค้าต้องไม่ว่างเปล่า"),
        ("Pen", -1, 5.0, "จำนวนสินค้าต้องไม่ติดลบ"),
        ("Pen", 1, 0, "ราคาต้องมากกว่าศูนย์"),
    ],
)
def test_add_item_rejects_invalid_values(inventory, name, quantity, price, message):
    with pytest.raises(ValueError, match=message):
        inventory.add_item(name, quantity, price)


def test_add_item_rejects_duplicate_name(inventory):
    inventory.add_item("Pen", 1, 5.0)

    with pytest.raises(ValueError, match="มีอยู่ในระบบแล้ว"):
        inventory.add_item("Pen", 2, 5.0)


def test_restock_validates_item_and_amount(inventory):
    with pytest.raises(KeyError, match="ไม่พบสินค้า"):
        inventory.restock("Missing", 1)

    inventory.add_item("Pen", 1, 5.0)
    for amount in (0, -1):
        with pytest.raises(ValueError, match="จำนวนที่เติมต้องมากกว่าศูนย์"):
            inventory.restock("Pen", amount)

    assert inventory.restock("Pen", 2) == 3


def test_total_value_sums_quantity_times_price(inventory):
    assert inventory.get_total_value() == 0
    inventory.add_item("Pen", 3, 5.0)
    inventory.add_item("Ruler", 2, 10.0)

    assert inventory.get_total_value() == 35.0


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
