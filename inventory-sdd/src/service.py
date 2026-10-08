"""Business logic ของระบบ inventory สำหรับ Lab 3."""

from typing import Any, Mapping

from src.models import Product, StockTransaction
from src.notifiers import Notifier


class InventoryService:
    """จัดการสินค้า, ธุรกรรม, รายงาน และการแจ้งเตือนผ่าน abstraction."""

    def __init__(self, observers: Mapping[str, Notifier] | None = None) -> None:
        """รับ notifier ตามช่องทางผ่าน dependency injection."""
        self.products: dict[str, Product] = {}
        self.transactions: list[StockTransaction] = []
        self.observers: dict[str, Notifier] = {
            channel.strip().lower(): notifier
            for channel, notifier in (observers or {}).items()
        }

    def add_observer(self, channel: str, observer: Notifier) -> None:
        """ลงทะเบียน observer สำหรับช่องทางที่ระบุ."""
        normalized_channel = channel.strip().lower()
        if not normalized_channel:
            raise ValueError("ชื่อช่องทางแจ้งเตือนต้องไม่ว่างเปล่า")
        self.observers[normalized_channel] = observer

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าใหม่และปฏิเสธรหัสซ้ำ."""
        if product.id in self.products:
            raise ValueError(f"รหัสสินค้า '{product.id}' มีอยู่ในระบบแล้ว")
        self._validate_channels(product.notification_channels)
        self.products[product.id] = product

    def receive_stock(self, product_id: str, quantity: int) -> int:
        """รับสินค้าเมื่อจำนวนมากกว่าศูนย์และคืนยอดคงเหลือใหม่."""
        self._validate_quantity(quantity)
        product = self._get_product(product_id)
        product.quantity += quantity
        self.transactions.append(
            StockTransaction(product_id, "in", quantity)
        )
        return product.quantity

    def dispense_stock(self, product_id: str, quantity: int) -> int:
        """จ่ายสินค้า ตรวจยอด และแจ้งเมื่อข้ามจากไม่ต่ำเป็นต่ำกว่า threshold."""
        self._validate_quantity(quantity)
        product = self._get_product(product_id)
        if product.quantity < quantity:
            raise ValueError("จำนวนคงเหลือไม่พอ")

        previous_quantity = product.quantity
        product.quantity -= quantity
        self.transactions.append(
            StockTransaction(product_id, "out", quantity)
        )
        if previous_quantity >= product.threshold and product.quantity < product.threshold:
            self._notify_low_stock(product)
        return product.quantity

    def _notify_low_stock(self, product: Product) -> None:
        """แจ้งเฉพาะ observer ที่เลือกไว้ในสินค้านั้น."""
        message = (
            f"แจ้งเตือนสต็อกต่ำ: สินค้า {product.name} คงเหลือ "
            f"{product.quantity} (Threshold: {product.threshold})"
        )
        for channel in product.notification_channels:
            observer = self.observers.get(channel)
            if observer is not None:
                observer.notify(message)

    def get_stock_value_report(self) -> dict[str, Any]:
        """คำนวณมูลค่าสต็อกแยกหมวดและมูลค่ารวม."""
        if not self.products:
            return {
                "message": "ยังไม่มีข้อมูลสินค้าในระบบ",
                "categories": {},
                "total_value": 0.0,
            }

        category_totals: dict[str, float] = {}
        for product in self.products.values():
            value = product.quantity * product.price
            category_name = product.category.name
            category_totals[category_name] = (
                category_totals.get(category_name, 0.0) + value
            )

        return {
            "message": "รายงานมูลค่าสต็อก",
            "categories": category_totals,
            "total_value": sum(category_totals.values()),
        }

    def set_product_threshold(self, product_id: str, threshold: int) -> None:
        """ตั้ง threshold รายสินค้าและปฏิเสธค่าติดลบ."""
        if threshold < 0:
            raise ValueError("Threshold ไม่สามารถเป็นค่าติดลบได้")
        self._get_product(product_id).threshold = threshold

    def set_notification_channels(
        self, product_id: str, channels: tuple[str, ...] | list[str]
    ) -> None:
        """ตั้งช่องทาง Email, SMS หรือหลายช่องทางให้สินค้า."""
        normalized = tuple(channel.strip().lower() for channel in channels)
        if not normalized or any(not channel for channel in normalized):
            raise ValueError("ต้องเลือกช่องทางแจ้งเตือนอย่างน้อยหนึ่งช่องทาง")
        self._validate_channels(normalized)
        self._get_product(product_id).notification_channels = normalized

    def _validate_channels(self, channels: tuple[str, ...]) -> None:
        """ตรวจว่ามี observer ตั้งค่าไว้ครบทุกช่องทางของสินค้า."""
        missing = [channel for channel in channels if channel not in self.observers]
        if missing:
            raise ValueError(
                f"ยังไม่ได้ตั้งค่า notifier สำหรับช่องทาง: {', '.join(missing)}"
            )

    def _get_product(self, product_id: str) -> Product:
        """ค้นหาสินค้าและแจ้งข้อผิดพลาดเมื่อไม่มีรหัสนั้น."""
        try:
            return self.products[product_id]
        except KeyError as error:
            raise ValueError("ไม่พบข้อมูลสินค้านี้ในระบบ") from error

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        """ปฏิเสธจำนวนรับหรือจ่ายที่น้อยกว่าหรือเท่ากับศูนย์."""
        if quantity <= 0:
            raise ValueError("จำนวนสินค้าต้องมากกว่า 0")
