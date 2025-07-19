from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random

from residents.models import Resident
from tasks.models.task_template import TaskTemplate
from tasks.models.assigned_task import AssignedTask
from tasks.models.task_progress import TaskProgress


class Command(BaseCommand):
    help = "Назначает задания резидентам по строгому порядку и длительности"

    # Конфигурация: TaskTemplate.id → (days_writing, days_submitting)
    TASK_SCHEDULE = {
        1: (2, 1),
        2: (3, 20),
        3: (3, 20),
        4: (4, 1),
        5: (2, 20),
        6: (3, 20),
        7: (3, 20),
    }

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Очистка старых AssignedTask и TaskProgress..."))
        TaskProgress.objects.all().delete()
        AssignedTask.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Старые данные удалены.\n"))

        today = date.today()
        task_templates = {t.id: t for t in TaskTemplate.objects.order_by("id")}
        users = list(AssignedTask._meta.get_field("assigned_by").related_model.objects.all())

        if len(task_templates) < 7:
            self.stdout.write(self.style.ERROR("Ожидается 7 шаблонов заданий."))
            return

        for resident in Resident.objects.all():
            self.stdout.write(self.style.NOTICE(f"👤 {resident.full_name}"))

            current_date = resident.date_of_admission
            task_number = 1  # от 1 до 7

            while task_number <= 7:
                # Проверка на доступность шаблона
                if task_number not in self.TASK_SCHEDULE or task_number not in task_templates:
                    self.stdout.write(self.style.WARNING(f"Пропущено задание #{task_number}"))
                    break

                writing_days, submitting_days = self.TASK_SCHEDULE[task_number]
                total_days = writing_days + submitting_days

                if current_date + timedelta(days=total_days - 1) > today:
                    self.stdout.write(f"⏸️  Недостаточно времени на задание #{task_number}, остановка.")
                    break  # Дальше задания уже не поместятся

                task_template = task_templates[task_number]

                assigned_task = AssignedTask.objects.create(
                    task=task_template,
                    resident=resident,
                    assigned_by=random.choice(users) if users else None,
                    writing_started=current_date,
                    status=AssignedTask.Status.WRITING,
                )

                # === WRITING ===
                for i in range(writing_days):
                    TaskProgress.objects.create(
                        assigned_task=assigned_task,
                        stage=TaskProgress.Stage.WRITING,
                        comment=f"День {i + 1}: пишет задание...",
                        updated_by=random.choice(users) if users else None,
                        created_at=current_date + timedelta(days=i),
                    )

                writing_end = current_date + timedelta(days=writing_days - 1)
                submitting_start = writing_end + timedelta(days=1)

                assigned_task.writing_finished = writing_end
                assigned_task.submitting_started = submitting_start
                assigned_task.status = AssignedTask.Status.SUBMITTING
                assigned_task.save()

                # === SUBMITTING ===
                for i in range(submitting_days):
                    day = submitting_start + timedelta(days=i)
                    TaskProgress.objects.create(
                        assigned_task=assigned_task,
                        stage=TaskProgress.Stage.SUBMITTING,
                        comment=f"Сдаёт задание, день {i + 1}",
                        updated_by=random.choice(users) if users else None,
                        created_at=day,
                    )

                # Завершение
                completed_at = submitting_start + timedelta(days=submitting_days - 1)
                TaskProgress.objects.create(
                    assigned_task=assigned_task,
                    stage=TaskProgress.Stage.COMPLETED,
                    comment="Задание завершено удовлетворительно",
                    updated_by=random.choice(users) if users else None,
                    created_at=completed_at,
                )
                assigned_task.completed_at = completed_at
                assigned_task.status = AssignedTask.Status.COMPLETED
                assigned_task.save()

                self.stdout.write(self.style.SUCCESS(
                    f"✅ Назначено задание #{task_number} ({task_template.title}) → {resident.full_name}"
                ))

                current_date = completed_at + timedelta(days=1)
                task_number += 1

        self.stdout.write(self.style.SUCCESS("\nГенерация завершена."))