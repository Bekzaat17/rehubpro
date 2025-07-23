from django.shortcuts import redirect
from django.urls import resolve, reverse, NoReverseMatch
from licenses.services.license_service import LicenseService


class LicenseCheckMiddleware:
    """
    Проверка статуса лицензии. Если expired — блокируем доступ.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Разрешаем доступ к статике и админке
        try:
            license_expired_url = reverse("licenses:license_expired")
        except NoReverseMatch:
            license_expired_url = "/license/expired/"  # запасной путь

        allowed_paths = [
            "/static/",
            reverse("admin:login"),
            license_expired_url,
        ]

        # Не проверяем лицензии для разрешённых путей
        if request.path.startswith("/static/") or any(request.path.startswith(p) for p in allowed_paths):
            return self.get_response(request)

        # Проверка лицензии
        if LicenseService.get_status() == "expired":
            return redirect(license_expired_url)

        return self.get_response(request)