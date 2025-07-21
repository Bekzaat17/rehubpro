# reminders/services/reminder_scheduler.py
from django.utils import timezone
from reminders.models.reminder import Reminder
from reminders.enums import RepeatInterval
from notifications.services.notification_service import NotificationService


class ReminderScheduler:
    def run(self):
        now = timezone.now()
        reminders = Reminder.objects.filter(
            is_active=True,
            datetime__lte=now
        )

        for reminder in reminders:
            # Пропуск, если уже отправлено в эту минуту
            if reminder.last_triggered_at and abs((now - reminder.last_triggered_at).total_seconds()) < 60:
                continue

            # Отправка уведомления
            NotificationService().send(
                user=reminder.user,
                title=reminder.title,
                message=reminder.text
            )

            # Обновление статуса
            reminder.last_triggered_at = now

            if reminder.repeat == RepeatInterval.ONCE:
                reminder.is_active = False
            elif reminder.repeat == RepeatInterval.DAILY:
                reminder.datetime += timezone.timedelta(days=1)
            elif reminder.repeat == RepeatInterval.WEEKLY:
                reminder.datetime += timezone.timedelta(weeks=1)
            elif reminder.repeat == RepeatInterval.MONTHLY:
                # простой способ: прибавим 30 дней (можно позже заменить на dateutil.relativedelta)
                reminder.datetime += timezone.timedelta(days=30)

            reminder.save()