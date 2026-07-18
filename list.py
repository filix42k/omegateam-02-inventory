import json
import os

# 1. กำหนดตำแหน่งไฟล์ JSON (ปรับชื่อไฟล์ 'item.json' ให้ตรงกับที่คุณใช้งานจริง)
file_path = 'item.json'

try:
    # 2. เปิดและอ่านไฟล์ JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        inventory = json.load(file)
    
    print("==================================================")
    print(f" รายการสินค้าในคลังทั้งหมด ({len(inventory)} รายการ)")
    print("==================================================")
    
    # 3. วนลูปแสดงผล รหัส ชื่อ และจำนวนคงเหลือ
    for item in inventory:
        # สังเกตคีย์ในไฟล์ JSON ของคุณ: 
        # ถ้าใช้คำอื่น เช่น 'code' หรือ 'stock' ให้เปลี่ยนตัวหนังสือในเครื่องหมาย ['...'] ให้ตรงกันนะครับ
        item_id = item.get('id') or item.get('code') or 'ไม่มีรหัส'
        item_name = item.get('name') or 'ไม่ระบุชื่อ'
        item_quantity = item.get('quantity') or item.get('stock') or 0
        
        print(f"รหัส: {item_id:<10} | ชื่อสินค้า: {item_name:<20} | จำนวนคงเหลือ: {item_quantity} ชิ้น")
        
    print("==================================================")

except FileNotFoundError:
    print(f"❌ ไม่พบไฟล์ข้อมูลสินค้าที่ตำแหน่ง: {file_path}")
    print("กรุณาเช็กว่าชื่อไฟล์ในโฟลเดอร์ data ถูกต้องหรือไม่")
except json.JSONDecodeError:
    print("❌ ไฟล์ JSON รูปแบบไม่ถูกต้อง กรุณาเช็กเครื่องหมาย , หรือ [ ] ในไฟล์ข้อมูล")