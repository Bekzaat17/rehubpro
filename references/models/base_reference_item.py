# /references/models/base_reference_item.py

from django.db import models
from uuid import uuid4
from slugify import slugify

class BaseReferenceItem(models.Model):
    """
    Абстрактная базовая модель для всех справочников.
    Общие поля:
    - id: UUID
    - name: Название элемента справочника
    - slug: Уникальный slug, формируемый из name
    - is_active: Для soft-delete
    - created_at / updated_at: Тех. информация
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField("Название", max_length=255, unique=True)
    slug = models.SlugField("Слаг", max_length=255, unique=True, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def save(self, *args, **kwargs):
        """
        Автоматически формирует slug при первом сохранении,
        если он не был указан вручную.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name