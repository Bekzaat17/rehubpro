from django.db import models


class ActiveResidentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)