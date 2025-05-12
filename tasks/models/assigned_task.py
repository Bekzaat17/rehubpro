# tasks/models/assigned_task.py

from django.db import models
from django.conf import settings  # импортируем настройки для модели пользователя
from .task_template import TaskTemplate
from residents.models import Resident

class AssignedTask(models.Model):
    template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # используем AUTH_USER_MODEL
    given_date = models.DateField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.template.title} для {self.resident.name}'