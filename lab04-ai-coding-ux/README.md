# Lab 04 — สถานะและหลักฐาน

งาน Lab 4 เก็บไว้ในโฟลเดอร์นี้ใน repository เดิม ส่วนงาน Lab 5 อยู่ที่โฟลเดอร์หลัก

## ขอบเขตการใช้ AI

ผู้ใช้แจ้งเมื่อ 9 ต.ค. 2569 ว่าอาจารย์อนุญาตให้ใช้ AI ช่วยทำ Lab 4 ต่อไปนี้เป็นผลงานที่ Codex ช่วยร่าง/ตรวจตามคำขอ และมี `AI_USE_LOG.md` บันทึกที่มาไว้ ข้อมูลผู้ใช้เป็นสถานการณ์จำลอง ไม่ใช่บทสัมภาษณ์หรือ role-play ที่เกิดขึ้นจริง และไม่ได้ระบุชื่อหรือคำพูดของบุคคลจริง

## สิ่งที่อยู่ในชุดงาน

- `findings-lab04.md`, `persona.md`: findings, needs/pain points/surprises, POV และ journey map 5 ขั้นจาก scenario จำลอง
- `assets/wireframe-ai.md`: wireframe หน้า Login, Dashboard และ Add Product
- `assets/inventory-mockup.drawio`, `assets/mockup-link.txt`: mockup แก้ไขได้ 3 หน้าใน draw.io
- `accessibility-review.md`: checklist, contrast ratio และจุดที่แก้จาก AI draft 2 จุด
- `prompt-vs-context.md`: prompt 2 รอบ ผลตัวอย่าง และการเปรียบเทียบ โดยเปิดเผยว่า Codex สร้างผลทั้งสองรอบ
- `inventory_service.py`, `code-review.md`: สำเนาโค้ดผู้สอนและ review comments พร้อมตัวอย่างกรณีผิดพลาด/การจัดหมวด
- `discount.py`, `tests/test_discount.py`, `debug-log.md`: โค้ดที่แก้แล้ว, หลักฐาน root cause และผลทดสอบ
- `reflection.md`: ร่างคำตอบแบบฝึกหัดส่งท้ายที่ระบุว่า Codex เป็นผู้ร่าง
- `AI_USE_LOG.md`: บันทึกการใช้ AI และที่มาของผลลัพธ์

## ผลตรวจที่ยืนยันได้

- `python -m pytest tests/ -v` ผ่าน 6/6 ตาม `test-results.txt`
- `discount.py` มีการแก้ 3 root causes: สูตรส่วนลด, average ของรายการว่าง และ slice ของ `cheapest_n`
- mockup draw.io มี 3 หน้า และไฟล์ XML ตรวจ parse ได้
- contrast ที่คำนวณใน checklist: ข้อความหลัก 17.74:1, ปุ่ม Primary 8.72:1, Success/Warning ประมาณ 5.02:1 บนพื้นขาว

## ข้อจำกัดประวัติ Git

โค้ดแก้ทั้งสาม root causes เดิมถูกรวมใน commit `9315382` ไม่ได้แยก commit ต่อ root cause ตามข้อความใน Lab 4 การแยกประวัติย้อนหลังหลัง PR ถูก merge แล้วจะเป็นการสร้างประวัติใหม่ จึงไม่ได้อ้างว่า commit เดิมแยกไว้แล้ว

เอกสารติดตามผล Lab 4 ล่าสุดอยู่ใน branch `codex/lab4-followup` และแยกจาก Lab 5 แล้ว การสร้าง PR ผ่าน GitHub connector ถูกปฏิเสธด้วย 403; เปิดหน้าเปรียบเทียบ branch ได้ที่:
https://github.com/filix42k/omegateam-02-inventory/compare/main...codex/lab4-followup?expand=1

## แหล่งโจทย์

- https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/labs/lab04-quickstart
- https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/labs/lab04-quickstart/lab04-full
