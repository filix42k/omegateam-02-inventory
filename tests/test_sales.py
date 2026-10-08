import pytest

from src.models import Category, Product
from src.sales import SalesService
from src.service import InventoryService


@pytest.fixture
def sales_setup():
    inventory = InventoryService()
    inventory.add_product(
        Product("physical-1", "Notebook", Category("Stationery"), 25, quantity=10)
    )
    inventory.add_product(
        Product(
            "digital-1",
            "E-book",
            Category("Digital"),
            99,
            quantity=4,
            product_type="digital",
            download_url="https://example.test/downloads/ebook-1",
        )
    )
    return inventory, SalesService(inventory)


def test_physical_product_sale_reduces_stock_after_confirmation(sales_setup):
    inventory, sales = sales_setup
    sales.place_order("order-1", "physical-1", 3)

    sales.confirm_order("order-1")

    assert inventory.products["physical-1"].quantity == 7


def test_physical_order_above_available_stock_is_rejected(sales_setup):
    inventory, sales = sales_setup
    with pytest.raises(ValueError, match="จำนวนคงเหลือไม่พอ"):
        sales.place_order("order-2", "physical-1", 11)

    assert inventory.products["physical-1"].quantity == 10


def test_digital_product_sale_does_not_reduce_stock(sales_setup):
    inventory, sales = sales_setup
    sales.place_order("order-3", "digital-1", 1)

    sales.confirm_order("order-3")

    assert inventory.products["digital-1"].quantity == 4


def test_digital_download_is_unavailable_until_order_is_confirmed(sales_setup):
    _, sales = sales_setup
    sales.place_order("order-4", "digital-1", 1)

    with pytest.raises(ValueError, match="คำสั่งซื้อยังไม่ได้ยืนยัน"):
        sales.download_link("order-4")

    sales.confirm_order("order-4")
    assert sales.download_link("order-4") == "https://example.test/downloads/ebook-1"


def test_unknown_product_cannot_be_ordered(sales_setup):
    _, sales = sales_setup
    with pytest.raises(ValueError, match="ไม่พบสินค้าในระบบ"):
        sales.place_order("order-5", "missing", 1)


def test_order_rejects_duplicate_id_and_invalid_quantity(sales_setup):
    _, sales = sales_setup
    sales.place_order("order-6", "physical-1", 1)

    with pytest.raises(ValueError, match="มีอยู่แล้ว"):
        sales.place_order("order-6", "physical-1", 1)
    for amount in (0, -1):
        with pytest.raises(ValueError, match="มากกว่าศูนย์"):
            sales.place_order(f"invalid-{amount}", "physical-1", amount)
    for amount in (1.5, "2"):
        with pytest.raises(TypeError, match="จำนวนสั่งซื้อต้องเป็นจำนวนเต็ม"):
            sales.place_order(f"invalid-{amount}", "physical-1", amount)


def test_order_rejects_unsupported_product_type(sales_setup):
    inventory, sales = sales_setup
    inventory.add_product(
        Product(
            "unsupported-1",
            "Service",
            Category("Other"),
            1,
            product_type="service",
        )
    )

    with pytest.raises(ValueError, match="ไม่รองรับชนิดสินค้า"):
        sales.place_order("order-7", "unsupported-1", 1)


def test_confirming_order_twice_does_not_sell_twice(sales_setup):
    inventory, sales = sales_setup
    order = sales.place_order("order-8", "physical-1", 3)

    assert sales.confirm_order("order-8") is order
    assert sales.confirm_order("order-8") is order
    assert inventory.products["physical-1"].quantity == 7


def test_confirmed_physical_product_has_no_download_link(sales_setup):
    _, sales = sales_setup
    sales.place_order("order-9", "physical-1", 1)
    sales.confirm_order("order-9")

    with pytest.raises(ValueError, match="ไม่มีลิงก์ดาวน์โหลด"):
        sales.download_link("order-9")


def test_confirmed_digital_product_requires_a_configured_download_link(sales_setup):
    inventory, sales = sales_setup
    inventory.add_product(
        Product("digital-2", "Another E-book", Category("Digital"), 49, product_type="digital")
    )
    sales.place_order("order-10", "digital-2", 1)
    sales.confirm_order("order-10")

    with pytest.raises(ValueError, match="ยังไม่ได้กำหนดลิงก์ดาวน์โหลด"):
        sales.download_link("order-10")


def test_unknown_order_is_rejected(sales_setup):
    _, sales = sales_setup
    with pytest.raises(KeyError, match="ไม่พบคำสั่งซื้อ"):
        sales.confirm_order("missing")
    with pytest.raises(KeyError, match="ไม่พบคำสั่งซื้อ"):
        sales.download_link("missing")


def test_stock_is_rechecked_when_competing_physical_orders_are_confirmed(sales_setup):
    inventory, sales = sales_setup
    sales.place_order("order-11", "physical-1", 6)
    sales.place_order("order-12", "physical-1", 6)
    sales.confirm_order("order-11")

    with pytest.raises(ValueError, match="จำนวนคงเหลือไม่พอ"):
        sales.confirm_order("order-12")

    assert inventory.products["physical-1"].quantity == 4
    assert not sales.orders["order-12"].confirmed
