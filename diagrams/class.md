# Class Diagram - Inventory System (Omega Team)

```mermaid
classDiagram
    direction TB

    class Category {
        +str name
    }

    class Product {
        +str id
        +str name
        +Category category
        +float price
        +int quantity
        +int threshold
        +str notifier_type
    }

    class StockTransaction {
        +str product_id
        +str transaction_type
        +int quantity
        +datetime timestamp
    }

    class Notifier {
        <<interface>>
        +notify(message: str) void
    }

    class EmailNotifier {
        +str destination
        +notify(message: str) void
    }

    class SMSNotifier {
        +str destination
        +notify(message: str) void
    }

    class NotifierFactory {
        -Dict~str, Type~ _notifier_classes$
        +create(channel: str, destination: str) Notifier$
        +register_notifier(channel: str, notifier_class: Type) void$
    }

    class InventoryService {
        +Dict~str, Product~ products
        +List~StockTransaction~ transactions
        +List~Notifier~ observers
        +add_observer(observer: Notifier) void
        +add_product(product: Product) void
        +receive_stock(product_id: str, quantity: int) void
        +dispense_stock(product_id: str, quantity: int) void
        -_check_threshold_and_notify(product: Product) void
        +get_stock_value_report() Dict~str, Any~
        +set_product_threshold(product_id: str, threshold: int) void
    }

    %% ความสัมพันธ์ (Relationships)
    Product "1" --> "1" Category : has category
    InventoryService "1" *-- "*" Product : Composition (จัดเก็บและดูแลสินค้า)
    InventoryService "1" *-- "*" StockTransaction : Composition (บันทึกประวัติการรับ-จ่าย)
    
    Notifier <|.. EmailNotifier : Realization (สืบทอด Interface)
    Notifier <|.. SMSNotifier : Realization (สืบทอด Interface)
    
    NotifierFactory ..> Notifier : Dependency (สร้าง Notifier)
    InventoryService o-- Notifier : Observer (เก็บ List ของ Notifier และเรียก notify)
```
