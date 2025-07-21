from django.db import migrations
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


def create_schedule_reminders_task(apps, schema_editor):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.update_or_create(
        name="Schedule reminders task",
        defaults={
            "interval": schedule,
            "task": "reminders.tasks.schedule_reminders.schedule_reminders",
            "args": json.dumps([]),
            "kwargs": json.dumps({}),
            "enabled": True,
        },
    )


def delete_schedule_reminders_task(apps, schema_editor):
    PeriodicTask.objects.filter(name="Schedule reminders task").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("reminders", "0001_initial"),  # измени, если у тебя другая последняя миграция
        ("django_celery_beat", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_schedule_reminders_task, delete_schedule_reminders_task),
    ]