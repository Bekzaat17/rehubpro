from .base_reference_item import BaseReferenceItem

class PhysicalState(BaseReferenceItem):
    """
    Физическое состояние резидента.
    Например: Хорошее, Жалобы на здоровье и т.д.
    """
    class Meta:
        verbose_name = "Физическое состояние"
        verbose_name_plural = "Физические состояния"