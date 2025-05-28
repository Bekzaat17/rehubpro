from django.db import models
from django.utils.text import slugify
from .base_reference_item import BaseReferenceItem


class ResidentRole(BaseReferenceItem):
    """
    Роль (функция), которая назначается резиденту.
    Например: айболит, президент, физорг и т.д.
    """

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Уникальный идентификатор для использования в коде, API и шаблонах"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Дополнительная информация о назначении или функциях роли."
    )

    class Meta:
        verbose_name = "Роль резидента"
        verbose_name_plural = "Роли резидентов"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while ResidentRole.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name