import json

import pytest

from inventory import (
    add_item,
    create_initial_db,
    issue_stock,
    list_items,
    load_items,
    receive_stock,
    save_items,
)


def test_create_initial_db_writes_empty_list_and_keeps_existing_file(tmp_path):
    filename = tmp_path / "items.json"
    create_initial_db(filename)
    assert json.loads(filename.read_text(encoding="utf-8")) == []

    filename.write_text('[{"code": "A"}]', encoding="utf-8")
    create_initial_db(filename)
    assert json.loads(filename.read_text(encoding="utf-8")) == [{"code": "A"}]


def test_load_items_handles_missing_valid_invalid_and_non_list_files(tmp_path):
    filename = tmp_path / "items.json"
    assert load_items(filename) == []

    filename.write_text('[{"code": "A"}]', encoding="utf-8")
    assert load_items(filename) == [{"code": "A"}]

    filename.write_text("not json", encoding="utf-8")
    assert load_items(filename) == []
    filename.write_text('{"code": "A"}', encoding="utf-8")
    assert load_items(filename) == []


def test_save_items_persists_json_and_list_items_formats_empty_and_populated(capsys, tmp_path):
    filename = tmp_path / "items.json"
    items = [{"code": "A1", "name": "Pen", "quantity": 3}]
    save_items(items, filename)
    assert json.loads(filename.read_text(encoding="utf-8")) == items

    list_items([])
    assert "ยังไม่มีสินค้า" in capsys.readouterr().out
    list_items(items)
    output = capsys.readouterr().out
    assert "A1" in output and "Pen" in output and "3" in output


@pytest.mark.parametrize(
    ("code", "name", "quantity", "message"),
    [
        ("", "Pen", 1, "กรุณากรอกรหัสสินค้า"),
        ("A1", "  ", 1, "กรุณากรอกชื่อสินค้า"),
        ("A1", "Pen", -1, "จำนวนสินค้าต้องไม่ติดลบ"),
    ],
)
def test_add_item_rejects_invalid_values(capsys, tmp_path, code, name, quantity, message):
    assert add_item([], code, name, quantity, tmp_path / "items.json") is None
    assert message in capsys.readouterr().out


def test_add_item_rejects_duplicate_and_saves_valid_item(capsys, tmp_path):
    filename = tmp_path / "items.json"
    items = [{"code": "A1", "name": "Pen", "quantity": 1}]
    assert add_item(items, "A1", "Other", 2, filename) is None
    assert "รหัสสินค้าซ้ำ" in capsys.readouterr().out

    saved = add_item(items, "B2", " Ruler ", 2, filename)
    assert saved == {"code": "B2", "name": "Ruler", "quantity": 2}
    assert load_items(filename) == items


def test_receive_stock_success_and_errors(capsys, tmp_path):
    filename = tmp_path / "items.json"
    items = [{"code": "A1", "name": "Pen", "quantity": 3}]
    assert receive_stock(items, "A1", 2, filename)["quantity"] == 5
    assert load_items(filename)[0]["quantity"] == 5

    assert receive_stock(items, "A1", -1, filename) is None
    assert "จำนวนรับเข้า" in capsys.readouterr().out
    assert receive_stock(items, "missing", 1, filename) is None
    assert "ไม่พบสินค้า" in capsys.readouterr().out


def test_issue_stock_success_insufficient_quantity_and_errors(capsys, tmp_path):
    filename = tmp_path / "items.json"
    items = [{"code": "A1", "name": "Pen", "quantity": 3}]
    assert issue_stock(items, "A1", 1, filename)["quantity"] == 2
    assert load_items(filename)[0]["quantity"] == 2

    assert issue_stock(items, "A1", 4, filename) is None
    assert "จำนวนคงเหลือไม่พอ" in capsys.readouterr().out
    assert items[0]["quantity"] == 2
    assert issue_stock(items, "A1", -1, filename) is None
    assert "จำนวนจ่ายออก" in capsys.readouterr().out
    assert issue_stock(items, "missing", 1, filename) is None
    assert "ไม่พบสินค้า" in capsys.readouterr().out
