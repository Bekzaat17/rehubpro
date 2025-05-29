from django.db import models
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
        verbose_name = "Функция резидента"
        verbose_name_plural = "Функции резидентов"

    def __str__(self):
        return self.name