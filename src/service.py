from typing import Dict, Any, List
from src.models import Product, StockTransaction
from src.notifiers import NotifierFactory

class InventoryService:
    def __init__(self, admin_contacts: Dict[str, str]):
        """
        รับค่า dependencies เริ่มต้นผ่าน Constructor
        :param admin_contacts: ดิกชันนารีเก็บข้อมูลปลายทางสำหรับแจ้งเตือน 
                               เช่น {"email": "manager@company.com", "sms": "0812345678"}
        """
        self.products: Dict[str, Product] = {}
        self.transactions: List[StockTransaction] = []
        self.admin_contacts = admin_contacts

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าใหม่เข้าสู่ระบบ"""
        self.products[product.id] = product

    def receive_stock(self, product_id: str, quantity: int) -> None:
        """บันทึกรับสินค้าเข้าสต็อกและอัปเดตทันที"""
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")
        
        product = self.products[product_id]
        product.quantity += quantity
        self.transactions.append(StockTransaction(product_id=product_id, transaction_type="in", quantity=quantity))

    def dispense_stock(self, product_id: str, quantity: int) -> None:
        """บันทึกจ่ายสินค้าออก ตรวจสอบจำนวนคงเหลือ และแจ้งเตือนหากต่ำกว่า Threshold"""
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")
        
        product = self.products[product_id]
        
        # ตรวจสอบว่าสินค้ามีพอจ่ายหรือไม่ หากไม่พอ Exception จะหยุดการทำงานก่อนเปลี่ยนแปลงสต็อก (NFR-03)
        if product.quantity < quantity:
            raise ValueError("จำนวนคงเหลือไม่พอ")
        
        product.quantity -= quantity
        self.transactions.append(StockTransaction(product_id=product_id, transaction_type="out", quantity=quantity))

        self._check_threshold_and_notify(product)

    def _check_threshold_and_notify(self, product: Product) -> None:
        """ตรวจสอบสถานะสต็อกและส่งแจ้งเตือนถ้าต่ำกว่ากำหนด"""
        if product.quantity < product.threshold:
            notifier = NotifierFactory.get_notifier(product.notifier_type)
            destination = self.admin_contacts.get(product.notifier_type, "Unknown Destination")
            message = f"แจ้งเตือนสต็อกต่ำ: สินค้า {product.name} คงเหลือ {product.quantity} (Threshold: {product.threshold})"
            
            notifier.send(message, destination)

    def get_stock_value_report(self) -> Dict[str, Any]:
        """คำนวณและคืนค่ารายงานมูลค่าสต็อกรวมแยกตามหมวดหมู่สินค้า"""
        if not self.products:
            return {
                "message": "ยังไม่มีข้อมูลสินค้าในระบบ",
                "categories": {},
                "total_value": 0.0
            }

        category_totals: Dict[str, float] = {}
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

    def set_product_notifier(self, product_id: str, notifier_type: str) -> None:
        """เลือกหรืออัปเดตช่องทางแจ้งเตือนเป็นรายสินค้า"""
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")
        
        # ตรวจสอบล่วงหน้าว่ามี Notification Type นี้ใน Factory หรือไม่
        NotifierFactory.get_notifier(notifier_type)
        self.products[product_id].notifier_type = notifier_type
        