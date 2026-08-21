# AI_ITERATION_LOG.md

**Date:** 2026-08-21
**Topic:** Code Review & Refactoring Opportunities (ฟีเจอร์แจ้งเตือนสต็อกต่ำ)
**Reviewer:** Senior Software Engineer / AI Assistant

## 🚩 Issues Found (จุดที่ต้องปรับปรุง)

จากการรีวิวโค้ด Python เบื้องต้น พบปัญหาด้านการออกแบบที่ควรได้รับการ Refactor ใน Sprint ถัดไป ดังนี้:

### 1. Type Hints ยังไม่ครอบคลุม (Missing/Incomplete Type Hints)
- **ปัญหา:** แม้จะมีการใช้ Type Hint บ้าง (เช่น `message: str`) แต่ยังขาดความเข้มงวดในหลายจุด เช่น ไม่มี Return Type (`-> None`) ในเมธอด `add_product` หรือ `dispatch_stock` 
- **ผลกระทบ:** ทำให้ IDE หรือเครื่องมืออย่าง `mypy` ไม่สามารถตรวจสอบ Type ได้เต็มประสิทธิภาพ เพิ่มความเสี่ยงในการเกิด Runtime Error
- **แนวทางแก้ไข:** เติม Type Hints ให้ครบทุกฟังก์ชันและเมธอด รวมถึงพิจารณาใช้ `dataclass` หรือ `Pydantic` สำหรับ Model (`Product`) เพื่อการทำ Data Validation ที่ดีขึ้น

### 2. การรวมทุกอย่าง (Coupling / SRP Violation)
- **ปัญหา:** โค้ดปัจจุบันรวมเอา Class ทั้งหมด (`Product`, `InventoryService`, `Notifier`) ไว้ในที่เดียวกัน และ `InventoryService` ยังต้องรับภาระเรียกใช้ `NotifierFactory` โดยตรง (Tight Coupling)
- **ผลกระทบ:** ขัดกับหลัก Single Responsibility Principle (SRP) หากอนาคตระบบแจ้งเตือนมีความซับซ้อนขึ้น จะทำให้ไฟล์คลังสินค้าบวมและแก้ไขยาก (God Object)
- **แนวทางแก้ไข:** 
  - แยกไฟล์ออกเป็น Module ชัดเจน เช่น `models.py`, `services.py`, `notifications.py`
  - ควรเปลี่ยนไปใช้ **Event-Driven Architecture** หรือ **Observer Pattern** (เช่น เมื่อสต็อกต่ำ `InventoryService` แค่โยน Event `LowStockEvent` ออกไป ส่วนระบบ Notification ค่อยคอยดักฟังและทำงานต่อเอง)

### 3. Hardcode ข้อมูลปลายทาง (Missing Contact Information)
- **ปัญหา:** ระบบรู้ว่าต้องส่งแจ้งเตือนผ่านช่องทางไหน (เช่น `"Email"`, `"SMS"`) แต่กลับ **ไม่มีการเก็บข้อมูลปลายทาง** (เช่น อีเมล `manager@company.com` หรือเบอร์โทรศัพท์ `081-xxx-xxxx`) 
- **ผลกระทบ:** ในโลกความเป็นจริง ระบบจะไม่สามารถส่งแจ้งเตือนได้เลย เพราะไม่มี Address ปลายทาง
- **แนวทางแก้ไข:** ต้องแก้ Spec และ Model โดยอาจจะต้องมีคลาส `ManagerProfile` เพื่อเก็บเบอร์โทรและอีเมล หรือเพิ่มฟิลด์ `notification_contacts` เข้าไปในระบบตั้งค่า 

---
**Next Action:** 
- [ ] สร้าง Ticket/Task เพื่อ Refactor โค้ดให้แยก Module
- [ ] อัปเดต Acceptance Criteria (AC) ใน US-05 เพื่อระบุให้ชัดเจนว่าผู้จัดการต้องกรอกอีเมล/เบอร์โทรด้วย

| ประเด็น | ก่อนมี context (ขั้นที่ 4) | หลังมี context (ขั้นที่ 6) |
| :--- | :--- | :--- |
| **แยกไฟล์/ความรับผิดชอบ** | มักจะเขียนคลาสและ Business Logic ทั้งหมดรวมกันไว้ในไฟล์เดียวเพื่อให้โค้ดรันได้ง่ายที่สุด | แยกส่วนประกอบเป็น 3 ไฟล์อย่างชัดเจน (`models.py`, `notifiers.py`, `service.py`) ตามหลักการ SRP และกฎที่กำหนด |
| **type hint + docstring** | อาจมีการใช้ type hint แค่บางส่วน และ docstring มักจะเป็นภาษาอังกฤษหรือไม่มีเลย | บังคับใช้ type hint ทุก function signature และมี docstring เป็นภาษาไทยในทุก public method ครบถ้วน |
| **service ผูกกับ notifier ตรง ๆ หรือไม่** | `InventoryService` มักจะเรียกสร้างอินสแตนซ์และใช้งาน `EmailNotifier` หรือ `SMSNotifier` โดยตรง (Tight Coupling) | ไม่ผูกติดกันตรง ๆ โดย `InventoryService` จะเรียกผ่าน Abstraction (Protocol) และใช้ `NotifierFactory` สร้างให้แทน (ตามหลัก DIP/OCP) |
| **hardcode config หรือไม่** | มักจะระบุอีเมล เบอร์โทร หรือค่า Threshold ฝังไว้ในเมธอดของ Business Logic โดยตรง | ไม่มีการ hardcode ข้อมูลเหล่านี้ในลอจิก แต่ใช้วิธีรับค่าผ่าน Constructor (Dependency Injection) |