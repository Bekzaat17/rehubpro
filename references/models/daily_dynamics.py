from .base_reference_item import BaseReferenceItem
from .mixins.scorable_mixin import ScorableMixin


class DailyDynamics(ScorableMixin, BaseReferenceItem):
    """
    Оценка динамики в течение дня.
    Например: Положительная, Стабильная, Негативная.
    """
    class Meta:
        verbose_name = "Динамика"
        verbose_name_plural = "Динамика"