# notifications/urls.py

from django.urls import path
from notifications.views import notifications_view
from notifications.views.notifications_view import unread_notifications_view

app_name = 'notifications'

urlpatterns = [
    path('unread-count/', notifications_view.unread_count_view, name='unread_count'),
    path('mark-read/', notifications_view.mark_as_read_view, name='mark_as_read'),
    path("unread/", unread_notifications_view, name="unread_notifications"),
]