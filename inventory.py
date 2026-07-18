import json

def load_items(path="item.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def update_quantity(items, code, change):
    for item in items:
        if item["code"] == code:
            new_qty = item["quantity"] + change
            if new_qty < 0:
                print("จำนวนคงเหลือไม่พอ")
                return items
            item["quantity"] = new_qty
            return items
    print("ไม่พบสินค้ารหัสนี้")
    return items