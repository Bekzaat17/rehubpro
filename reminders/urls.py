# reminders/urls.py
from django.urls import path
from reminders.views.reminders_page import RemindersPageView
from reminders.views.api import create_reminder, delete_reminder

app_name = "reminders"

urlpatterns = [
    path('', RemindersPageView.as_view(), name="reminders_page"),
    path('create/', create_reminder, name="create_reminder"),
    path('delete/<int:pk>/', delete_reminder, name="delete_reminder"),
]