from .base_reference_item import BaseReferenceItem
from .mixins.scorable_mixin import ScorableMixin

#TODO from django.utils.translation import gettext_lazy as _ vezde sdelat localizaciu


class MrpActivity(ScorableMixin, BaseReferenceItem):
    """
    Активность резидента на МРП.
    Например: Активен, Пассивен, Безучастен.
    """
    class Meta:
        verbose_name = "Активность на МРП"
        verbose_name_plural = "Активность на МРП"