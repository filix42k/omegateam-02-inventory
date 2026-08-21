# TEAM_CHARTER.md

## สมาชิกและบทบาท

| ชื่อ | GitHub Username | บทบาท |
|---|---|---|
| นางสาวนริสรา ไกยสินธุ์ | filix42k | Product Owner |
| นายชินชนกนันทร์ พรมศรี | chinchanoknantpromsri | Scrum Master |
| นายพชรดนย์ มูลสาระ | poom24052549 | Scrum Master |
| นายกิตติธร รูปสะอาด  | kittithonru-coder | Developer |
| นายเตชสิทธิ์ แก้ววิเชียร  | Mik-kaewwichian | Developer |
| นายพงศกร ศรีวิเศษ  | Phongsakhon870 | Developer |

## Branching Strategy

ทีมใช้ GitHub Flow:
- main branch ต้อง deploy ได้เสมอ ห้าม commit โดยตรง
- ทุก feature ใหม่ต้องสร้าง branch ชื่อ feat/<issue-number>-<short-name>
- ทุก PR ต้องมีคนอื่นในทีมอย่างน้อย 1 คน review และ approve ก่อน merge

## เพดานงานที่ทำพร้อมกัน (WIP limit)

- คอลัมน์ In Progress มีการ์ดพร้อมกันได้ไม่เกิน 3 ใบ (เริ่มที่จำนวนคนที่เขียนโค้ดในทีม)
- เมื่อชนเพดาน ห้ามลากการ์ดใหม่เข้ามา ให้ช่วยกันปิดของเดิมหรือรีวิว PR ที่ค้างใน In Review ก่อน
- ปรับเพดานระหว่าง sprint ได้ แต่ต้องเขียนเหตุผลกำกับไว้ท้ายหัวข้อนี้ ไม่ใช่ปรับเพราะการ์ดล้น

## Sprint Goal (Sprint 1)

sprint นี้ทีมจะส่งมอบ US-01, US-02 และ US-03 ที่รันได้จริงผ่านเมนู Command Line เก็บข้อมูลด้วยไฟล์ JSON และผ่าน acceptance criteria ครบถ้วนทุกข้อ

## AI Usage Policy

- ใช้ AI ช่วยเขียน draft code และ draft commit message ได้
- ทุก commit message ที่ AI generate ต้องอ่านและแก้ให้ตรงกับ diff จริงก่อน commit
- ห้าม copy code จาก AI โดยไม่อ่านและทำความเข้าใจก่อน
- ใช้เฉพาะ AI ที่ไม่มีค่าใช้จ่าย ไม่บังคับซื้อ subscription
