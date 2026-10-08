"""สร้างไฟล์ draw.io และตรวจชุดสีด้วย standard library."""
from pathlib import Path
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
doc = ET.Element('mxfile', host='app.diagrams.net')
pages = {
    'Login': ['OMEGA INVENTORY — เข้าสู่ระบบ', 'ชื่อผู้ใช้ *', '[ กรอกชื่อผู้ใช้ ]', '! ระบุชื่อผู้ใช้ในช่องนี้', 'รหัสผ่าน *', '[ กรอกรหัสผ่าน ]   แสดงรหัสผ่าน', '! รหัสผ่านไม่ถูกต้อง กรุณาลองอีกครั้ง', 'เข้าสู่ระบบ', 'เข้าระบบไม่ได้? ติดต่อผู้ดูแล'],
    'Dashboard': ['OMEGA INVENTORY — ภาพรวมคลัง', 'ภาพรวม | เพิ่มสินค้า | ออกจากระบบ', 'ข้อมูลตัวอย่าง: จับต้องได้ 24 | ดิจิทัล 6 | สต็อกต่ำ 3', 'ค้นหาชื่อหรือรหัส [________]   ชนิด [ทั้งหมด]', 'รหัส | ชื่อ | ชนิด | คงเหลือ | สถานะ', 'P001 | ปากกา | จับต้องได้ | 4 ชิ้น | ! สต็อกต่ำ', 'D001 | แบบฝึกหัด | ไฟล์ดิจิทัล | ไม่จำกัด | พร้อมขาย', 'เพิ่มสินค้า', 'สถานะว่าง: ยังไม่มีสินค้าในระบบ — เพิ่มสินค้ารายการแรก', 'ยืนยันคำสั่งซื้อ: จับต้องได้ → จำนวนและสถานะจัดส่ง', 'ดิจิทัล → เปิดดาวน์โหลดได้หลังยืนยันคำสั่งซื้อเท่านั้น'],
    'Add Product': ['OMEGA INVENTORY — เพิ่มสินค้า', '* จำเป็นต้องกรอก', 'ชื่อสินค้า * [____________]   รหัสสินค้า * [____________]', 'ชนิดสินค้า * (●) จับต้องได้ (○) ไฟล์ดิจิทัล', 'หมวดหมู่ [เลือกหมวดหมู่]   ราคา * [_______] บาท', '! ราคา: กรอกตัวเลขมากกว่า 0 บาท', 'จับต้องได้: จำนวนเริ่มต้น * [___] ชิ้น | จุดแจ้งเตือน [___]', 'ดิจิทัล: ไฟล์สินค้า * [เลือกไฟล์] — ไม่มี stock ให้ตัด', 'รูปสินค้า (ไม่บังคับ) [เลือกภาพ]', 'ยกเลิก                         บันทึกสินค้า', '✓ บันทึก ปากกา (P001) แล้ว — กลับไปดูรายการ'],
}
for title, rows in pages.items():
    diagram = ET.SubElement(doc, 'diagram', id=title.replace(' ', '-'), name=title)
    model = ET.SubElement(diagram, 'mxGraphModel', page='1', pageWidth='1000', pageHeight='950')
    cells = ET.SubElement(model, 'root')
    ET.SubElement(cells, 'mxCell', id='0')
    ET.SubElement(cells, 'mxCell', id='1', parent='0')
    for index, label in enumerate(rows):
        primary = index == 0 or label in ('เข้าสู่ระบบ', 'เพิ่มสินค้า') or 'บันทึกสินค้า' in label
        color = '#1E40AF' if primary else '#FFFFFF'
        font = '#FFFFFF' if primary else '#B45309' if label.startswith('!') or '! สต็อกต่ำ' in label else '#15803D' if label.startswith('✓') else '#111827'
        style = f'rounded=1;whiteSpace=wrap;html=0;fillColor={color};fontColor={font};strokeColor=#CBD5E1;fontSize=18;align=left;spacingLeft=18;'
        cell = ET.SubElement(cells, 'mxCell', id=str(index+2), value=label, style=style, vertex='1', parent='1')
        ET.SubElement(cell, 'mxGeometry', x='70', y=str(50+index*70), width='850', height='58', attrib={'as': 'geometry'})
ET.ElementTree(doc).write(root/'inventory-mockup.drawio', encoding='utf-8', xml_declaration=True)
ET.parse(root/'inventory-mockup.drawio')

def lum(code):
    values = [int(code[i:i+2], 16)/255 for i in (1, 3, 5)]
    values = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in values]
    return sum(c*w for c,w in zip(values, (.2126,.7152,.0722)))

ratios = {code: (lum('#FFFFFF')+.05)/(lum(code)+.05) for code in ['#111827','#1E40AF','#15803D','#B45309']}
assert all(value >= 4.5 for value in ratios.values())
print('Verified: 3 draw.io pages, valid XML; contrast ratios:', ratios)
