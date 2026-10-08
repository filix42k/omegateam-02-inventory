"""ข้อมูลหลักของระบบคลังสินค้า Lab 3."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Category:
    """หมวดหมู่สินค้า."""

    name: str

    def __post_init__(self) -> None:
        """ตรวจว่าชื่อหมวดหมู่ไม่ว่าง."""
        if not self.name or not self.name.strip():
            raise ValueError("ชื่อหมวดหมู่ต้องไม่ว่างเปล่า")
        self.name = self.name.strip()


@dataclass
class Product:
    """ข้อมูลสินค้าและการตั้งค่ารายการนั้น."""

    id: str
    name: str
    category: Category
    price: float
    quantity: int = 0
    threshold: int = 0
    notification_channels: tuple[str, ...] = ("email",)

    def __post_init__(self) -> None:
        """ตรวจข้อมูลสินค้าและกำหนดช่องทางแจ้งเตือนเริ่มต้นเป็น Email."""
        if not self.id or not self.id.strip():
            raise ValueError("รหัสสินค้าต้องไม่ว่างเปล่า")
        if not self.name or not self.name.strip():
            raise ValueError("ชื่อสินค้าต้องไม่ว่างเปล่า")
        if self.price <= 0:
            raise ValueError("ราคาต้องมากกว่าศูนย์")
        if self.quantity < 0:
            raise ValueError("จำนวนสินค้าต้องไม่ติดลบ")
        if self.threshold < 0:
            raise ValueError("Threshold ไม่สามารถเป็นค่าติดลบได้")
        if not self.notification_channels:
            raise ValueError("ต้องเลือกช่องทางแจ้งเตือนอย่างน้อยหนึ่งช่องทาง")
        self.id = self.id.strip()
        self.name = self.name.strip()
        self.notification_channels = tuple(
            channel.strip().lower() for channel in self.notification_channels
        )


@dataclass
class StockTransaction:
    """รายการรับหรือจ่ายสินค้าพร้อมเวลาที่บันทึก."""

    product_id: str
    transaction_type: str
    quantity: int
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """ตรวจประเภทและจำนวนของรายการเคลื่อนไหว."""
        if self.transaction_type not in {"in", "out"}:
            raise ValueError("ประเภท transaction ต้องเป็น in หรือ out")
        if self.quantity <= 0:
            raise ValueError("จำนวนสินค้าต้องมากกว่า 0")
