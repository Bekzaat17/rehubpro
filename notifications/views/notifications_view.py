# notifications/views/notifications_view.py

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from notifications.models import Notification


@login_required
def unread_count_view(request):
    """
    Возвращает количество непрочитанных уведомлений текущего пользователя.
    """
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread': count})


@require_POST
@login_required
def mark_as_read_view(request):
    """
    Помечает конкретное уведомление как прочитанное.
    Ожидает POST с полем 'id'.
    """
    notif_id = request.POST.get("id")
    if not notif_id:
        return JsonResponse({"success": False, "error": "ID не передан"}, status=400)

    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
        notif.is_read = True
        notif.save()
        return JsonResponse({"success": True})
    except Notification.DoesNotExist:
        return JsonResponse({"success": False, "error": "Уведомление не найдено"}, status=404)

@require_GET
@login_required
def unread_notifications_view(request):
    """
    Возвращает список непрочитанных уведомлений для текущего пользователя.
    """
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')

    return JsonResponse({
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for n in notifications
        ]
    })