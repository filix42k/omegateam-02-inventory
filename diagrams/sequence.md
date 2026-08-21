sequenceDiagram
    actor Staff as พนักงาน
    participant IS as InventoryService
    participant P as Product
    participant Tx as StockTransaction
    participant NF as NotifierFactory
    participant N as Notifier (Email/SMS)

    Staff->>IS: dispense_stock(product_id, quantity)
    
    %% ตรวจสอบรหัสสินค้า
    IS->>IS: ตรวจสอบ product_id ใน self.products
    
    %% ตรวจสอบจำนวนสต็อก
    IS->>P: อ่านค่า quantity ปัจจุบัน
    alt จำนวนสินค้าไม่พอ (quantity < ขอเบิก)
        IS-->>Staff: raise ValueError("จำนวนคงเหลือไม่พอ")
    else จำนวนสินค้าเพียงพอ
        %% อัปเดตสต็อกและบันทึก Transaction
        IS->>P: ลดจำนวน quantity (product.quantity -= quantity)
        IS->>Tx: สร้าง StockTransaction(product_id, "out", quantity)
        Tx-->>IS: คืนค่า instance
        IS->>IS: นำ transaction เพิ่มลง self.transactions
        
        %% ตรวจสอบ Threshold
        IS->>IS: _check_threshold_and_notify(product)
        IS->>P: ตรวจสอบ quantity < threshold
        
        alt ถ้าน้อยกว่า Threshold (สต็อกต่ำ)
            IS->>P: ดึงค่า notifier_type
            IS->>NF: NotifierFactory.get_notifier(notifier_type)
            NF-->>IS: คืนค่า Notifier object (Email/SMS)
            IS->>N: notifier.send(message, destination)
            N-->>IS: ส่งแจ้งเตือนสำเร็จ
        end
        IS-->>Staff: ทำรายการจ่ายสินค้าสำเร็จ
    end