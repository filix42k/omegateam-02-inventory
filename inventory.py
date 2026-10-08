import json
import os

DATA_FILE = "items.json"


# [US-01] Task-01: สร้างไฟล์ฐานข้อมูลเริ่มต้น items.json แบบว่างเพื่อรองรับสถานะไม่มีสินค้า
def create_initial_db(filename=DATA_FILE):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)


# Task: เขียนฟังก์ชัน load_items() อ่านข้อมูลจากไฟล์ JSON (อ้างอิง Issue #4)
def load_items(filename=DATA_FILE):
    """อ่านข้อมูลสินค้าจากไฟล์ JSON และคืนค่าเป็น list"""
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, encoding="utf-8") as file:
            items = json.load(file)

        if isinstance(items, list):
            return items

        return []
    except (json.JSONDecodeError, OSError):
        return []


# Task: ฟังก์ชันบันทึกข้อมูลสินค้าลงในไฟล์ JSON
def save_items(items, filename=DATA_FILE):
    """บันทึกข้อมูลสินค้าลงในไฟล์ JSON"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=4)


# [US-01] Task-02: เขียนฟังก์ชันแสดงรายการสินค้าตามเงื่อนไข AC-1 และ AC-2 (Assignee: Mik-kaewwichian)
def list_items(items):
    """แสดงรายการสินค้าทั้งหมดพร้อมจำนวนคงเหลือ"""
    if not items:
        print("ยังไม่มีสินค้าในระบบ")
        return

    print(f"{'รหัส':<12} {'ชื่อสินค้า':<25} {'จำนวนคงเหลือ':>12}")
    print("-" * 52)

    for item in items:
        code = item.get("code", "-")
        name = item.get("name", "-")
        quantity = item.get("quantity", 0)
        print(f"{code:<12} {name:<25} {quantity:>12}")


# [US-02] Task-03 & Task-04: ตรวจสอบ Validation รหัสซ้ำ และเพิ่มสินค้า
# Assignee: Phongsakhon870, chinchanoknantpromsri
def add_item(items, code, name, quantity, filename=DATA_FILE):
    """เพิ่มสินค้าใหม่ โดยตรวจสอบรหัสซ้ำและจำนวนติดลบ"""
    code = code.strip()
    name = name.strip()

    if not code:
        print("กรุณากรอกรหัสสินค้า")
        return None

    if not name:
        print("กรุณากรอกชื่อสินค้า")
        return None

    duplicate = any(item.get("code") == code for item in items)

    if duplicate:
        print("รหัสสินค้าซ้ำ")
        return None

    if quantity < 0:
        print("จำนวนสินค้าต้องไม่ติดลบ")
        return None

    new_item = {
        "code": code,
        "name": name,
        "quantity": quantity,
    }

    items.append(new_item)
    save_items(items, filename)
    return new_item


# [US-03] Task-05: เขียนฟังก์ชันค้นหาและอัปเดตยอดคงเหลือ N + Input (Assignee: poom24052549-prog)
def receive_stock(items, code, quantity, filename=DATA_FILE):
    """รับสินค้าเข้าและบันทึกจำนวนคงเหลือใหม่"""
    if quantity < 0:
        print("จำนวนรับเข้าต้องไม่ติดลบ")
        return None

    for item in items:
        if item.get("code") == code:
            item["quantity"] = item.get("quantity", 0) + quantity
            save_items(items, filename)
            return item

    print("ไม่พบสินค้า")
    return None


# [US-03] Task-06: เขียนระบบตรวจสอบเงื่อนไขไม่ให้จ่ายออกมากกว่าคงเหลือ (Assignee: filix42k)
def issue_stock(items, code, quantity, filename=DATA_FILE):
    """จ่ายสินค้าออกโดยป้องกันจำนวนคงเหลือติดลบ"""
    if quantity < 0:
        print("จำนวนจ่ายออกต้องไม่ติดลบ")
        return None

    for item in items:
        if item.get("code") == code:
            current_quantity = item.get("quantity", 0)

            if quantity > current_quantity:
                print("จำนวนคงเหลือไม่พอ")
                return None

            item["quantity"] = current_quantity - quantity
            save_items(items, filename)
            return item

    print("ไม่พบสินค้า")
    return None


class InventoryItem:
    def __init__(self, name: str, quantity: int, price: float):
        if not name or not name.strip():
            raise ValueError("ชื่อสินค้าต้องไม่ว่างเปล่า")
        if quantity < 0:
            raise ValueError("จำนวนสินค้าต้องไม่ติดลบ")
        if price <= 0:
            raise ValueError("ราคาต้องมากกว่าศูนย์")
        self.name = name.strip()
        self.quantity = quantity
        self.price = price


class Inventory:
    def __init__(self):
        self._items: dict[str, InventoryItem] = {}

    def add_item(self, name: str, quantity: int, price: float) -> InventoryItem:
        """เพิ่มสินค้าใหม่ ถ้าชื่อซ้ำให้ raise ValueError"""
        if name in self._items:
            raise ValueError(f"สินค้า '{name}' มีอยู่ในระบบแล้ว")
        item = InventoryItem(name, quantity, price)
        self._items[item.name] = item
        return item

    def restock(self, name: str, amount: int) -> int:
        """เพิ่มจำนวนสินค้าที่มีอยู่ คืนค่าจำนวนหลังเติม"""
        if name not in self._items:
            raise KeyError(f"ไม่พบสินค้า '{name}' ในระบบ")
        if amount <= 0:
            raise ValueError("จำนวนที่เติมต้องมากกว่าศูนย์")
        self._items[name].quantity += amount
        return self._items[name].quantity

    def sell(self, name: str, amount: int) -> int:
        """ขายสินค้า ลดจำนวน คืนค่าจำนวนคงเหลือ"""
        if name not in self._items:
            raise KeyError(f"ไม่พบสินค้า '{name}' ในระบบ")
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise TypeError("quantity must be an integer")
        if amount <= 0:
            raise ValueError("จำนวนที่ขายต้องมากกว่าศูนย์")
        if self._items[name].quantity < amount:
            raise ValueError(
                f"สินค้า '{name}' คงเหลือ {self._items[name].quantity} ชิ้น "
                f"ไม่เพียงพอสำหรับการขาย {amount} ชิ้น"
            )
        self._items[name].quantity -= amount
        return self._items[name].quantity

    def low_stock_items(self, threshold: int) -> list[InventoryItem]:
        """คืนสินค้าที่มีจำนวนไม่เกิน threshold โดยเรียงชื่อตามตัวอักษร"""
        matching_items = [
            item for item in self._items.values() if item.quantity <= threshold
        ]
        return sorted(matching_items, key=lambda item: item.name)

    def get_total_value(self) -> float:
        """คำนวณมูลค่ารวมของสินค้าทั้งหมดในคลัง"""
        return sum(item.quantity * item.price for item in self._items.values())
