from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subfolders'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'

    def __str__(self):
        return self.name

    def is_root(self):
        return self.parent is None

    def get_ancestors(self):
        """
        Возвращает список родительских папок от корня до текущего.
        """
        folder = self
        ancestors = []
        while folder.parent:
            folder = folder.parent
            ancestors.insert(0, folder)  # prepend
        return ancestors