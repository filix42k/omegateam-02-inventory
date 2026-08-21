# Sprint Retrospective: Sprint 1

## Velocity

- Story point ที่วางแผน: 13 points
- Story point ที่ทำสำเร็จ (Done): 13 points
- Velocity Sprint 1: 13 points

## เพดานงานที่ทำพร้อมกัน (WIP limit)
- เพดานที่ตั้งไว้ใน TEAM_CHARTER.md: 3 ใบ
- ชนเพดานกี่ครั้งใน sprint นี้: 1 ครั้ง
- เพดานที่จะใช้ใน sprint หน้า: 3 ใบ เพราะ สมาชิกสามารถแบ่งงานกันทำได้โดยไม่ชนกัน

> ทีมวางแผน US-01 = 3 points, US-02 = 5 points และ US-03 = 5 points  
> นับเฉพาะ User Story ที่อยู่ในสถานะ Done เมื่อสิ้นสุด Sprint

## Start: สิ่งที่ควรเริ่มทำในรอบต่อไป

- ตรวจสอบชื่อ Branch และหมายเลข Issue ก่อน Commit และ Push เพื่อป้องกันการใช้ชื่อ Branch ตัวอย่างที่ไม่ตรงกับงานจริง
- อัปเดต `main` ด้วย `git pull origin main` ก่อนสร้าง Branch ใหม่ทุกครั้ง เพื่อลด Merge Conflict
- ตกลงรูปแบบข้อมูลและชื่อฟังก์ชันร่วมกันก่อนเริ่มพัฒนา เพื่อให้โค้ดของสมาชิกเชื่อมต่อกันได้ง่าย

## Stop: สิ่งที่ควรหยุดทำ

- หยุดคัดลอกคำสั่งตัวอย่างโดยไม่เปลี่ยนชื่อ Branch ให้ตรงกับ Issue จริง ตัวอย่างเช่น การใช้ `feat/5-load-items` ทั้งที่งานจริงคือ `feat/5-list-items`
- หยุด Commit งานโดยไม่ตรวจสอบ Branch ปัจจุบัน เพราะใน Sprint นี้เคย Commit งาน `load_items()` ลงใน Branch `docs/update-readme`
- หยุด Merge Pull Request ของตนเองโดยไม่มีเพื่อน Review เพราะไม่เป็นไปตาม GitHub Flow ของทีม

## Continue: สิ่งที่ทำได้ดี ควรทำต่อ

- ใช้ GitHub Issues และ Project Board เพื่อติดตามงานจาก To Do, In Progress, In Review และ Done
- แบ่งงานให้สมาชิกคนละ Task และระบุ Assignee อย่างชัดเจน
- Commit งานเป็นส่วนเล็กและใช้ข้อความ Commit ที่อธิบายสิ่งที่เปลี่ยนแปลง
- ทดสอบโค้ดทั้งกรณีปกติและกรณีข้อมูลว่างก่อนเปิด Pull Request

## AI Commit Audit

PR #10 เป็น PR ที่ต้องตรวจแก้คำแนะนำจาก AI มากที่สุด เนื่องจากคำสั่งตัวอย่างระบุชื่อ Branch และฟังก์ชันเป็น `feat/5-load-items` และ `load_items()` แต่ Diff จริงของ Issue #5 เป็นฟังก์ชัน `list_items()` ทีมจึงแก้ชื่อ Branch และ Commit Message ให้ตรงกับงานจริงก่อนส่ง Pull Request

## Action Item สำหรับ Sprint ถัดไป

| Action | เจ้าของ |
|---|---|
| ตรวจสอบ Issue, Branch และ Commit Message ก่อน Push ทุกครั้ง | นางสาวนริสรา ไกยสินธุ์ |
| ตรวจสอบว่า PR ทุกใบมี Review Comment และ Approval ก่อน Merge | นายชินชนกนันทร์ พรมศรี |

### รายละเอียด Velocity

| User Story | Story Points | สถานะ ณ สิ้น Sprint | คะแนนที่นับ |
|---|---:|---|---:|
| US-01 ดูรายการสินค้า | 3 | Done | 3 |
| US-02 เพิ่มสินค้าใหม่ | 5 | Done | 5 |
| US-03 แก้ไขจำนวนสินค้า | 5 | Done | 5 |
| **รวม** | **13** | | **13** |

## การวิเคราะห์ Project Board

**Issue ที่ใช้เวลานานที่สุดจาก In Progress ถึง Done:**  
Issue #4: เขียนฟังก์ชัน `load_items()` อ่านข้อมูลจากไฟล์ JSON เนื่องจากต้องรองรับกรณีไม่มีไฟล์หรือข้อมูล JSON ไม่ถูกต้อง และต้องรวมโค้ดกับฟังก์ชัน `list_items()` โดยไม่เขียนทับงานเดิม

**Issue ที่ค้างใน In Progress นานผิดปกติหรือเป็น Blocker:**  
ไม่พบ Issue ค้างใน In Progress ณ สิ้น Sprint โดย Task ของ US-01, US-02 และ US-03 ได้ดำเนินการเสร็จและผ่านกระบวนการ Pull Request แล้ว

**จำนวน Pull Request ที่ Merge สำเร็จ:**  
ทีม Merge Pull Request สำเร็จทั้งหมด 6 PR

### ภาพถ่าย Project Board ณ สิ้นสุด Sprint 1

![Project Board Screenshot](image.png)
