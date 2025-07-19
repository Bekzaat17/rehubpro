# users/management/commands/create_consultant.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Создаёт пользователя-консультанта (если ещё не существует)"

    def handle(self, *args, **kwargs):
        username = os.getenv("CONSULTANT_USERNAME", "consultant")
        email = os.getenv("CONSULTANT_EMAIL", "consultant@example.com")
        password = os.getenv("CONSULTANT_PASSWORD", "rehab123")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Пользователь '{username}' уже существует."))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True  # если нужно доступ к админке
        )

        # Если у тебя есть отдельная модель "Профиль" или "Роль", можно сюда добавить:
        # ConsultantProfile.objects.create(user=user, ...)

        self.stdout.write(self.style.SUCCESS(f"✅ Консультант '{username}' создан."))