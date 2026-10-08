# AI ethics and team practice

## Responsibility for incorrect charges

The team remains responsible for prices, discounts, member points, and stock changes even when AI proposes the code. Characterization tests protect the existing calculation order, while the new edge tests and CI catch regressions before merge. A passing test is evidence, not a transfer of responsibility; a reviewer must inspect the changed behavior and the business rules.

## Copyright and licensing

Before committing generated code, review it for copied comments, unusual identifiers, and code that resembles a known package. Check source attribution and dependency licenses, prefer small independently understood implementations, and record the origin of instructor-provided files. Do not include third-party code unless its license is compatible with the project.

## Member data and PDPA

Member names and points can identify a person when combined with purchase history. Collect only what checkout needs, explain the purpose, restrict access, define retention and deletion periods, and honor applicable data-subject rights. Test with fake member IDs and do not paste customer records, contact details, or order histories into an AI prompt.

## Bias in recommendations

If recommendations are added, compare exposure, ranking, and outcomes across product categories and customer groups where lawful and appropriate. Use representative test data, check for systematic under-recommendation, and keep a human review path for complaints and unusual results.

## แนวปฏิบัติของทีม (ประมาณ 190 คำ)

ทีม จะ ใช้ AI เป็น ผู้ช่วย เสนอ โค้ด สร้าง ตัวอย่าง และ อธิบาย ทางเลือก เท่านั้น ผู้รับผิดชอบ งาน ต้อง อ่าน โค้ด ทุกบรรทัด และ อธิบาย ผลกระทบ ต่อ สต็อก ราคา แต้มสมาชิก และ ลิงก์ดาวน์โหลด ได้ ก่อน commit ทุก feature ต้อง เริ่ม จาก test ที่ ระบุ พฤติกรรม ชัดเจน เรา จะ รัน test ให้ เห็น ผลแดง ก่อน เขียน โค้ด จากนั้น ตรวจ ว่า test เขียว และ เพิ่มกรณี ขอบเขต กับ error path การ refactor ต้อง มี characterization test บันทึก พฤติกรรมเดิม และ ห้าม เปลี่ยน สูตร ลำดับ ส่วนลด หรือ การปัดเศษ โดย ไม่มี ข้อตกลง ทางธุรกิจ ทุก pull request ต้อง ผ่าน Ruff, pytest และ coverage gate ผู้รีวิว จะ ตรวจ diff, test, dependency และ log ของ CI ด้วยตนเอง หาก CI แดง ห้าม merge จนกว่า จะ เข้าใจ สาเหตุ และ แก้ พร้อม test ใหม่ ข้อมูลสมาชิก จริง ใบสั่งซื้อ และ credentials ห้าม ส่ง เข้า AI ใช้ ข้อมูลจำลอง ใน test และ เก็บ เฉพาะข้อมูล ที่ จำเป็น ทีม จะ ตรวจ license ของ โค้ด และ package ก่อนใช้งาน จำกัด สิทธิ์เข้าถึงข้อมูลสมาชิก กำหนด ระยะเวลาเก็บ และ เปิดช่องทาง แก้ไขหรือลบ ตามคำขอ หากพบ ความผิดพลาด เรื่องราคา หรือ bias ในการแนะนำสินค้า ให้ หยุด feature แจ้งทีม และ แก้ที่สาเหตุ โดย มีหลักฐาน จาก test ก่อน release
