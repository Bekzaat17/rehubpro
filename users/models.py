from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Список допустимых ролей пользователей, используем TextChoices для читаемости и удобства
class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Администратор'
    CONSULTANT = 'consultant', 'Консультант'
    PSYCHOLOGIST = 'psychologist', 'Психолог'


# Кастомный менеджер пользователей. Обязательно нужен при кастомной модели User.
class UserManager(BaseUserManager):
    # Метод для создания обычного пользователя
    def create_user(self, username, email, password=None, role=UserRole.CONSULTANT, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)  # Приводим email к стандартному виду
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)  # Хешируем пароль
        user.save(using=self._db)  # Сохраняем в базу
        return user

    # Метод для создания суперпользователя
    def create_superuser(self, username, email, password=None, **extra_fields):
        # Устанавливаем обязательные флаги для админки
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, role=UserRole.ADMIN, **extra_fields)


# Основная модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    # Имя пользователя (логин)
    username = models.CharField(max_length=150, unique=True)

    # Email, обязателен и уникален
    email = models.EmailField(unique=True)

    # Роль пользователя (админ, консультант, психолог)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CONSULTANT
    )

    # Активен ли пользователь (может входить)
    is_active = models.BooleanField(default=True)

    # Является ли сотрудником (доступ к админке)
    is_staff = models.BooleanField(default=False)

    # Подключаем наш кастомный менеджер
    objects = UserManager()

    # Основное поле для логина — username
    USERNAME_FIELD = 'username'

    # Обязательные поля при создании суперпользователя
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username  # Отображение пользователя в админке и логах