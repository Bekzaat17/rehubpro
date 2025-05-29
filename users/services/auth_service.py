from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from typing import Optional


class AuthenticateUserService:
    """
    Use-case: Авторизация пользователя по логину и паролю.
    """

    @staticmethod
    def execute(username: str, password: str) -> Optional[AbstractUser]:
        user = authenticate(username=username, password=password)
        return user