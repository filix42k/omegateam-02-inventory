from typing import Protocol


class Notifier(Protocol):
    def notify(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือน (Observer method)"""
        ...

class EmailNotifier:
    def __init__(self, destination: str):
        self.destination = destination

    def notify(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือนผ่าน Email (จำลองการทำงาน)"""
        print(f"[Email] To: {self.destination} - {message}")

class SMSNotifier:
    def __init__(self, destination: str):
        self.destination = destination

    def notify(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือนผ่าน SMS (จำลองการทำงาน)"""
        print(f"[SMS] To: {self.destination} - {message}")

class NotifierFactory:
    _notifier_classes: dict[str, type[Notifier]] = {
        "email": EmailNotifier,
        "sms": SMSNotifier
    }

    @classmethod
    def create(cls, channel: str, destination: str) -> Notifier:
        """สร้างและคืนค่า Notifier ตามช่องทางที่ระบุ พร้อมกำหนดปลายทาง"""
        notifier_class = cls._notifier_classes.get(channel.lower())
        if not notifier_class:
            raise ValueError(f"ไม่พบช่องทางการแจ้งเตือนประเภท: {channel}")
        return notifier_class(destination)

    @classmethod
    def register_notifier(cls, channel: str, notifier_class: type[Notifier]) -> None:
        """ลงทะเบียนช่องทางแจ้งเตือนใหม่ เพื่อรองรับ NFR-02 (Maintainability)"""
        cls._notifier_classes[channel.lower()] = notifier_class        