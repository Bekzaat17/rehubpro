from django.utils import timezone
from licenses.services.license_service import LicenseService


def global_variables(request):
    return {
        'PROJECT_NAME': 'RehubPro',
        'now': timezone.now(),
        'DATE_FORMAT': 'd.m.Y',  # Глобальный формат даты для шаблонов
    }


def license_banner(request):
    status = LicenseService.get_status()

    if status == 'warning':
        days_left = LicenseService.get_days_left()
        return {
            "license_status": status,
            "license_warning": f"⚠️ Срок действия лицензии истекает через {days_left} дней."
        }

    elif status == 'grace':
        return {
            "license_status": status,
            "license_warning": "⚠️ Внимание! Срок действия лицензии истёк."
        }

    elif status == 'expired':
        return {
            "license_status": status
            # ⛔ Никакого license_warning — покажется только overlay
        }

    return {}