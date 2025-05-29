from .base_reference_item import BaseReferenceItem

class Motivation(BaseReferenceItem):
    """
    Мотивация на выздоровление.
    Например: Положительная, Вынужденная, Нулевая и т.д.
    """
    class Meta:
        verbose_name = "Мотивация"
        verbose_name_plural = "Мотивации"