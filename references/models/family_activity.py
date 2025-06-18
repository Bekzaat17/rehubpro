from .base_reference_item import BaseReferenceItem
from .mixins.scorable_mixin import ScorableMixin


class FamilyActivity(ScorableMixin, BaseReferenceItem):
    """
    Активность резидента в семье.
    Например: Активен, Пассивен, Уклоняется и т.д.
    """
    class Meta:
        verbose_name = "Активность в семье"
        verbose_name_plural = "Активность в семье"