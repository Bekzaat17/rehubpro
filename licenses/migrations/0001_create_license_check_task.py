from django.db import migrations
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


def create_license_check_task(apps, schema_editor):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    PeriodicTask.objects.update_or_create(
        name="Check license expiration",
        defaults={
            "interval": schedule,
            "task": "licenses.tasks.check_license_expiration.check_license_expiration",
            "args": json.dumps([]),
            "kwargs": json.dumps({}),
            "enabled": True,
        },
    )


def delete_license_check_task(apps, schema_editor):
    PeriodicTask.objects.filter(name="Check license expiration").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("django_celery_beat", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_license_check_task, delete_license_check_task),
    ]