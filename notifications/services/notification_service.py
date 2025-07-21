from notifications.services.websocket_sender import WebSocketSender
from notifications.services.base import NotificationSender


class NotificationService:
    """
    Фасад уведомлений. Вызывает одну или все стратегии.
    """

    def __init__(self):
        self.senders: dict[str, NotificationSender] = {
            "websocket": WebSocketSender(),
            # "push": PushSender()     # Пока не реализовано
            # "email": EmailSender()   # Пока не реализовано
        }

    def send(self, user, title, message, channel: str = None):
        """
        Отправка уведомления одному пользователю.
        Если `channel` не указан, отправляет по всем стратегиям.
        """
        if channel:
            sender = self.senders.get(channel)
            if not sender:
                raise ValueError(f"Unknown channel: {channel}")
            sender.send(user, title, message)
        else:
            for sender in self.senders.values():
                sender.send(user, title, message)