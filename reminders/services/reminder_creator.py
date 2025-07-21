# reminders/services/reminder_creator.py
from reminders.models.reminder import Reminder
from django.contrib.auth.models import User


class ReminderCreator:
    def __init__(self, user: User):
        self.user = user

    def create(self, data: dict) -> Reminder:
        return Reminder.objects.create(user=self.user, **data)

    def update(self, reminder: Reminder, data: dict) -> Reminder:
        for field, value in data.items():
            setattr(reminder, field, value)
        reminder.save()
        return reminder