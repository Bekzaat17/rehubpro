# roles/models/resident_role_assignment.py
from django.db import models
from uuid import uuid4
from residents.models.resident import Resident
from references.models.resident_role import ResidentRole


class ResidentRoleAssignment(models.Model):
    """
    Назначение роли (функции) резиденту на определённый период.
    Позволяет вести историю и учитывать активность.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    resident = models.ForeignKey(
        Resident,
        on_delete=models.CASCADE,
        related_name='role_assignments',
        verbose_name="Резидент"
    )

    role = models.ForeignKey(
        ResidentRole,
        on_delete=models.SET_NULL,
        null=True,  # роль может быть удалена, но история сохраняется
        blank=True,  # допускаем "без роли"
        related_name='assignments',
        verbose_name="Роль (функция)"
    )

    assigned_at = models.DateField(
        verbose_name="Дата назначения"
    )

    unassigned_at = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата завершения роли"
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий (необязательно)"
    )

    class Meta:
        verbose_name = "Назначение роли резиденту"
        verbose_name_plural = "Назначения ролей резидентам"
        ordering = ['-assigned_at']

    def __str__(self):
        role_name = self.role.name if self.role else "Без роли"
        return f"{self.resident} — {role_name} ({self.assigned_at})"

    def is_active(self):
        return self.unassigned_at is None