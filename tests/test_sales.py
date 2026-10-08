import pytest

from src.models import Category, Product
from src.service import InventoryService
from src.sales import SalesService


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
