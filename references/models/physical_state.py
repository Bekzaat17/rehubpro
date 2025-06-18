from .base_reference_item import BaseReferenceItem
from .mixins.scorable_mixin import ScorableMixin


class PhysicalState(ScorableMixin, BaseReferenceItem):
    """
    Физическое состояние резидента.
    Например: Хорошее, Жалобы на здоровье и т.д.
    """
    class Meta:
        verbose_name = "Физическое состояние"
        verbose_name_plural = "Физические состояния"