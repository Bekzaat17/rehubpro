# users/management/commands/populate_task_templates.py

from django.core.management.base import BaseCommand
from tasks.models.task_template import TaskTemplate
from tasks.enums.task_type import TaskType


class Command(BaseCommand):
    help = "Создаёт шаблоны заданий (если их ещё нет)"

    def handle(self, *args, **kwargs):
        templates = [
            ("#1 Тест", TaskType.TEST),
            ("#2 Плюсы и минусы употребления", TaskType.LONG_TERM),
            ("#3 Потери от употребления", TaskType.LONG_TERM),
            ("#4 Моё дно", TaskType.SHORT_TERM),
            ("#5 Иллюзии", TaskType.LONG_TERM),
            ("#6 Бессилие", TaskType.LONG_TERM),
            ("#7 Неуправляемость", TaskType.LONG_TERM),
        ]

        created = 0
        for title, task_type in templates:
            obj, is_created = TaskTemplate.objects.get_or_create(
                title=title,
                defaults={"task_type": task_type}
            )
            if is_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Создано {created} шаблонов заданий"))