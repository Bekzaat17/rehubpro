from django.db import models
from django.utils.translation import gettext_lazy as _

class DependencyType(models.TextChoices):
    ALCOHOL = "F10", _("Алкогольная зависимость (F10)")
    OPIOIDS = "F11", _("Опиоидная зависимость (F11)")
    CANNABIS = "F12", _("Каннабиноидная зависимость (F12)")
    SEDATIVES = "F13", _("Седативная зависимость (F13)")
    COCAINE = "F14", _("Кокаиновая зависимость (F14)")
    STIMULANTS = "F15", _("Психостимуляторы (F15)")
    SCHIZOTYPAL = "F21", _("Шизотипическое расстройство (F21)")
    MULTIPLE = "F19", _("Множественные зависимости (F19)")
    OTHER = "OTHER", _("Другое")