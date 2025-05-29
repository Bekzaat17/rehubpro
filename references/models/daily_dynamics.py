from .base_reference_item import BaseReferenceItem

class DailyDynamics(BaseReferenceItem):
    """
    Оценка динамики в течение дня.
    Например: Положительная, Стабильная, Негативная.
    """
    class Meta:
        verbose_name = "Динамика"
        verbose_name_plural = "Динамика"