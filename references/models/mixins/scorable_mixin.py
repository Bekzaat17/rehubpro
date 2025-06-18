from django.db import models

class ScorableMixin(models.Model):
    """
    Миксин для добавления числового поля score.
    Используется для справочников, где важен количественный показатель.
    """
    score = models.IntegerField("Оценка", default=0)

    class Meta:
        abstract = True