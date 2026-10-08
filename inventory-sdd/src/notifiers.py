"""Abstraction และ factory สำหรับช่องทางแจ้งเตือน."""

from typing import Protocol, Type


class Notifier(Protocol):
    """สัญญาของผู้แจ้งเตือนทุกช่องทาง."""

    def notify(self, message: str) -> None:
        """แสดงหรือส่งข้อความแจ้งเตือน."""
        ...


class EmailNotifier:
    """จำลองการแจ้งเตือนผ่าน Email ด้วย print."""

    def __init__(self, destination: str) -> None:
        """รับปลายทาง Email จากผู้เรียก."""
        self.destination = destination

    def notify(self, message: str) -> None:
        """พิมพ์ข้อความ Email จำลอง."""
        print(f"[Email] To: {self.destination} - {message}")


class SMSNotifier:
    """จำลองการแจ้งเตือนผ่าน SMS ด้วย print."""

    def __init__(self, destination: str) -> None:
        """รับปลายทาง SMS จากผู้เรียก."""
        self.destination = destination

    def notify(self, message: str) -> None:
        """พิมพ์ข้อความ SMS จำลอง."""
        print(f"[SMS] To: {self.destination} - {message}")


class NotifierFactory:
    """สร้าง notifier โดยไม่ให้ business logic รู้จักคลาสปลายทาง."""

    _notifier_classes: dict[str, Type[Notifier]] = {
        "email": EmailNotifier,
        "sms": SMSNotifier,
    }

    @classmethod
    def create(cls, channel: str, destination: str) -> Notifier:
        """สร้าง notifier ตามชื่อช่องทางและปลายทาง."""
        notifier_class = cls._notifier_classes.get(channel.strip().lower())
        if notifier_class is None:
            raise ValueError(f"ไม่พบช่องทางการแจ้งเตือนประเภท: {channel}")
        return notifier_class(destination)

    @classmethod
    def register_notifier(cls, channel: str, notifier_class: Type[Notifier]) -> None:
        """ลงทะเบียนช่องทางใหม่โดยไม่แก้ business logic."""
        normalized_channel = channel.strip().lower()
        if not normalized_channel:
            raise ValueError("ชื่อช่องทางแจ้งเตือนต้องไม่ว่างเปล่า")
        cls._notifier_classes[normalized_channel] = notifier_class
