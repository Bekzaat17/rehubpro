# lectures/models/lecture_category.py

from django.db import models

class LectureCategory(models.Model):
    """
    Категория лекций (например, 'Зависимости', 'Созависимость', 'Мотивация').
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория лекции"
        verbose_name_plural = "Категории лекций"