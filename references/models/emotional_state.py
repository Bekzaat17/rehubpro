from .base_reference_item import BaseReferenceItem

class EmotionalState(BaseReferenceItem):
    """
    Эмоциональное состояние резидента.
    Например: Ровное, Возбуждённое, Агрессивное и т.д.
    """
    class Meta:
        verbose_name = "Эмоциональное состояние"
        verbose_name_plural = "Эмоциональные состояния"