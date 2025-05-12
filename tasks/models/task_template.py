# tasks/models/task_template.py

from django.db import models
from django.conf import settings

class TaskTemplate(models.Model):
    class TaskType(models.TextChoices):
        TEST = 'test', 'Тест'
        SHORT_TERM = 'short_term', 'Краткосрочное'
        LONG_TERM = 'long_term', 'Долгосрочное'

    title = models.CharField(max_length=255)
    description = models.TextField()
    task_type = models.CharField(max_length=20, choices=TaskType.choices)  # ✅ добавили поле типа
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ добавили поле даты

    def __str__(self):
        return self.title