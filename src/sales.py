from dataclasses import dataclass

from src.service import InventoryService


@dataclass
class Order:
    id: str
    product_id: str
    quantity: int
    confirmed: bool = False


class SalesService:
    """Coordinate order confirmation and product-specific stock fulfillment."""

    def __init__(self, inventory: InventoryService):
        self.inventory = inventory
        self.orders: dict[str, Order] = {}

    def place_order(self, order_id: str, product_id: str, quantity: int) -> Order:
        if order_id in self.orders:
            raise ValueError(f"คำสั่งซื้อ '{order_id}' มีอยู่แล้ว")
        product = self._get_product(product_id)
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("จำนวนสั่งซื้อต้องเป็นจำนวนเต็ม")
        if quantity <= 0:
            raise ValueError("จำนวนสั่งซื้อต้องมากกว่าศูนย์")
        if product.product_type not in {"physical", "digital"}:
            raise ValueError(f"ไม่รองรับชนิดสินค้า: {product.product_type}")
        if product.product_type == "physical" and quantity > product.quantity:
            raise ValueError("จำนวนคงเหลือไม่พอ")

        order = Order(order_id, product_id, quantity)
        self.orders[order_id] = order
        return order

    def confirm_order(self, order_id: str) -> Order:
        order = self._get_order(order_id)
        if order.confirmed:
            return order

        product = self._get_product(order.product_id)
        if product.product_type == "physical":
            self.inventory.dispense_stock(order.product_id, order.quantity)
        order.confirmed = True
        return order

    def download_link(self, order_id: str) -> str:
        order = self._get_order(order_id)
        if not order.confirmed:
            raise ValueError("คำสั่งซื้อยังไม่ได้ยืนยัน")

        product = self._get_product(order.product_id)
        if product.product_type != "digital":
            raise ValueError("สินค้านี้ไม่มีลิงก์ดาวน์โหลด")
        if not product.download_url:
            raise ValueError("ยังไม่ได้กำหนดลิงก์ดาวน์โหลด")
        return product.download_url

    def _get_order(self, order_id: str) -> Order:
        try:
            return self.orders[order_id]
        except KeyError as exc:
            raise KeyError(f"ไม่พบคำสั่งซื้อ '{order_id}'") from exc

    def _get_product(self, product_id: str):
        try:
            return self.inventory.products[product_id]
        except KeyError as exc:
            raise ValueError("ไม่พบสินค้าในระบบ") from exc
