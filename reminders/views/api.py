# reminders/views/api.py
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from reminders.forms.reminder_form import ReminderForm
from reminders.models.reminder import Reminder
from reminders.services.reminder_creator import ReminderCreator


@login_required
@require_POST
def create_reminder(request):
    form = ReminderForm(request.POST)
    if form.is_valid():
        ReminderCreator(request.user).create(form.cleaned_data)
    return redirect('reminders:reminders_page')


@login_required
@require_POST
def delete_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.delete()
    return redirect('reminders:reminders_page')