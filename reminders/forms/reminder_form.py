# reminders/forms/reminder_form.py
from django import forms
from reminders.models.reminder import Reminder
from reminders.enums import RepeatInterval


class ReminderForm(forms.ModelForm):
    datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Когда напомнить"
    )

    class Meta:
        model = Reminder
        fields = ['title', 'text', 'datetime', 'repeat', 'is_active']
        labels = {
            'title': 'Заголовок',
            'text': 'Описание',
            'repeat': 'Повтор',
            'is_active': 'Активно?',
        }