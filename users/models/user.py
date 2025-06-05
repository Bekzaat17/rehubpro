# users/models/user.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
from .enums import UserRole


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CONSULTANT
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username