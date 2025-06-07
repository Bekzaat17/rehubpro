#tasks/enums/task_type.py
from django.db import models

class TaskType(models.TextChoices):
    SHORT_TERM = 'short_term', 'Краткосрочное'
    LONG_TERM = 'long_term', 'Долгосрочное'
    TEST = 'test', 'Тестовое'