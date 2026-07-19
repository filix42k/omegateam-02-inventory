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


def save_all_items(items):
    """ฟังก์ชันช่วยสำหรับเขียนข้อมูลทั้งหมดลงไฟล์ JSON"""
    with open(DB_FILE, 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=4)


def list_items():
    """แสดงรายการสินค้าทั้งหมด"""
    items = load_items()

    if not items:
        print("ยังไม่มีสินค้าในระบบ")
        return

    print("📋 รายการสินค้าทั้งหมดในระบบ:")
    for item in items:
        print(f"รหัส: {item['id']} | ชื่อ: {item['name']} | จำนวนคงเหลือ: {item['quantity']}")


# ==========================================
# เพิ่มฟังก์ชันใหม่ตาม Task-04 (AC-1 & AC-2)
# ==========================================

def save_item(new_item):
    """
    บันทึกสินค้าใหม่ลงระบบ โดยทำการตรวจสอบรหัสซ้ำก่อนบันทึก
    """
    items = load_items()
    
    # AC-2: เช็กว่ามีรหัสสินค้า (id) นี้อยู่ในระบบแล้วหรือยัง
    for item in items:
        if item['id'] == new_item['id']:
            print("รหัสสินค้าซ้ำ")  # แสดงข้อความปฏิเสธตาม AC-2 โดยไม่เขียนทับข้อมูลเดิม
            return False
            
    # AC-1: หากไม่ซ้ำ บันทึกสินค้าใหม่ลงระบบ
    items.append(new_item)
    save_all_items(items)
    print(f"✅ เพิ่มสินค้า '{new_item['name']}' เรียบร้อยแล้ว")
    return True


# ==========================================
# เพิ่มฟังก์ชันใหม่ตาม Task-05 ค้นหาและอัปเดตยอดคงเหลือ N + Input
# ==========================================

def update_balance(item_id, n):
    """
    ค้นหาสินค้าจาก id และอัปเดตยอดคงเหลือตามจำนวน n 
    (n เป็นบวก = เพิ่มสต็อก, n เป็นลบ = ลดสต็อก)
    """
    items = load_items()
    is_found = False

    for item in items:
        if item['id'] == item_id:
            # คำนวณยอดคงเหลือใหม่
            new_quantity = item['quantity'] + n
            
            # ป้องกันไม่ให้ยอดคงเหลือติดลบ (Optional)
            if new_quantity < 0:
                print(f"⚠️ ยอดคงเหลือไม่เพียงพอ (คงเหลือ: {item['quantity']}, ต้องการลด: {abs(n)})")
                return False
                
            item['quantity'] = new_quantity
            is_found = True
            print(f"🔄 อัปเดต '{item['name']}' สำเร็จ (ยอดคงเหลือใหม่: {item['quantity']})")
            break

    if is_found:
        save_all_items(items)
        return True
    else:
        print(f"❌ ไม่พบสินค้า รหัส {item_id} ในระบบ")
        return False


# ทดสอบการทำงานเมื่อรันไฟล์นี้โดยตรง
if __name__ == "__main__":
    print("--- [เตรียมระบบ] รีเซ็ตไฟล์ database สำหรับทดสอบ ---")
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    create_initial_db() # จะได้รหัส 1 และ 2 มาเริ่มต้น
    
    print("\n" + "="*40 + "\n")

    print("--- ทดสอบ AC-1 (เพิ่มสินค้าใหม่ที่รหัสไม่ซ้ำ) ---")
    item_new = {
        "id": 3,
        "name": "Gaming Headset",
        "category": "Electronics",
        "price": 2500.00,
        "quantity": 10
    }
    save_item(item_new)
    list_items() # ควรจะเห็นรหัส 3 เพิ่มเข้ามาด้วย

    print("\n" + "-"*40 + "\n")

    print("--- ทดสอบ AC-2 (เพิ่มสินค้าด้วยรหัสเดิมที่ซ้ำ) ---")
    item_duplicate = {
        "id": 1, # รหัส 1 ซ้ำกับ Mechanical Keyboard
        "name": "Wireless Charger",
        "category": "Electronics",
        "price": 990.00,
        "quantity": 5
    }
    save_item(item_duplicate) # ควรขึ้นว่า "รหัสสินค้าซ้ำ" และไม่บันทึก
    
    print("\n" + "="*40 + "\n")

    print("--- ทดสอบ Task-05 (อัปเดตยอดคงเหลือ) ---")
    # ทดสอบ 1: เพิ่มยอดคงเหลือ 5 ชิ้น ให้กับรหัส 1
    print("[1] เพิ่มจำนวนสินค้า รหัส 1 อีก 5 ชิ้น")
    update_balance(1, 5)

    # ทดสอบ 2: ลดยอดคงเหลือ 10 ชิ้น จากรหัส 2
    print("\n[2] ลดจำนวนสินค้า รหัส 2 ลง 10 ชิ้น")
    update_balance(2, -10)
    
    # ทดสอบ 3: ลองลดจำนวนสินค้าจนติดลบ (เพื่อทดสอบการดักจับข้อผิดพลาด)
    print("\n[3] ลองลดจำนวนสินค้า รหัส 3 ลง 20 ชิ้น (เกินสต็อกที่มี)")
    update_balance(3, -20)

    # ทดสอบ 4: อัปเดตสินค้าที่ไม่มีในระบบ
    print("\n[4] อัปเดตสินค้า รหัส 99 ที่ไม่มีในระบบ")
    update_balance(99, 10)

    print("\n--- ตรวจสอบข้อมูลในระบบอีกครั้งหลังจากทำการอัปเดต ---")
    list_items()