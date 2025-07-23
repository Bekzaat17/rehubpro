# users/management/commands/populate_demo_residents.py

from django.core.management.base import BaseCommand
from residents.models import Resident
from residents.enums import DependencyType, ResidentStatus
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = "Создаёт 10 тестовых резидентов (если их ещё нет)"

    def handle(self, *args, **kwargs):
        today = date.today()

        demo_residents = [
            {
                "first_name": "Иван",
                "last_name": "Иванов",
                "middle_name": "Иванович",
                "identical_number": "test000001",
                "date_of_birth": date(1985, 5, 20),
                "dependency_type": DependencyType.F11,  # Наркоман
                "notes": "Первый тестовый резидент"
            },
            {
                "first_name": "Пётр",
                "last_name": "Петров",
                "middle_name": "Петрович",
                "identical_number": "test000002",
                "date_of_birth": date(1990, 3, 15),
                "dependency_type": DependencyType.F10,  # Алкоголик
                "notes": "Второй тестовый резидент"
            },
            {
                "first_name": "Сергей",
                "last_name": "Сергеев",
                "middle_name": "Сергеевич",
                "identical_number": "test000003",
                "date_of_birth": date(1992, 7, 10),
                "dependency_type": DependencyType.F63,  # Лудоман
                "notes": "Третий тестовый резидент"
            },
            {
                "first_name": "Анна",
                "last_name": "Алексеева",
                "middle_name": "Петровна",
                "identical_number": "test000004",
                "date_of_birth": date(1995, 2, 18),
                "dependency_type": DependencyType.F32,
                "notes": "Четвёртая тестовая резидентка"
            },
            {
                "first_name": "Мария",
                "last_name": "Ильина",
                "middle_name": "Николаевна",
                "identical_number": "test000005",
                "date_of_birth": date(1988, 9, 5),
                "dependency_type": DependencyType.F20,
                "notes": "Пятая тестовая резидентка"
            },
            {
                "first_name": "Николай",
                "last_name": "Смирнов",
                "middle_name": "Игоревич",
                "identical_number": "test000006",
                "date_of_birth": date(1982, 11, 12),
                "dependency_type": DependencyType.F17,
                "notes": "Шестой тестовый резидент"
            },
            {
                "first_name": "Елена",
                "last_name": "Кузнецова",
                "middle_name": "Сергеевна",
                "identical_number": "test000007",
                "date_of_birth": date(1999, 6, 28),
                "dependency_type": DependencyType.F33,
                "notes": "Седьмая тестовая резидентка"
            },
            {
                "first_name": "Дмитрий",
                "last_name": "Орлов",
                "middle_name": "Олегович",
                "identical_number": "test000008",
                "date_of_birth": date(1987, 1, 8),
                "dependency_type": DependencyType.F15,
                "notes": "Восьмой тестовый резидент"
            },
            {
                "first_name": "Оксана",
                "last_name": "Миронова",
                "middle_name": "Алексеевна",
                "identical_number": "test000009",
                "date_of_birth": date(1993, 12, 3),
                "dependency_type": DependencyType.F84,
                "notes": "Девятая тестовая резидентка"
            },
            {
                "first_name": "Алексей",
                "last_name": "Павлов",
                "middle_name": "Андреевич",
                "identical_number": "test000010",
                "date_of_birth": date(1985, 8, 25),
                "dependency_type": DependencyType.F63,  # Лудоман
                "notes": "Десятый тестовый резидент"
            },
        ]

        created_count = 0
        for resident_data in demo_residents:
            admission_days_ago = random.randint(10, 90)
            date_of_admission = today - timedelta(days=admission_days_ago)

            # 👇 Вычисляем статус по количеству дней
            if admission_days_ago < 20:
                status = ResidentStatus.NEWBIE
            elif admission_days_ago < 40:
                status = ResidentStatus.IN_PROGRESS
            else:
                status = ResidentStatus.ADVANCED

            resident, created = Resident.objects.get_or_create(
                identical_number=resident_data["identical_number"],
                defaults={
                    "first_name": resident_data["first_name"],
                    "last_name": resident_data["last_name"],
                    "middle_name": resident_data["middle_name"],
                    "date_of_birth": resident_data["date_of_birth"],
                    "date_of_admission": date_of_admission,
                    "dependency_type": resident_data["dependency_type"],
                    "notes": resident_data["notes"],
                    "status": status,
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Создано {created_count} резидентов"))