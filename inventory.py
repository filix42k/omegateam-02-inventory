import json
import os

DB_FILE = 'items.json'

def create_initial_db():
    """สร้างไฟล์ items.json พร้อมข้อมูลเริ่มต้น หากยังไม่มีไฟล์"""
    if not os.path.exists(DB_FILE):
        initial_items = [
            {
                "id": 1,
                "name": "Mechanical Keyboard",
                "category": "Electronics",
                "price": 3200.00,
                "quantity": 15
            },
            {
                "id": 2,
                "name": "Ergonomic Mouse",
                "category": "Electronics",
                "price": 1850.50,
                "quantity": 30
            }
        ]

        # เขียนข้อมูลลงไฟล์ JSON
        with open(DB_FILE, 'w', encoding='utf-8') as file:
            json.dump(initial_items, file, ensure_ascii=False, indent=4)
        print(f"✅ สร้างไฟล์ {DB_FILE} สำเร็จ")
    else:
        print(f"ℹ️ ไฟล์ {DB_FILE} มีอยู่แล้ว")


def load_items():
    """อ่านข้อมูลสินค้าทั้งหมดจากไฟล์ JSON"""
    if not os.path.exists(DB_FILE):
        return []

    with open(DB_FILE, 'r', encoding='utf-8') as file:
        items = json.load(file)
        return items


def list_items():
    """แสดงรายการสินค้าตามเงื่อนไข AC-1 และ AC-2"""
    items = load_items()

    # AC-2: Given ยังไม่มีสินค้าในระบบ | When เรียกคำสั่ง list | Then แสดงข้อความ "ยังไม่มีสินค้าในระบบ"
    if not items:
        print("ยังไม่มีสินค้าในระบบ")
        return

    # AC-1: Given มีสินค้าอย่างน้อย 1 รายการ | When เรียกคำสั่ง list | Then แสดงชื่อ รหัส และจำนวนคงเหลือครบทุกรายการ
    print("📋 รายการสินค้าทั้งหมดในระบบ:")
    for item in items:
        print(f"รหัส: {item['id']} | ชื่อ: {item['name']} | จำนวนคงเหลือ: {item['quantity']}")


# ทดสอบการทำงานเมื่อรันไฟล์นี้โดยตรง
if __name__ == "__main__":
    print("--- ทดสอบ AC-1 (มีสินค้าในระบบ) ---")
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    create_initial_db()  # สร้างไฟล์พร้อมข้อมูลเริ่มต้น 2 รายการ
    list_items()

    print("\n" + "-"*40 + "\n")

    print("--- ทดสอบ AC-2 (ไม่มีสินค้าในระบบ) ---")
    # จำลองสถานการณ์โดยการเคลียร์ข้อมูลในไฟล์ให้เป็นลิสต์ว่าง []
    with open(DB_FILE, 'w', encoding='utf-8') as file:
        json.dump([], file, ensure_ascii=False, indent=4)

    list_items()