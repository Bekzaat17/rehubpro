from django.db import models
from django.conf import settings
from django.utils import timezone

from residents.models import Resident
from references.models.emotional_state import EmotionalState
from references.models.physical_state import PhysicalState
from references.models.motivation import Motivation
from references.models.daily_dynamics import DailyDynamics
from references.models.character_trait import CharacterTrait
from references.models.family_activity import FamilyActivity
from references.models.mrp_activity import MrpActivity


class ResidentReport(models.Model):
    """
    Ежедневный отчёт по резиденту, заполняемый консультантом.
    Один отчёт — на одного резидента за день.
    """

    resident = models.ForeignKey(
        Resident, on_delete=models.CASCADE, related_name="daily_reports"
    )
    date = models.DateField(default=timezone.localdate)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="resident_reports_created"
    )

    emotional_state = models.ForeignKey(EmotionalState, on_delete=models.SET_NULL, null=True)
    physical_state = models.ForeignKey(PhysicalState, on_delete=models.SET_NULL, null=True)
    motivation = models.ForeignKey(Motivation, on_delete=models.SET_NULL, null=True)
    daily_dynamics = models.ForeignKey(DailyDynamics, on_delete=models.SET_NULL, null=True)

    positive_traits = models.ManyToManyField(
        CharacterTrait,
        related_name="positive_reports",
        blank=True,
        help_text="Отмеченные достоинства характера"
    )
    negative_traits = models.ManyToManyField(
        CharacterTrait,
        related_name="negative_reports",
        blank=True,
        help_text="Отмеченные дефекты характера"
    )

    mrp_activity = models.ForeignKey(MrpActivity, on_delete=models.SET_NULL, null=True, blank=True)
    family_activity = models.ForeignKey(FamilyActivity, on_delete=models.SET_NULL, null=True, blank=True)

    # --- утреннее собрание терапевтического сообщества ---
    usts_info_shared = models.BooleanField(
        default=False,
        help_text="Информацию подает (ровно / не ровно)"
    )
    usts_format_followed = models.BooleanField(
        default=False,
        help_text="Имеет ли формат УСТС"
    )
    usts_comment = models.TextField(
        blank=True,
        help_text="Комментарий по УСТС"
    )

    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ("resident", "date")
        ordering = ["-date"]
        verbose_name = "Ежедневный отчет"
        verbose_name_plural = "Ежедневные отчеты"

    def __str__(self):
        return f"{self.resident} — {self.date}"

    def is_filled(self) -> bool:
        """
        Проверяет, заполнены ли все необходимые поля отчёта.
        Используется в UI для отображения состояния карточки.
        """
        return all([
            self.emotional_state is not None,
            self.physical_state is not None,
            self.motivation is not None,
            self.daily_dynamics is not None,
            self.comment.strip() != "",
            self.mrp_activity is not None,
            self.family_activity is not None,
            self.positive_traits.exists() or self.negative_traits.exists()
        ])