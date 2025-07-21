# rehubpro/reminders/tasks/schedule_reminders.py
from celery import shared_task
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from reminders.models import Reminder
from reminders.enums import RepeatInterval
from notifications.services.notification_service import NotificationService


@shared_task
def schedule_reminders():
    now = timezone.now()

    reminders = Reminder.objects.filter(
        is_active=True,
        datetime__lte=now,
    )

    for reminder in reminders:
        NotificationService().send(
            user=reminder.user,
            title=reminder.title,
            message=reminder.text
        )

        if reminder.repeat == RepeatInterval.ONCE:
            reminder.is_active = False

        elif reminder.repeat == RepeatInterval.DAILY:
            reminder.datetime += timezone.timedelta(days=1)

        elif reminder.repeat == RepeatInterval.WEEKLY:
            reminder.datetime += timezone.timedelta(weeks=1)

        elif reminder.repeat == RepeatInterval.MONTHLY:
            reminder.datetime += relativedelta(months=1)

        reminder.last_triggered_at = now

        reminder.save()