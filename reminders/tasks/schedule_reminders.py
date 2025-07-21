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

    # Буфер на случай если Celery чуть отстаёт
    reminders = Reminder.objects.filter(
        is_active=True,
        datetime__lte=now + timezone.timedelta(minutes=1),
    )

    for reminder in reminders:
        # Явная проверка, чтобы избежать преждевременной отправки
        if now < reminder.datetime:
            continue

        # Форматируем текст уведомления с указанием времени
        message = f"{reminder.text}\n\n🕒 Время: {reminder.datetime.astimezone().strftime('%d.%m.%Y %H:%M')}"

        NotificationService().send(
            user=reminder.user,
            title=reminder.title,
            message=message
        )

        # Обновляем дату по типу повтора
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