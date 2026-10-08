# Lab 04 — สถานะงาน

เตรียมใน repository เดิมตามโจทย์ ไม่มีการแก้ระบบ inventory หลัก

## มีแล้ว
- findings และ persona พร้อม journey map: **ข้อมูลจำลอง ไม่ใช่สัมภาษณ์จริง**
- text wireframe ครบ Login / Dashboard / Add Product
- assets/inventory-mockup.drawio ครบ 3 หน้า แก้ไขได้ใน draw.io
- accessibility checklist, contrast คำนวณผ่าน และปรับ error messages 2 จุดในร่างโดย Codex
- inventory.py, inventory_service.py และ tests/test_discount.py เป็นสำเนาจากผู้สอน; แก้ discount.py แล้วตาม 3 root causes
- baseline-results.txt: ผลเดิม 2/6 โดยเรียกตรง; หลังแก้ยืนยัน `python -m pytest tests/ -v` ผ่าน 6/6 ใน test-results.txt
- AI-assisted code review 8 จุด, debug log พร้อมผลก่อน/หลัง, ตัวอย่าง prompt/context และร่างแบบฝึกหัดส่งท้าย (ระบุที่มาแล้ว)

## ต้องทำก่อนส่ง
1. ทีมสัมภาษณ์กันตามโจทย์และแทนที่ข้อมูลจำลองใน findings/persona
2. เปิด mockup ตรวจและแก้ด้วยตัวเองอย่างน้อย 2 จุด พร้อมบันทึกก่อน/หลังของตน
3. หากต้องส่งผลทดลองในฐานะนักศึกษา ให้รัน prompt/context ด้วยเครื่องมือฟรีและเก็บผลของตน; ตัวอย่างปัจจุบันเป็นการสาธิตโดย Codex
4. อ่าน inventory_service.py และเพิ่มความเห็นของตนเพื่อเทียบกับ AI review
5. ทบทวนสมมติฐานและหลักฐานใน debug-log.md ด้วยตัวเอง; commit แยกแต่ละ root cause
6. ยืนยัน test-results.txt เป็นผล `python -m pytest tests/ -v` จริง (6 passed)
7. เขียน reflection ใหม่จากประสบการณ์ของตน
8. สัมภาษณ์ผู้ใช้จริงแทนข้อมูลจำลอง แล้ว commit / push การแก้ไขเพิ่มเติม เปิด PR ให้เพื่อน review และส่งลิงก์ตาม eLearning

## แหล่งต้นฉบับ
https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/labs/lab04-quickstart
https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/labs/lab04-quickstart/lab04-full

ยังไม่ใช่ชุดงานที่ส่งได้ครบ rubric: findings/persona ยังเป็นข้อมูลจำลอง และส่วนที่โจทย์ให้ผู้เรียนตรวจ/เขียนเองยังเป็น AI-assisted draft. งานปัจจุบัน commit และ push แล้วบน branch `codex/lab4-complete`; PR ยังไม่ได้เปิด.
