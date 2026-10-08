# Prompt Engineering เทียบกับ Context Engineering

> ตัวอย่างเปรียบเทียบสร้างโดย Codex เมื่อ 8 ต.ค. 2569 สำหรับคำขอผู้ใช้. ผลรอบที่ 1 และ 2 เป็นข้อความตัวอย่างที่ AI สร้างในงานนี้ ไม่ใช่ผลจากบัญชี AI ภายนอกหรือการทดลองของนักศึกษา.

## รอบที่ 1 — prompt สั้น
Prompt ที่ส่ง: “เขียน function ลด stock”

ผลที่ AI สร้าง:
```python
def reduce_stock(quantity, amount):
    return quantity - amount
```
ข้อสังเกตจากผลนี้: ไม่มีการตรวจ amount มากกว่า 0, ไม่เช็ก stock พอหรือไม่, ไม่คืน error ตาม interface เดิม และไม่ชัดว่า input เป็น inventory ไหน

## รอบที่ 2 — prompt พร้อม context
Prompt ที่ส่ง: “เพิ่มเมธอด `sell_many(orders: dict[str, int]) -> dict[str, int]` ให้ `Inventory` โดยรักษา interface เดิม ถ้าไม่พบสินค้าให้ raise `KeyError` ถ้าจำนวนไม่มากกว่า 0 หรือ stock ไม่พอให้ raise `ValueError`. การขายต้อง atomic: ถ้ามีรายการใดไม่ผ่าน validation ห้ามเปลี่ยน stock ของรายการใดเลย. ห้ามใช้ library ภายนอก. ใช้โค้ด `inventory.py` ที่แนบ และให้ผลผ่านเกณฑ์ด้านล่าง.”

Context ที่แนบ: เนื้อหาทั้งไฟล์ `inventory.py` ในโฟลเดอร์นี้. ไฟล์กำหนด `Inventory`, `InventoryItem`, `sell`, exception เดิม และวิธีเก็บ `_items`.

เกณฑ์ที่แนบ:
- A=10, B=5; ขาย A=2, B=3 ต้องคืนยอด A=8, B=2
- A=10, B=2; ขาย A=3, B=5 ต้อง raise `ValueError` และยอดทั้งคู่ไม่เปลี่ยน
- สินค้าไม่มีอยู่ต้อง `KeyError` และ stock ที่มีอยู่ไม่เปลี่ยน
- amount เป็นศูนย์หรือติดลบต้อง `ValueError`

ผลที่ AI สร้างในรอบนี้ (ตัวอย่าง implementation):
```python
def sell_many(self, orders: dict[str, int]) -> dict[str, int]:
    # ตรวจทั้งหมดก่อนแตะ stock เพื่อคง atomicity
    for name, amount in orders.items():
        if name not in self._items:
            raise KeyError(f"ไม่พบสินค้า '{name}' ในระบบ")
        if amount <= 0:
            raise ValueError("จำนวนที่ขายต้องมากกว่าศูนย์")
        if self._items[name].quantity < amount:
            raise ValueError(f"สินค้า '{name}' มี stock ไม่เพียงพอ")
    # validation ผ่านทุกตัวแล้ว จึงหักยอด
    result = {}
    for name, amount in orders.items():
        self._items[name].quantity -= amount
        result[name] = self._items[name].quantity
    return result
```

## เปรียบเทียบจากผลที่สร้าง
| ประเด็น | รอบ 1 | รอบ 2 |
|---|---|---|
| ยึด interface เดิม | ไม่ทราบเจ้าของ stock | เพิ่มบน `Inventory` และใช้ `_items`/exception ที่มีอยู่ |
| validation | ไม่มี | ตรวจชื่อ จำนวน และ stock |
| หลายรายการ | ไม่มีแนวคิด batch | ตรวจครบก่อนแก้ ทำให้ error ไม่ทิ้ง stock บางส่วน |
| ข้อจำกัด | ไม่กำหนด | ห้าม dependency ภายนอก พร้อม test cases |

สรุป: prompt รอบสองยาวขึ้นเพราะแนบ interface, requirement เชิงขอบเขต และเกณฑ์ตรวจ ผลลัพธ์จึงตอบโจทย์ชัดกว่า แต่ implementation ที่ AI สร้างยังต้องทดสอบจริง รวมกรณี duplicate key และ concurrency ก่อนใช้.
