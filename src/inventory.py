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
        with open(filename, "r", encoding="utf-8") as file:
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


import unicodedata


def _pad_str(text, width, align="left"):
    """จัดระยะห่างข้อความภาษาไทยโดยชดเชยความกว้างสระบน/ล่าง/วรรณยุกต์"""
    display_len = sum(1 for c in str(text) if unicodedata.category(c) != "Mn")
    pad_len = max(0, width - display_len)
    if align == "right":
        return " " * pad_len + str(text)
    return str(text) + " " * pad_len


# [US-01] Task-02: เขียนฟังก์ชันแสดงรายการสินค้าตามเงื่อนไข AC-1 และ AC-2 (Assignee: Mik-kaewwichian)
def list_items(items):
    """แสดงรายการสินค้าทั้งหมดพร้อมจำนวนคงเหลือ"""
    if not items:
        print("\nยังไม่มีสินค้าในระบบ")
        return

    print(f"\n{_pad_str('รหัส', 12)} {_pad_str('ชื่อสินค้า', 25)} {_pad_str('จำนวนคงเหลือ', 12, 'right')}")
    print("-" * 52)

    for item in items:
        code = item.get("code", "-")
        name = item.get("name", "-")
        quantity = item.get("quantity", 0)
        print(f"{_pad_str(code, 12)} {_pad_str(name, 25)} {_pad_str(quantity, 12, 'right')}")


# [US-02] Task-03 & Task-04: ตรวจสอบ Validation รหัสซ้ำ และเพิ่มสินค้า (Assignee: Phongsakhon870, chinchanoknantpromsri)
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