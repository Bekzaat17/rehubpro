from django.db import models
from ..enums import DependencyType

class Resident(models.Model):
    """
    Модель резидента (человека, проходящего реабилитацию).
    """
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    date_of_admission = models.DateField(verbose_name="Дата поступления")
    dependency_type = models.CharField(
        max_length=10,
        choices=DependencyType.choices,
        default=DependencyType.OTHER,
        verbose_name="Тип зависимости"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Заметки")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Резидент"
        verbose_name_plural = "Резиденты"

    def __str__(self):
        return self.full_name