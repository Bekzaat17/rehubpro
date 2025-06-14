# rehubpro/reports/models/resident_report.py

from django.db import models
from django.core.exceptions import ValidationError
from residents.models import Resident
from users.models import User
from references.models import (
    CharacterTrait,
    ResidentRole,
    DailyDynamics,
    Motivation,
    PhysicalState,
    EmotionalState,
    FamilyActivity,
    MrpActivity,
)

class ResidentReport(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    # Эмоциональное состояние (один вариант)
    emotional_state = models.ForeignKey(
        EmotionalState,
        on_delete=models.PROTECT,
        related_name="emotional_reports"
    )

    # Физическое состояние и жалобы
    physical_state = models.ForeignKey(
        PhysicalState,
        on_delete=models.PROTECT,
        related_name="physical_reports"
    )
    physical_complaints = models.TextField(blank=True)

    # Активности
    family_activity = models.ForeignKey(
        FamilyActivity,
        on_delete=models.PROTECT
    )
    mrp_activity = models.ForeignKey(
        MrpActivity,
        on_delete=models.PROTECT
    )

    # УСТС
    usts_info_shared = models.BooleanField()
    usts_format_followed = models.BooleanField()
    usts_consequences = models.TextField(blank=True)

    # Мотивация
    motivation = models.ForeignKey(
        Motivation,
        on_delete=models.PROTECT
    )

    # Динамика в процентах
    dynamic_percent = models.PositiveIntegerField()

    # Характер: достоинства и дефекты (многие ко многим)
    character_traits = models.ManyToManyField(
        CharacterTrait,
        related_name="reports"
    )

    # Функции
    resident_role = models.ManyToManyField(
        ResidentRole,
        related_name="reports"
    )

    # Дополнительные заметки
    notes = models.TextField(blank=True)

    # Общая динамика (radio/select)
    dynamic_summary = models.ForeignKey(
        DailyDynamics,
        on_delete=models.PROTECT,
        related_name="summary_reports"
    )

    class Meta:
        verbose_name = "Ежедневный отчёт"
        verbose_name_plural = "Ежедневные отчёты"

    def clean(self):
        """Проверка валидности по типу справочников"""
        for trait in self.character_traits.all():
            if trait.type.slug not in ["dostoinstvo", "defekt"]:
                raise ValidationError("Недопустимый тип характера")

        if self.dynamic_percent > 100:
            raise ValidationError("Динамика не может превышать 100%")

    def __str__(self):
        return f"Отчёт по {self.resident.full_name} от {self.created_at.date()}"