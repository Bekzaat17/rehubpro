#tasks/models/task_template.py
from django.db import models
from tasks.enums.task_type import TaskType

class TaskTemplate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=50, choices=TaskType.choices)

    def __str__(self):
        return self.title