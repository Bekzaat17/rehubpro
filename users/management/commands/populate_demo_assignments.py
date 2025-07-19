from django.core.management.base import BaseCommand
from datetime import date, timedelta, datetime
import random

from residents.models import Resident
from tasks.models.task_template import TaskTemplate
from tasks.models.assigned_task import AssignedTask
from tasks.models.task_progress import TaskProgress


class Command(BaseCommand):
    help = "Назначает задания резидентам по строгому порядку и длительности"

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

            current_datetime = datetime.combine(resident.date_of_admission, datetime.min.time())
            task_number = 1

            while task_number <= 7:
                if task_number not in self.TASK_SCHEDULE or task_number not in task_templates:
                    self.stdout.write(self.style.WARNING(f"Пропущено задание #{task_number}"))
                    break

                writing_days, submitting_days = self.TASK_SCHEDULE[task_number]
                task_template = task_templates[task_number]

                assigned_task = AssignedTask.objects.create(
                    task=task_template,
                    resident=resident,
                    assigned_by=random.choice(users) if users else None,
                    assigned_at=current_datetime,
                    writing_started=current_datetime.date(),
                    status=AssignedTask.Status.WRITING,
                )

                # === WRITING ===
                writing_end = current_datetime.date()
                for i in range(writing_days):
                    day = current_datetime.date() + timedelta(days=i)
                    if day > today:
                        break
                    TaskProgress.objects.create(
                        assigned_task=assigned_task,
                        stage=TaskProgress.Stage.WRITING,
                        comment=f"День {i + 1}: пишет задание...",
                        updated_by=random.choice(users) if users else None,
                        created_at=day,
                    )
                    writing_end = day

                assigned_task.writing_finished = writing_end
                submitting_start = writing_end + timedelta(days=1)
                assigned_task.submitting_started = submitting_start

                # === SUBMITTING ===
                submitted_days_created = 0
                for i in range(submitting_days):
                    day = submitting_start + timedelta(days=i)
                    if day > today:
                        break
                    TaskProgress.objects.create(
                        assigned_task=assigned_task,
                        stage=TaskProgress.Stage.SUBMITTING,
                        comment=f"Сдаёт задание, день {i + 1}",
                        updated_by=random.choice(users) if users else None,
                        created_at=day,
                    )
                    submitted_days_created += 1

                # === COMPLETED ===
                if submitted_days_created == submitting_days:
                    completed_at = submitting_start + timedelta(days=submitting_days)
                    if completed_at <= today:
                        TaskProgress.objects.create(
                            assigned_task=assigned_task,
                            stage=TaskProgress.Stage.COMPLETED,
                            comment="Задание завершено удовлетворительно",
                            updated_by=random.choice(users) if users else None,
                            created_at=completed_at,
                        )
                        assigned_task.completed_at = completed_at
                        assigned_task.status = AssignedTask.Status.COMPLETED
                    else:
                        assigned_task.status = AssignedTask.Status.SUBMITTING
                elif submitted_days_created > 0:
                    assigned_task.status = AssignedTask.Status.SUBMITTING
                else:
                    assigned_task.status = AssignedTask.Status.WRITING

                assigned_task.save()

                self.stdout.write(self.style.SUCCESS(
                    f"✅ Назначено задание #{task_number} ({task_template.title}) → {resident.full_name}"
                ))

                if assigned_task.status != AssignedTask.Status.COMPLETED:
                    self.stdout.write(self.style.WARNING(
                        f"⏹ Прерывание: задание #{task_number} не завершено, следующее не создаётся.\n"
                    ))
                    break

                # ⏩ Новое задание назначаем через 1 минуту после завершения предыдущего
                current_datetime = datetime.combine(assigned_task.completed_at, datetime.min.time()) + timedelta(minutes=1)
                task_number += 1

        self.stdout.write(self.style.SUCCESS("\n🎉 Генерация завершена."))