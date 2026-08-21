from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Category:
    name: str

@dataclass
class Product:
    id: str
    name: str
    category: Category
    price: float
    quantity: int = 0
    threshold: int = 0
    notifier_type: str = "email"

@dataclass
class StockTransaction:
    product_id: str
    transaction_type: str  # 'in' หรือ 'out'
    quantity: int
    timestamp: datetime = field(default_factory=datetime.now)