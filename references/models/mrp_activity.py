from .base_reference_item import BaseReferenceItem

class MrpActivity(BaseReferenceItem):
    """
    Активность резидента на МРП.
    Например: Активен, Пассивен, Безучастен.
    """
    class Meta:
        verbose_name = "Активность на МРП"
        verbose_name_plural = "Активность на МРП"