# /references/models/base_reference_item.py

from django.db import models
from uuid import uuid4

class BaseReferenceItem(models.Model):
    """
    Абстрактная базовая модель для всех справочных значений.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name