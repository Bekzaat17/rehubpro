from django.views import View
from django.shortcuts import render
from django.contrib.auth import get_user_model
from notifications.notification_service import NotificationService

User = get_user_model()


class DevPanelView(View):
    def get(self, request):
        return render(request, "test/dev_panel.html")

    def post(self, request):
        action = request.POST.get("action")
        result = None
        error = None

        try:
            if action == "send_notification":
                NotificationService().send(
                    user=request.user,
                    title="🔔 Проверка уведомлений",
                    message="Это тестовое уведомление из DevPanel!"
                )
                result = "✅ Уведомление успешно отправлено!"
            else:
                error = "Неизвестное действие"
        except Exception as e:
            error = str(e)

        return render(request, "test/dev_panel.html", {
            "result": result,
            "error": error,
        })