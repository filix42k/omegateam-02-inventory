# Debug log — discount.py

> บันทึกนี้จัดทำโดย Codex ตามคำขอผู้ใช้ เป็นตัวอย่างการไล่หลักฐานที่ตรวจสอบซ้ำได้ ไม่ใช่บันทึกที่นักศึกษาทำเอง. หากส่งงาน ให้ผู้เรียนอ่านหลักฐานและเขียน/ยืนยันด้วยตัวเอง.

## สภาพแวดล้อมและวิธีทดสอบ
เริ่มต้น Python ของสภาพแวดล้อมไม่มี pytest (`No module named pytest`). ติดตั้ง pytest 9.1.1 และ dependencies ลงโฟลเดอร์ชั่วคราวเฉพาะ Lab 4 แล้วรัน `python -m pytest tests/ -v` จากโฟลเดอร์นี้ได้จริง.

### Root cause 1 — สูตรส่วนลดผิด
1. Reproduce: `test_apply_discount_basic` ได้ assertion fail เมื่อ input `(100.0, 10)` คาด 90.0
2. Traceback: `tests/test_discount.py:8`, assertion `apply_discount(100.0, 10) == 90.0`
3. สมมติฐาน: โค้ดลบ `percent / 100` ซึ่งลบ 0.1 บาท แทนการหักร้อยละ 10 ของราคา
4. ยืนยัน: โค้ดเดิมคืน 99.9 แทน 90.0; `test_apply_discount_zero` ผ่านเพราะ 0% ไม่ทำให้เห็นข้อผิดพลาดของสูตร
5. Root cause/แก้: เปลี่ยนเป็น `price * (1 - percent / 100)`; การแก้ทำให้ 100 บาทลด 10% เหลือ 90 บาท และไม่เปลี่ยนเมื่อ percent=0

### Root cause 2 — average_price ไม่รองรับรายการว่าง
1. Reproduce: `test_average_price_empty` โยน `ZeroDivisionError`
2. Traceback: `discount.py:18`, `sum(prices) / len(prices)`; test assertion อยู่ `tests/test_discount.py:28`
3. สมมติฐาน: เมื่อ list ว่าง ตัวหาร `len(prices)` เป็น 0
4. ยืนยัน: `len([]) == 0`; traceback ชี้ division by zero โดยตรง
5. Root cause/แก้: เพิ่มกรณี `if not prices: return 0.0` ตาม expected result ใน test

### Root cause 3 — cheapest_n เริ่ม slice ที่ index 1
1. Reproduce: `test_cheapest_n` คาด `[10.0, 20.0]` แต่ไม่ผ่าน
2. Traceback: assertion `tests/test_discount.py:33`
3. สมมติฐาน: `ordered[1:n]` ตัดสินค้าราคาถูกที่สุดที่ตำแหน่ง 0 ออก และคืนเพียง n−1 รายการ
4. ยืนยัน: รายการเรียงแล้วคือ `[10.0, 20.0, 30.0, 50.0]`; `ordered[1:2]` ได้ `[20.0]`
5. Root cause/แก้: ใช้ `ordered[:n]` เพื่อเลือก n ตัวแรกหลังเรียงราคา

### Failure ที่ตามมาจาก root cause 1
`test_bulk_total` ล้มเหลวเพราะรวม 300 บาทแล้วส่งเข้า `apply_discount` ที่ใช้สูตรผิด. ไม่ต้องแก้ `bulk_total`; เมื่อแก้ root cause ของส่วนลด test นี้ผ่านด้วย.

## ผลหลังแก้
ผล `python -m pytest tests/ -v`: **6 passed in 0.03s**. ผลและชื่อ test ถูกบันทึกใน `test-results.txt`.

## Commit แยก root cause
ยังไม่ได้สร้าง commit แยกสาม root causes เพราะนโยบาย branch ของทีมกำหนด `feat/<issue-number>-<short-name>` แต่ไม่พบ issue ที่เกี่ยวข้องให้ใช้เป็นเลขอ้างอิง; ไม่ควรเดา issue number หรือ commit ตรง main.
