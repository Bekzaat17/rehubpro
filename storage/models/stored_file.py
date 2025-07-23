import mimetypes
from django.db import models
from django.contrib.auth import get_user_model
from .folder import Folder

User = get_user_model()
#TODO nujno sdelat sborwik musora
class StoredFile(models.Model):
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name='files',
        null=True,
        blank=True,
        verbose_name="Папка",
    )
    file = models.FileField(upload_to='storage/')
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def mime_type(self):
        return mimetypes.guess_type(self.file.name)[0] or "application/octet-stream"

    @property
    def size_mb(self):
        return round(self.file.size / 1024 / 1024, 2) if self.file else 0

    @property
    def is_image(self):
        return self.mime_type.startswith("image/")

    @property
    def is_video(self):
        return self.mime_type.startswith("video/")

    @property
    def is_text(self):
        return self.mime_type.startswith("text/")

    @property
    def is_pdf(self):
        return self.mime_type == "application/pdf"

    @property
    def is_office(self):
        return self.mime_type in {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

    @property
    def is_previewable(self):
        return any([self.is_image, self.is_video, self.is_text, self.is_pdf, self.is_office])

    def get_readable_type(self):
        if self.mime_type.startswith("image/"):
            return "Изображение"
        elif self.mime_type.startswith("video/"):
            return "Видео"
        elif self.mime_type.startswith("audio/"):
            return "Аудио"
        elif self.mime_type.startswith("application/pdf"):
            return "PDF-документ"
        elif self.mime_type.startswith("application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
            return "Документ Word"
        elif self.mime_type.startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
            return "Таблица Excel"
        elif self.mime_type.startswith("application/zip"):
            return "Архив ZIP"
        elif self.mime_type.startswith("text/plain"):
            return "Текстовый файл"
        else:
            return "Файл"

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.name