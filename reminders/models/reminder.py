# reminders/models/reminder.py
from django.db import models
from django.contrib.auth import get_user_model
from reminders.enums import RepeatInterval

User = get_user_model()


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # для заголовка уведомления
    text = models.TextField()                 # подробное описание
    datetime = models.DateTimeField()         # когда сработает
    repeat = models.CharField(
        max_length=20,
        choices=RepeatInterval.choices,
        default=RepeatInterval.ONCE
    )
    is_active = models.BooleanField(default=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        return f"{self.title} — {self.datetime.strftime('%Y-%m-%d %H:%M')}"