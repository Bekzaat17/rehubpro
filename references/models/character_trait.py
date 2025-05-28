from django.db import models
from django.utils.text import slugify
from .base_reference_item import BaseReferenceItem


class TraitType(models.TextChoices):
    STRENGTH = 'strength', 'Достоинство'
    DEFECT = 'defect', 'Дефект'


class CharacterTrait(BaseReferenceItem):
    """
    Черта характера: может быть достоинством или дефектом.
    """
    type = models.CharField(
        max_length=10,
        choices=TraitType.choices,
        default=TraitType.DEFECT
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Уникальный идентификатор для использования в коде, API и шаблонах"
    )

    class Meta:
        verbose_name = "Черта характера"
        verbose_name_plural = "Черты характера"

    def save(self, *args, **kwargs):
        # Если slug не установлен, генерируем из name
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while CharacterTrait.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"