# users/models/enums.py
from django.db import models

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Администратор'
    CONSULTANT = 'consultant', 'Консультант'
    PSYCHOLOGIST = 'psychologist', 'Психолог'