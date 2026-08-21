from typing import Protocol, Dict

class Notifier(Protocol):
    def send(self, message: str, destination: str) -> None:
        """ส่งข้อความแจ้งเตือนไปยังปลายทาง"""
        ...

class EmailNotifier:
    def send(self, message: str, destination: str) -> None:
        """ส่งข้อความแจ้งเตือนผ่าน Email (จำลองการทำงาน)"""
        print(f"[Email] To: {destination} - {message}")

class SMSNotifier:
    def send(self, message: str, destination: str) -> None:
        """ส่งข้อความแจ้งเตือนผ่าน SMS (จำลองการทำงาน)"""
        print(f"[SMS] To: {destination} - {message}")

class NotifierFactory:
    _notifiers: Dict[str, Notifier] = {
        "email": EmailNotifier(),
        "sms": SMSNotifier()
    }

    @classmethod
    def get_notifier(cls, notifier_type: str) -> Notifier:
        """คืนค่า Notifier ตามประเภทที่ระบุ"""
        notifier = cls._notifiers.get(notifier_type.lower())
        if not notifier:
            raise ValueError(f"ไม่พบช่องทางการแจ้งเตือนประเภท: {notifier_type}")
        return notifier

    @classmethod
    def register_notifier(cls, notifier_type: str, notifier: Notifier) -> None:
        """ลงทะเบียนช่องทางแจ้งเตือนใหม่ เพื่อรองรับ NFR-02 (Maintainability)"""
        cls._notifiers[notifier_type.lower()] = notifier
        