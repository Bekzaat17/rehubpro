#tasks/models/assigned_task.py
from django.db import models
from django.contrib.auth import get_user_model
from .task_template import TaskTemplate
from residents.models import Resident

User = get_user_model()


class AssignedTask(models.Model):
    """
    Конкретное задание, назначенное резиденту.
    Содержит ключевые даты прохождения и ссылку на шаблон задания.
    """
    class Status(models.TextChoices):
        WRITING = "writing", "Пишет"
        SUBMITTING = "submitting", "Сдаёт"
        COMPLETED = "completed", "Завершено"

    task = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name="assigned_tasks")
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="assigned_tasks")
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks")

    assigned_at = models.DateTimeField(auto_now_add=True)

    writing_started = models.DateField(null=True, blank=True, help_text="Дата начала написания задания")
    writing_finished = models.DateField(null=True, blank=True, help_text="Дата завершения написания")
    submitting_started = models.DateField(null=True, blank=True, help_text="Дата начала сдачи")
    completed_at = models.DateField(null=True, blank=True, help_text="Дата полного завершения задания")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.WRITING)

    class Meta:
        verbose_name = "Назначенное задание"
        verbose_name_plural = "Назначенные задания"
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.task.title} → {self.resident.full_name}"