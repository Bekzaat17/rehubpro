#tasks/models/task_progress.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from .assigned_task import AssignedTask

User = get_user_model()


class TaskProgress(models.Model):
    """
    История выполнения назначенного задания резидентом.
    Каждая запись отражает этап и комментарий консультанта.
    """
    class Stage(models.TextChoices):
        WRITING = "writing", "Пишет"
        SUBMITTING = "submitting", "Сдаёт"
        COMPLETED = "completed", "Завершено"

    assigned_task = models.ForeignKey(AssignedTask, on_delete=models.CASCADE, related_name="progress_entries")
    stage = models.CharField(max_length=20, choices=Stage.choices)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="task_progress_updates")

    class Meta:
        verbose_name = "Прогресс по заданию"
        verbose_name_plural = "Прогресс по заданиям"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.assigned_task} → {self.get_stage_display()} [{self.created_at.date()}]"