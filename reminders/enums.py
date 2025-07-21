# reminders/enums.py
from django.db import models

class RepeatInterval(models.TextChoices):
    ONCE = 'once', 'Один раз'
    DAILY = 'daily', 'Каждый день'
    WEEKLY = 'weekly', 'Каждую неделю'
    MONTHLY = 'monthly', 'Каждый месяц'