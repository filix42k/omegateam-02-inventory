# Design Review — SOLID

> เป็นร่างวิเคราะห์ที่ Codex ช่วยเตรียมตามคำขอผู้ใช้ เพื่อให้ผู้เรียนตรวจและอธิบายด้วยตนเองก่อนส่ง. ใบงาน Lab 3 กำหนดให้ขั้นนี้ทำเองโดยไม่ใช้ AI.

| หลัก | ละเมิดหรือไม่ | จุดที่เกี่ยวข้อง | เหตุผลและผลกระทบ | ข้อเสนอ |
|---|---|---|---|---|
| S (SRP) | ยังไม่พบการละเมิดชัดเจนในขอบเขต Lab | `InventoryService` use-case methods; `Notifier` classes | Service ประสาน inventory use cases และ delegates printing ไป notifier. หาก report/stock workflow โตขึ้น อาจมีหลายเหตุผลในการเปลี่ยน service. | คง notifier แยก; แยก report service เมื่อมีความต้องการรายงานเพิ่มขึ้นจริง |
| O (OCP) | ผ่านสำหรับการเพิ่มช่องทาง | `NotifierFactory.register_notifier`, `InventoryService.observers` | ลงทะเบียน notifier ใหม่และ inject ด้วย channel ได้ โดยไม่เพิ่ม if/elif ใน service. | เขียน test ว่า notifier ใหม่ register ได้และรับแจ้งตาม channel |
| L (LSP) | ผ่าน | `EmailNotifier`, `SMSNotifier` implement `Notifier` | ทั้งคู่รับ message และคืน None ตาม contract จึงใช้แทนกันได้. | รักษา contract เดียวและเพิ่ม contract test เมื่อมี notifier ใหม่ |
| I (ISP) | ผ่าน | `Notifier` protocol | Protocol มี method เดียว `notify`; implementer ไม่ถูกบังคับ method ที่ไม่ใช้. | แยก protocol เพิ่มเฉพาะเมื่อเกิด client ที่ต้องการ operation คนละชุด |
| D (DIP) | ผ่าน | `InventoryService.__init__`, import `Notifier` | Service รับ mapping ของ abstraction `Notifier` ผ่าน constructor; ไม่ import concrete Email/SMS class. | สร้าง concrete notifiers ใน composition root แล้ว inject เข้า service |

## ประเด็นที่ตรวจพบใน implementation ก่อนปรับ
- `inventory_no_context.py` สร้าง `EmailNotifier`/`SMSNotifier` ผ่าน factory ใน business class จึงผูกกับ factory โดยตรงและเพิ่มช่องทางใหม่ต้องแก้ class เดิม
- เวอร์ชันเก่าของ `service.py` รับ observer เป็น list และแจ้งทุก observer จึงเลือก Email/SMS ต่อสินค้าไม่ได้
- ตารางเดิม `Design_review.md` จัดการตรวจข้อมูลเป็นการละเมิด ISP ซึ่งไม่ตรงความหมายของ ISP
