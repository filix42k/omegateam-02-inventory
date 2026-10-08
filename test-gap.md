# Test gap review for `Inventory.sell`

The short request used for the AI-generated first draft was: “ช่วยเขียน pytest unit test สำหรับเมธอด sell ของ class Inventory ให้หน่อย”. The draft in this work covered a normal sale and insufficient stock; it was a starting point, not evidence that the method was safe.

| กรณีที่ AI ให้มา | กรณีที่ขาด | test ที่เขียนเสริม |
|---|---|---|
| ขายสินค้าจำนวนปกติแล้วคืนจำนวนคงเหลือ | ขายหมดพอดีและยืนยันว่าคงเหลือเป็นศูนย์ | `test_sell_exactly_available_quantity_leaves_zero_stock` |
| ปฏิเสธเมื่อขายเกินยอดคงเหลือ | ขาย 0 และขายจำนวนติดลบ โดยตรวจว่ายอดเดิมไม่เปลี่ยน | `test_sell_rejects_zero_or_negative_quantity_without_changing_stock` |
| ปฏิเสธเมื่อขายเกินยอดคงเหลือ | สินค้าไม่มีในคลังและต้องแจ้งข้อผิดพลาดที่ระบุสินค้า | `test_sell_missing_item_raises_key_error` |
| — | จำนวนทศนิยมและข้อความต้องถูกปฏิเสธก่อนเปลี่ยนยอด | `test_sell_rejects_non_integer_quantity` |
| — | หลัง error ทุกแบบ ยอดคงเหลือต้องไม่เปลี่ยน | assertions ใน tests ของขอบเขตและยอดไม่พอ |

The tests cover all four requested groups: boundary values, invalid values, error paths, and input types. The AI draft is a representative draft generated for this exercise, not a transcript from another tool or a historical teammate interaction.
