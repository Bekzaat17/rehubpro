from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notifications.consumers.notifications_consumer import NotificationsConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/notifications/", NotificationsConsumer.as_asgi()),
        ])
    ),
})