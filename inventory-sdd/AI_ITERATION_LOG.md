# AI Iteration Log — Lab 3

> บันทึกนี้รวมสถานะจาก artifact เดิมของทีมและการแก้ใน `inventory-sdd/` ตามคำขอปัจจุบัน. รายการที่เขียนว่า reconstructed เป็นการสรุปย้อนหลังจากไฟล์ เพราะ repository เดิมไม่ได้เก็บ prompt เต็มไว้. การแก้ในรอบปัจจุบันใช้ Codex desktop; ไม่ได้ยืนยันสถานะค่าใช้จ่าย/สิทธิ์ว่าเป็นช่องทางฟรีตามใบงาน.

## ก่อนมี context: implementation เดิม
ไฟล์อ้างอิง: `src/inventory_no_context.py` (คัดจากโค้ดทีมที่มีอยู่)

Prompt ที่คาดจาก artifact เดิม (reconstructed; raw prompt ไม่อยู่ใน repository): “จาก spec นี้ ช่วยเขียนโค้ด Python สำหรับฟีเจอร์แจ้งเตือนสต็อกต่ำ”

| ประเด็น | ก่อนมี context: `inventory_no_context.py` | หลังมี context: `src/models.py`, `src/notifiers.py`, `src/service.py` |
|---|---|---|
| แยกไฟล์และหน้าที่ | รวม notifier, factory, product และ service ในไฟล์เดียว | แยก model, notifier/factory, service |
| Type hint / docstring | ไม่ครอบคลุม; public methods หลายตัวไม่มี docstring | type hints และ docstring ภาษาไทยใน public methods |
| Service ผูกกับ notifier | สร้าง NotifierFactory และ concrete notifier จาก service | รับ `Notifier` ตาม channel ผ่าน constructor |
| hard-code config | default/config อยู่กับ model และ factory | destination รับจาก caller; ไม่มี address จริงฝังใน business logic |
| Spec coverage | ไม่มี report/category และ threshold/channel setter ตาม user story ครบ | report แยกหมวด, threshold และ channel ตั้งค่ารายสินค้า |

## Iteration 1 — ขอบเขต threshold (บันทึกเดิมของทีม)
- ผลที่ผิดตาม `AI_ITERATION_LOG.md` เดิม: boundary ของ stock เท่ากับ threshold ถูกตีความผิดใน implementation รอบก่อน
- สาเหตุที่บันทึกไว้: spec เดิมไม่มีตัวอย่าง equality boundary ชัดเจน
- แก้ต้นทาง: เพิ่ม scenario ว่า quantity == threshold ต้องไม่แจ้งเตือน และเขียน predicate เป็น transition `old >= threshold and new < threshold`
- ผลที่บันทึกไว้: implementation รุ่นถัดไปไม่แจ้งเตือนที่ขอบเท่ากัน; เดิมระบุ test `test_stock_equals_threshold_should_not_notify` ผ่าน
- ข้อจำกัดหลักฐาน: raw prompt, output รอบแรก และ test file ไม่ถูกเก็บใน repo ที่ตรวจครั้งนี้

## Iteration 2 — Notification mocking และรูปแบบข้อความ (บันทึกเดิมของทีม)
- ผลที่ผิดตาม log เดิม: รูปแบบข้อความไม่ตรงและมีแนวโน้มเชื่อมต่อระบบส่งจริง
- สาเหตุที่บันทึกไว้: context ไม่ระบุการห้าม network/external library และ template ที่ต้องใช้
- แก้ต้นทาง: เพิ่มกฎให้ใช้ `print()` เท่านั้น และรูปแบบ `[Email]`/`[SMS] To: ...`
- ผลที่บันทึกไว้: notifier ใช้ print และ log เดิมระบุ unit test Email/SMS ผ่าน
- ข้อจำกัดหลักฐาน: raw prompt, test file และชื่อ AI platform ไม่ถูกบันทึกใน repo เดิม

## Iteration 3 — ทำ implementation ให้ตรงกับ spec ปัจจุบัน (รอบงานนี้)
- AI platform/channel: Codex desktop ใน workspace นี้. ไม่ยืนยันว่าเข้าเงื่อนไขเครื่องมือฟรีของรายวิชา
- คำสั่งผู้ใช้จริง: “ทำlab3ให้ครบ”. Prompt นี้ไม่ได้ระบุราย requirement แยกกัน; Codex ใช้ spec, rules, source code และ acceptance criteria ด้านล่างเป็น context ในการวางแผนการแก้ ไม่ควรอ้าง prompt ที่ร่างขึ้นภายหลังว่าเป็น raw prompt ที่ผู้ใช้ส่ง
- Context ที่แนบ/ใช้: `specs/spec.md`, `.ai-rules.md`, `src/inventory_no_context.py`, โมดูล models/notifiers/service ที่มีอยู่ และ acceptance criteria ใน Lab 3
- ปัญหาที่พบจาก artifact: source เดิมไม่ reject quantity <=0, setter รับ threshold ติดลบ, แจ้งซ้ำเมื่อ stock ต่ำอยู่แล้ว, และไม่ใช้ channel preference รายสินค้า
- แก้ต้นทาง: ใช้ validation ก่อนเปลี่ยน state, transition check, observers keyed by channel, Product.notification_channels และ test cases สำหรับทุกข้อ
- ผล: implementation อยู่ใน `src/`; acceptance tests ใน `tests/test_service.py` ครอบคลุม boundary, transition, channels, invalid quantity, threshold, report; รัน `python -m pytest tests/ -v` ผ่าน 12 tests

## สิ่งที่ยังต้องยืนยัน
- ผู้เรียนต้องยืนยัน AI ที่ใช้ตรงตามข้อกำหนดฟรีของรายวิชา และเพิ่ม raw prompt/output จากบัญชี/เครื่องมือที่ตนใช้จริง
- ผู้เรียนต้องตรวจและอธิบาย `design_review.md` ด้วยตนเองตามข้อกำหนด Lab 3
