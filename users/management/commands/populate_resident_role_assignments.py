# roles/management/commands/populate_demo_roles.py

from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random

from residents.models import Resident
from references.models.resident_role import ResidentRole
from roles.models.resident_role_assignment import ResidentRoleAssignment


COMMENTS = [
    "Справился ответственно",
    "Справился хорошо, повысить",
    "Не справился, понизить",
    "Справляется слабо, оставить на той же роли",
    "Отлично проявил инициативу",
    "Выполняет с трудом, нужна поддержка",
    "Без изменений",
    "Хорошая динамика, можно продвинуть"
]


class Command(BaseCommand):
    help = "Полностью перегенерирует историю ролей: каждые 2 недели, у всех обязательно есть роли"

    def handle(self, *args, **kwargs):
        today = date.today()
        roles = list(ResidentRole.objects.order_by("id"))

        if not roles:
            self.stdout.write(self.style.ERROR("❌ Сначала создай справочник ролей"))
            return

        residents = list(Resident.objects.all())
        if not residents:
            self.stdout.write(self.style.WARNING("⚠️  Нет резидентов для назначения ролей"))
            return

        # Очистка всех старых назначений ролей
        deleted_count, _ = ResidentRoleAssignment.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"🗑️  Удалено {deleted_count} всех старых назначений ролей"))

        # Определим даты смены ролей — каждые 14 дней от самой ранней даты поступления
        earliest_date = min(resident.date_of_admission for resident in residents)
        rotation_dates = []
        current = earliest_date

        while current <= today:
            rotation_dates.append(current)
            current += timedelta(days=14)

        for rotation_date in rotation_dates:
            random.shuffle(residents)  # перемешиваем резидентов на каждый цикл
            available_roles = roles[:]  # список доступных ролей

            for resident in residents:
                if resident.date_of_admission > rotation_date:
                    continue  # ещё не поступил

                # Завершаем активные роли
                active_roles = resident.role_assignments.filter(unassigned_at__isnull=True)
                for ar in active_roles:
                    ar.unassigned_at = rotation_date
                    ar.save()

                # Определим, сколько ролей дать (1–2)
                num_roles = random.choice([1, 2])
                assigned_roles = []

                for _ in range(num_roles):
                    if not available_roles:
                        # все роли уже назначались — начинаем сначала
                        available_roles = roles[:]
                        random.shuffle(available_roles)

                    # Берём первую доступную роль
                    role = available_roles.pop(0)
                    assigned_roles.append(role)

                # Назначаем
                for role in assigned_roles:
                    ResidentRoleAssignment.objects.create(
                        resident=resident,
                        role=role,
                        assigned_at=rotation_date,
                        comment=random.choice(COMMENTS),
                    )

        self.stdout.write(self.style.SUCCESS("✅ Роли успешно назначены: у каждого есть хотя бы одна."))