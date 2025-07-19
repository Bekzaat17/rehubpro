from django.db import models
from datetime import date
from ..enums import DependencyType
from ..managers import ActiveResidentManager


class Resident(models.Model):
    """
    Модель резидента (человека, проходящего реабилитацию).
    """
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Отчество"
    )

    date_of_birth = models.DateField(verbose_name="Дата рождения")
    date_of_admission = models.DateField(verbose_name="Дата поступления")

    # Менеджеры
    objects = models.Manager()  # обычный — для админки и прямого доступа
    active = ActiveResidentManager()


    dependency_type = models.CharField(
        max_length=10,
        choices=DependencyType.choices,
        default=DependencyType.OTHER,
        verbose_name="Тип зависимости"
    )

    identical_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Идентификационный номер"
    )

    notes = models.TextField(blank=True, null=True, verbose_name="Заметки")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        verbose_name = "Резидент"
        verbose_name_plural = "Резиденты"
        ordering = ["last_name", "first_name"]
        default_manager_name = "active"

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(p for p in parts if p)

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def days_in_rehab(self):
        return (date.today() - self.date_of_admission).days