# /references/models/base_reference_item.py

from django.db import models
from uuid import uuid4
from slugify import slugify

class BaseReferenceItem(models.Model):
    """
    Абстрактная базовая модель для всех справочных значений.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            Model = self.__class__
            while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name