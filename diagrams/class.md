classDiagram
    %% Models (models.py)
    class Category {
        +str name
    }

    class Product {
        +str id
        +str name
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

    %% Relationships in Models
    Product o-- Category : has

    %% Notifiers (notifiers.py)
    class Notifier {
        <<Protocol>>
        +send(message: str, destination: str) None
    }

    class EmailNotifier {
        +send(message: str, destination: str) None
    }

    class SMSNotifier {
        +send(message: str, destination: str) None
    }

    class NotifierFactory {
        -Dict _notifiers$
        +get_notifier(notifier_type: str)$ Notifier
        +register_notifier(notifier_type: str, notifier: Notifier)$ None
    }

    %% Relationships in Notifiers
    EmailNotifier ..|> Notifier : Realization
    SMSNotifier ..|> Notifier : Realization
    NotifierFactory ..> Notifier : Creates/Returns

    %% Service (service.py)
    class InventoryService {
        +Dict products
        +List transactions
        +Dict admin_contacts
        +__init__(admin_contacts: Dict)
        +add_product(product: Product) None
        +receive_stock(product_id: str, quantity: int) None
        +dispense_stock(product_id: str, quantity: int) None
        -_check_threshold_and_notify(product: Product) None
        +get_stock_value_report() Dict
        +set_product_threshold(product_id: str, threshold: int) None
        +set_product_notifier(product_id: str, notifier_type: str) None
    }

    %% Service Relationships
    InventoryService *-- Product : manages
    InventoryService *-- StockTransaction : records
    InventoryService ..> NotifierFactory : Dependency