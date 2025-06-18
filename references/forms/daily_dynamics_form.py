from django import forms
from ..models.daily_dynamics import DailyDynamics

class DailyDynamicsForm(forms.ModelForm):
    """
    Форма для создания и редактирования DailyDynamics.
    """
    class Meta:
        model = DailyDynamics
        fields = ["name", "score", "is_active"]