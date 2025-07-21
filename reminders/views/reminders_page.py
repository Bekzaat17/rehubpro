# reminders/views/reminders_page.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from reminders.models.reminder import Reminder
from reminders.forms.reminder_form import ReminderForm


class RemindersPageView(LoginRequiredMixin, TemplateView):
    template_name = "reminders/reminders_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReminderForm()
        context['reminders'] = Reminder.objects.filter(user=self.request.user).order_by('datetime')
        return context