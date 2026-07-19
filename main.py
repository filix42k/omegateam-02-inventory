import inventory


# [US-02] Task-03: เขียนฟังก์ชันรับค่าอินพุตและตรวจสอบ Validation เบื้องต้น (Assignee: Phongsakhon870)
def _read_int(prompt_text):
    while True:
        raw_value = input(prompt_text).strip()
        try:
            return int(raw_value)
        except ValueError:
            print("ขัดข้อง: กรุณากรอกจำนวนเป็นตัวเลขจำนวนเต็ม")


def main_menu():
    inventory.create_initial_db()
    items_list = inventory.load_items()

    while True:
        print("\n=== ระบบจัดการสต็อกร้านเครื่องเขียน (Omega Team) ===")
        print("1. ดูรายการสินค้าทั้งหมด")
        print("2. เพิ่มสินค้าใหม่")
        print("3. รับสินค้าเข้าสต็อก")
        print("4. จ่ายสินค้าออกสต็อก")
        print("0. ออกจากโปรแกรม")

        choice = input("กรุณาเลือกเมนู (0-4): ").strip()

        if choice == "1":
            # [US-01] Task-02: ดึงรายการสินค้ามาแสดงผล (Assignee: Mik-kaewwichian)
            items_list = inventory.load_items()
            inventory.list_items(items_list)

        elif choice == "2":
            # [US-02] Task-03 & Task-04: รับข้อมูลสินค้าใหม่และบันทึกลงระบบ (Assignee: Phongsakhon870, chinchanoknantpromsri)
            print("\n--- เพิ่มสินค้าใหม่ ---")
            code = input("กรอกรหัสสินค้า: ").strip()
            name = input("กรอกชื่อสินค้า: ").strip()
            quantity = _read_int("กรอกจำนวนสินค้าเริ่มต้น: ")
            items_list = inventory.load_items()
            inventory.add_item(items_list, code, name, quantity)

        elif choice == "3":
            # [US-03] Task-05: รับสินค้าเข้าสต็อก (Assignee: poom24052549-prog)
            print("\n--- รับสินค้าเข้าสต็อก ---")
            code = input("กรอกรหัสสินค้าที่ต้องการรับเข้า: ").strip()
            quantity = _read_int("กรอกจำนวนที่รับเข้า: ")
            items_list = inventory.load_items()
            inventory.receive_stock(items_list, code, quantity)

        elif choice == "4":
            # [US-03] Task-06: จ่ายสินค้าออกสต็อกและเช็กยอด (Assignee: filix42k)
            print("\n--- จ่ายสินค้าออกสต็อก ---")
            code = input("กรอกรหัสสินค้าที่ต้องการจ่ายออก: ").strip()
            quantity = _read_int("กรอกจำนวนที่จ่ายออก: ")
            items_list = inventory.load_items()
            inventory.issue_stock(items_list, code, quantity)

        elif choice == "0":
            print("ปิดโปรแกรมระบบสต็อก สวัสดีครับ")
            break

        else:
            print("เลือกเมนูไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")


if __name__ == "__main__":
    main_menu()