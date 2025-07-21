from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from reminders.forms.reminder_form import ReminderForm
from reminders.models.reminder import Reminder
from reminders.services.reminder_creator import ReminderCreator


@login_required
@require_POST
def create_reminder(request):
    reminder_id = request.GET.get("id")
    instance = Reminder.objects.filter(pk=reminder_id, user=request.user).first() if reminder_id else None

    form = ReminderForm(request.POST, instance=instance)
    if form.is_valid():
        service = ReminderCreator(request.user)
        if instance:
            service.update(instance, form.cleaned_data)
        else:
            service.create(form.cleaned_data)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def delete_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.delete()
    return JsonResponse({"success": True})


@login_required
@require_http_methods(["GET"])
def get_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    return JsonResponse({
        "id": reminder.id,
        "title": reminder.title,
        "text": reminder.text,
        "datetime": reminder.datetime.isoformat(),
        "repeat": reminder.repeat,
        "is_active": reminder.is_active
    })


@login_required
def reminders_list_partial(request):
    reminders = Reminder.objects.filter(user=request.user).order_by('datetime')
    return render(request, "reminders/_reminder_table.html", {"reminders": reminders})