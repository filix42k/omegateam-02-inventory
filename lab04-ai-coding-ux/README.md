# Lab 04 — สถานะงาน

เตรียมใน repository เดิมตามโจทย์ ไม่มีการแก้ระบบ inventory หลัก

## มีแล้ว
- findings และ persona พร้อม journey map: **role-play scenario ที่ AI ช่วยร่างตามคำขอผู้ใช้; ไม่ใช่การ role-play กับเพื่อนหรือสัมภาษณ์จริง**
- text wireframe ครบ Login / Dashboard / Add Product
- assets/inventory-mockup.drawio ครบ 3 หน้า แก้ไขได้ใน draw.io
- accessibility checklist, contrast คำนวณผ่าน และปรับ error messages 2 จุดในร่างโดย Codex
- inventory.py, inventory_service.py และ tests/test_discount.py เป็นสำเนาจากผู้สอน; แก้ discount.py แล้วตาม 3 root causes
- baseline-results.txt: ผลเดิม 2/6 โดยเรียกตรง; หลังแก้ยืนยัน `python -m pytest tests/ -v` ผ่าน 6/6 ใน test-results.txt
- AI-assisted code review 8 จุด, debug log พร้อมผลก่อน/หลัง, ตัวอย่าง prompt/context และร่างแบบฝึกหัดส่งท้าย (ระบุที่มาแล้ว)

## ต้องทำก่อนส่ง
1. หากต้องการให้ตรง rubric เต็ม ให้ทีม role-play กับเพื่อนและแทนที่/ยืนยัน findings/persona ด้วยสิ่งที่เกิดขึ้นจริง; ห้ามอ้าง scenario จำลองนี้เป็นผลจากทีม
2. เปิด mockup ตรวจและแก้ด้วยตัวเองอย่างน้อย 2 จุด พร้อมบันทึกก่อน/หลังของตน
3. หากต้องส่งผลทดลองในฐานะนักศึกษา ให้รัน prompt/context ด้วยเครื่องมือฟรีและเก็บผลของตน; ตัวอย่างปัจจุบันเป็นการสาธิตโดย Codex
4. อ่าน inventory_service.py และเพิ่มความเห็นของตนเพื่อเทียบกับ AI review
5. ทบทวนสมมติฐานและหลักฐานใน debug-log.md ด้วยตัวเอง; commit แยกแต่ละ root cause
6. ยืนยัน test-results.txt เป็นผล `python -m pytest tests/ -v` จริง (6 passed)
7. เขียน reflection ใหม่จากประสบการณ์ของตน
8. ทบทวนที่มาของข้อมูลและทำตามรูปแบบทีม/เดี่ยวที่เลือก จากนั้น commit/push ผลงานและส่งลิงก์ repository กับไฟล์ตาม eLearning

## แหล่งต้นฉบับ
https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/labs/lab04-quickstart
https://ecp-rmuti.gitbook.io/software-engineering-in-ai-era/labs/lab04-quickstart/lab04-full

ยังไม่ใช่ชุดงานที่ส่งได้ครบ rubric: findings/persona เป็นสถานการณ์จำลองที่ AI ช่วยร่างตามคำขอผู้ใช้ และส่วนที่โจทย์ให้ผู้เรียนตรวจ/เขียนเองยังเป็น AI-assisted draft. PR #66 ของ Lab 4 ถูก merge เข้า `main` แล้ว; การแก้ scenario รอบนี้ยังต้อง commit/push แยกก่อนจึงจะปรากฏใน remote.
