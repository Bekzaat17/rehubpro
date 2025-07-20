from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationSender(ABC):
    """
    Абстрактная стратегия отправки уведомлений.
    """

    @abstractmethod
    def send(self, user: User, title: str, message: str) -> None:
        pass