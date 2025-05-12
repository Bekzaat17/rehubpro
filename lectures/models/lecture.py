from django.db import models
from django.conf import settings
from .lecture_category import LectureCategory


class Lecture(models.Model):
    """
    Модель лекции, которую администратор или специалист может добавить
    через админку. Лекция может содержать текст, файл и/или ссылку на видео.
    """

    title = models.CharField(
        max_length=255,
        verbose_name="Название"
    )  # Заголовок лекции

    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )  # Краткое описание лекции (необязательное)

    content = models.TextField(
        verbose_name="Содержание (HTML или Markdown)"
    )  # Основной текст лекции, может быть в формате Markdown или HTML

    file = models.FileField(
        upload_to="lectures/files/",
        blank=True,
        null=True,
        verbose_name="Файл (PDF, DOC и т.д.)"
    )  # Прикреплённый файл (например, презентация, текст лекции)

    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео (YouTube и т.п.)"
    )  # Ссылка на видео-лекцию (необязательное поле)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )  # Дата и время создания лекции

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Создано пользователем"
    )  # Автор лекции (тот, кто создал — обычно консультант или админ)

    category = models.ForeignKey(
        LectureCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lectures',
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"

    def __str__(self):
        return self.title  # Отображение объекта в админке и других интерфейсах