from src.models import Category, Product
from src.notifiers import NotifierFactory
from src.service import InventoryService


class RecordingNotifier:
    def __init__(self):
        self.messages = []

    def notify(self, message: str) -> None:
        self.messages.append(message)


def make_service(channels=("email",)):
    email = RecordingNotifier()
    sms = RecordingNotifier()
    service = InventoryService({"email": email, "sms": sms})
    product = Product(
        "P1", "สายไฟ", Category("งานไฟฟ้า"), 30,
        quantity=20, threshold=15, notification_channels=channels,
    )
    service.add_product(product)
    return service, product, email, sms


def test_dispense_crossing_threshold_notifies_selected_email():
    service, product, email, sms = make_service(("email",))
    assert service.dispense_stock(product.id, 8) == 12
    assert len(email.messages) == 1
    assert sms.messages == []


def test_equal_threshold_does_not_notify():
    service, product, email, _ = make_service()
    assert service.dispense_stock(product.id, 5) == 15
    assert email.messages == []


def test_does_not_repeat_alert_while_already_below_threshold():
    service, product, email, _ = make_service()
    product.quantity = 12
    service.dispense_stock(product.id, 2)
    assert email.messages == []


def test_receiving_stock_never_triggers_low_stock_alert():
    service, product, email, _ = make_service()
    product.quantity = 10
    assert service.receive_stock(product.id, 2) == 12
    assert email.messages == []


def test_both_channels_receive_the_transition_alert():
    service, product, email, sms = make_service(("email", "sms"))
    service.dispense_stock(product.id, 8)
    assert len(email.messages) == 1
    assert len(sms.messages) == 1


def test_non_positive_receive_and_dispense_are_rejected_without_state_change():
    service, product, _, _ = make_service()
    for invalid_quantity in (0, -1):
        try:
            service.receive_stock(product.id, invalid_quantity)
        except ValueError:
            pass
        else:
            raise AssertionError("receive_stock accepted an invalid quantity")
        try:
            service.dispense_stock(product.id, invalid_quantity)
        except ValueError:
            pass
        else:
            raise AssertionError("dispense_stock accepted an invalid quantity")
    assert product.quantity == 20
    assert service.transactions == []


def test_insufficient_stock_does_not_change_stock_or_transactions():
    service, product, _, _ = make_service()
    try:
        service.dispense_stock(product.id, 21)
    except ValueError as error:
        assert str(error) == "จำนวนคงเหลือไม่พอ"
    else:
        raise AssertionError("overselling was accepted")
    assert product.quantity == 20
    assert service.transactions == []


def test_negative_threshold_is_rejected_without_changing_old_value():
    service, product, _, _ = make_service()
    try:
        service.set_product_threshold(product.id, -5)
    except ValueError as error:
        assert str(error) == "Threshold ไม่สามารถเป็นค่าติดลบได้"
    else:
        raise AssertionError("negative threshold was accepted")
    assert product.threshold == 15


def test_stock_value_report_groups_products_by_category():
    service, _, _, _ = make_service()
    service.add_product(Product("P2", "สวิตช์", Category("งานไฟฟ้า"), 50, 40))
    service.add_product(Product("P3", "ท่อ PVC", Category("งานประปา"), 60, 50))
    report = service.get_stock_value_report()
    assert report["categories"] == {"งานไฟฟ้า": 2600.0, "งานประปา": 3000.0}
    assert report["total_value"] == 5600.0


def test_empty_stock_report_is_zero_with_message():
    report = InventoryService().get_stock_value_report()
    assert report == {
        "message": "ยังไม่มีข้อมูลสินค้าในระบบ",
        "categories": {},
        "total_value": 0.0,
    }


def test_notifier_factory_can_create_existing_channels():
    assert NotifierFactory.create("email", "manager@example.test").destination == "manager@example.test"
    assert NotifierFactory.create("sms", "0000000000").destination == "0000000000"


def test_product_cannot_select_a_channel_without_a_configured_observer():
    service = InventoryService({"email": RecordingNotifier()})
    product = Product(
        "P2", "ดอกสว่าน", Category("เครื่องมือ"), 80,
        notification_channels=("sms",),
    )
    try:
        service.add_product(product)
    except ValueError as error:
        assert "sms" in str(error)
    else:
        raise AssertionError("unconfigured notification channel was accepted")
    assert product.id not in service.products
