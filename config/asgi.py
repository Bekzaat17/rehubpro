import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notifications.consumers.notifications_consumer import NotificationsConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rehubpro.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/notifications/", NotificationsConsumer.as_asgi()),
        ])
    ),
})