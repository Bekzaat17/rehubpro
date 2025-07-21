from django.urls import path
from reminders.views.reminders_page import RemindersPageView
from reminders.views.api import (
    create_reminder,
    delete_reminder,
    get_reminder,
    reminders_list_partial,
)

app_name = "reminders"

urlpatterns = [
    path('', RemindersPageView.as_view(), name="reminders_page"),
    path('create/', create_reminder, name="create_reminder"),
    path('delete/<int:pk>/', delete_reminder, name="delete_reminder"),
    path('<int:pk>/', get_reminder, name="get_reminder"),
    path('list/', reminders_list_partial, name="reminders_list_partial"),
]