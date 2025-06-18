from .base_reference_item import BaseReferenceItem
from .mixins.scorable_mixin import ScorableMixin


class EmotionalState(ScorableMixin, BaseReferenceItem):
    """
    Эмоциональное состояние резидента.
    Например: Ровное, Возбуждённое, Агрессивное и т.д.
    """
    class Meta:
        verbose_name = "Эмоциональное состояние"
        verbose_name_plural = "Эмоциональные состояния"