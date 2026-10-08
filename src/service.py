from typing import Any

from src.models import Product, StockTransaction
from src.notifiers import Notifier


class InventoryService:
    def __init__(self, observers: list[Notifier] = None):
        """
        รับค่า dependencies เริ่มต้นผ่าน Constructor (DIP)
        :param observers: รายการของ Notifier ที่ทำหน้าที่เป็น Observer
        """
        self.products: dict[str, Product] = {}
        self.transactions: list[StockTransaction] = []
        self.observers: list[Notifier] = observers if observers is not None else []

    def add_observer(self, observer: Notifier) -> None:
        """เพิ่ม Observer เข้าระบบ"""
        self.observers.append(observer)

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าใหม่เข้าสู่ระบบ"""
        self.products[product.id] = product

    def receive_stock(self, product_id: str, quantity: int) -> None:
        """บันทึกรับสินค้าเข้าสต็อกและอัปเดตทันที"""
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")
        
        product = self.products[product_id]
        product.quantity += quantity
        self.transactions.append(
            StockTransaction(
                product_id=product_id,
                transaction_type="in",
                quantity=quantity,
            )
        )

    def dispense_stock(self, product_id: str, quantity: int) -> None:
        """บันทึกจ่ายสินค้าออก ตรวจสอบจำนวนคงเหลือ และแจ้งเตือนหากต่ำกว่า Threshold"""
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")
        
        product = self.products[product_id]
        
        # ตรวจสอบว่าสินค้ามีพอจ่ายหรือไม่ หากไม่พอ Exception จะหยุดการทำงานก่อนเปลี่ยนแปลงสต็อก (NFR-03)
        if product.quantity < quantity:
            raise ValueError("จำนวนคงเหลือไม่พอ")
        
        product.quantity -= quantity
        self.transactions.append(
            StockTransaction(
                product_id=product_id,
                transaction_type="out",
                quantity=quantity,
            )
        )

        self._check_threshold_and_notify(product)

    def _check_threshold_and_notify(self, product: Product) -> None:
        """ตรวจสอบสถานะสต็อกและเรียก notify ทุก observer ถ้าต่ำกว่ากำหนด"""
        if product.quantity < product.threshold:
            message = (
                f"แจ้งเตือนสต็อกต่ำ: สินค้า {product.name} คงเหลือ {product.quantity} "
                f"(Threshold: {product.threshold})"
            )
            for observer in self.observers:
                observer.notify(message)

    def get_stock_value_report(self) -> dict[str, Any]:
        """คำนวณและคืนค่ารายงานมูลค่าสต็อกรวมแยกตามหมวดหมู่สินค้า"""
        if not self.products:
            return {
                "message": "ยังไม่มีข้อมูลสินค้าในระบบ",
                "categories": {},
                "total_value": 0.0
            }

        category_totals: dict[str, float] = {}
        total_value = 0.0

        for product in self.products.values():
            category_name = product.category.name
            value = product.quantity * product.price
            
            category_totals[category_name] = category_totals.get(category_name, 0.0) + value
            total_value += value

        return {
            "message": "รายงานมูลค่าสต็อก",
            "categories": category_totals,
            "total_value": total_value
        }

    def set_product_threshold(self, product_id: str, threshold: int) -> None:
        """ตั้งค่า Threshold ใหม่ให้สินค้าเฉพาะรายการ"""
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")
        
        self.products[product_id].threshold = threshold        
