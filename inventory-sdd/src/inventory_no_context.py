from abc import ABC, abstractmethod

# 1. สร้าง Notifier Interface และคลาสลูก (ตาม NFR-02 และ Design Notes)
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class EmailNotifier(Notifier):
    def send(self, message: str):
        print(f"[Email] {message}")

class SMSNotifier(Notifier):
    def send(self, message: str):
        print(f"[SMS] {message}")

class NotifierFactory:
    @staticmethod
    def get_notifiers(channels: list[str]) -> list[Notifier]:
        notifiers = []
        if "Email" in channels:
            notifiers.append(EmailNotifier())
        if "SMS" in channels:
            notifiers.append(SMSNotifier())
        return notifiers

# 2. โมเดลสินค้า (ครอบคลุม US-04, US-05 Default Config)
class Product:
    def __init__(self, name: str, stock: int = 0, threshold: int = 0, channels: list[str] = None):
        self.name = name
        self.stock = stock
        self.threshold = threshold
        self.channels = channels or ["Email"]

# 3. บริการจัดการสต็อก (ครอบคลุม US-01, US-02)
class InventoryService:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product):
        self.products[product.name] = product

    def dispatch_stock(self, name: str, qty: int):
        if qty <= 0:
            raise ValueError("จำนวนสินค้าต้องมากกว่า 0")
        if name not in self.products:
            raise ValueError("ไม่พบข้อมูลสินค้านี้ในระบบ")
            
        product = self.products[name]
        if product.stock < qty:
            raise ValueError("จำนวนคงเหลือไม่พอ")

        old_stock = product.stock
        product.stock -= qty

        # ตรวจสอบการแจ้งเตือน (ส่งเมื่อสถานะเปลี่ยนจาก >= เป็น < threshold เท่านั้น)
        if old_stock >= product.threshold and product.stock < product.threshold:
            self._notify_low_stock(product)

    def _notify_low_stock(self, product: Product):
        message = f"แจ้งเตือน: สินค้า '{product.name}' สต็อกต่ำกว่ากำหนด (คงเหลือ {product.stock})"
        notifiers = NotifierFactory.get_notifiers(product.channels)
        for notifier in notifiers:
            notifier.send(message)