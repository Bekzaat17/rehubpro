from django.db import models

from reports.models.resident_report import ResidentReport
from roles.models.resident_role_assignment import ResidentRoleAssignment


class ResidentReportRoleStatus(models.Model):
    """
    Связь между отчётом и активными ролями резидента, с оценкой ответственности.
    Используется для аналитики и отслеживания участия в функциях.
    """

    RESPONSIBILITY_CHOICES = [
        ("responsible", "Ответственный"),
        ("irresponsible", "Безответственный"),
    ]

    report = models.ForeignKey(
        ResidentReport,
        on_delete=models.CASCADE,
        related_name="role_statuses"
    )
    role_assignment = models.ForeignKey(
        ResidentRoleAssignment,
        on_delete=models.CASCADE,
        help_text="Активное назначение роли резиденту"
    )
    status = models.CharField(
        max_length=20,
        choices=RESPONSIBILITY_CHOICES,
        default="responsible"
    )

    class Meta:
        unique_together = ("report", "role_assignment")
        verbose_name = "Оценка роли резидента"
        verbose_name_plural = "Оценки ролей резидента"

    def __str__(self):
        return f"{self.role_assignment} — {self.get_status_display()}"