from django.contrib.auth import get_user_model
from licenses.services.license_service import LicenseService
from notifications.services.notification_service import NotificationService

User = get_user_model()


class LicenseNotifier:
    """
    Проверяет лицензию и уведомляет админов.
    """

    def run(self):
        status = LicenseService.get_status()
        days_left = LicenseService.get_days_left()

        if status not in ('warning', 'grace'):
            return

        if status == 'warning':
            message = f"⚠️ Срок действия лицензии истекает через {days_left} дн. Продлите её."
        elif status == 'grace':
            message = (
                f"❗ Лицензия истекла. Система работает в аварийном режиме. "
                f"Осталось {days_left} дн. до полной блокировки."
            )

        for user in self.get_admin_users():
            NotificationService().send(
                user=user,
                title="Срок действия лицензии",
                message=message
            )

    def get_admin_users(self):
        return User.objects.filter(is_staff=True, is_active=True)