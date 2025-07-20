from .base import NotificationSender
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class WebSocketSender(NotificationSender):
    """
    Отправка уведомлений через WebSocket (Django Channels).
    """

    def send(self, user, title, message):
        # Сохраняем уведомление и получаем его ID
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            channel='websocket',
        )

        # Отправляем через WebSocket в нужную группу
        channel_layer = get_channel_layer()
        group_name = f"user_{user.id}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "id": notification.id,        # ✅ Передаём ID уведомления
                "title": title,
                "message": message,
            }
        )