from django.db import models
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

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"