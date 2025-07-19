# reports/management/commands/populate_demo_reports.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import localdate
from datetime import timedelta
import random

from residents.models import Resident
from references.models import (
    EmotionalState, PhysicalState, Motivation, DailyDynamics,
    CharacterTrait, FamilyActivity, MrpActivity
)
from roles.models.resident_role_assignment import ResidentRoleAssignment
from tasks.models.task_progress import TaskProgress
from tasks.models.assigned_task import AssignedTask
from reports.services.report_factory import ReportFactory

User = get_user_model()


class Command(BaseCommand):
    help = "Полностью перегенерирует демо-отчёты ResidentReport за каждый день от даты приёма до сегодня."

    def handle(self, *args, **options):
        today = localdate()
        created_by = User.objects.order_by("?").first()

        residents = Resident.objects.all()
        if not residents.exists():
            self.stdout.write(self.style.WARNING("⚠️  Резиденты не найдены."))
            return

        # Кэш справочников
        emotional_states = list(EmotionalState.objects.all())
        physical_states = list(PhysicalState.objects.all())
        motivations = list(Motivation.objects.all())
        dynamics = list(DailyDynamics.objects.all())
        traits = list(CharacterTrait.objects.all())
        mrp_activities = list(MrpActivity.objects.all())
        family_activities = list(FamilyActivity.objects.all())

        for resident in residents:
            # Удаляем все предыдущие отчёты
            deleted_count, _ = resident.daily_reports.all().delete()
            self.stdout.write(self.style.WARNING(
                f"🗑️  Удалено {deleted_count} старых отчётов для {resident}"
            ))

            current_date = resident.date_of_admission

            while current_date <= today:
                # === Генерация данных ===
                data = {
                    "emotional_state": random.choice(emotional_states),
                    "physical_state": random.choice(physical_states),
                    "motivation": random.choice(motivations),
                    "daily_dynamics": random.choice(dynamics),
                    "positive_traits": random.sample(traits, k=random.randint(1, 2)),
                    "negative_traits": random.sample(traits, k=random.randint(0, 1)),
                    "mrp_activity": random.choice(mrp_activities),
                    "family_activity": random.choice(family_activities),
                    "comment": f"Автоотчёт за {current_date}",
                    "usts_info_shared": random.choice([True, False]),
                    "usts_format_followed": random.choice([True, False]),
                    "usts_comment": (
                        "Без замечаний" if random.random() > 0.3 else "Есть нарушения в УСТС"
                    ),
                }

                task_comments = self.get_task_comments(resident, current_date)
                role_statuses = self.get_role_statuses(resident, current_date)

                try:
                    factory = ReportFactory(resident, created_by, date=current_date, skip_validation=True)
                    factory.create_or_update_report(data, task_comments, role_statuses)
                    self.stdout.write(self.style.SUCCESS(
                        f"✔️  Отчёт создан: {resident} → {current_date}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f"❌ Ошибка для {resident} на {current_date}: {e}"
                    ))

                current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS("✅ Все отчёты успешно созданы."))

    def get_task_comments(self, resident, date):
        latest_progress = (
            TaskProgress.objects
            .filter(assigned_task__resident=resident, created_at__date__lte=date)
            .order_by("-created_at")
            .first()
        )

        if not latest_progress:
            return {}

        comment = latest_progress.comment or ""
        if not comment:
            return {}

        return {
            latest_progress.assigned_task.task.id: comment
        }

    def get_role_statuses(self, resident, date):
        statuses = {}
        role_assignments = ResidentRoleAssignment.objects.filter(
            resident=resident,
            assigned_at__lte=date
        ).filter(
            unassigned_at__isnull=True
        ) | ResidentRoleAssignment.objects.filter(
            resident=resident,
            assigned_at__lte=date,
            unassigned_at__gte=date
        )
        for role in role_assignments:
            statuses[str(role.id)] = random.choice(["responsible", "irresponsible"])
        return statuses