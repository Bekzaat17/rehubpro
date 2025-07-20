from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.user = self.scope["user"]
        self.group_name = f"user_{self.user.id}"

        # подписываемся на группу
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # отписываемся при отключении
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # пока не обрабатываем входящие сообщения
        pass

    async def send_notification(self, event):
        # метод вызывается из WebSocketSender через group_send
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "title": event["title"],
            "message": event["message"],
        }))