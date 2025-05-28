# rehabpro/references/models/resident_function.py

from django.db import models
from .base_reference_item import BaseReferenceItem

class ResidentFunction(BaseReferenceItem):
    """
    Назначаемая функция резидента (айболит, физорг и т.д.)
    """
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Функция резидента"
        verbose_name_plural = "Функции резидентов"