from django import forms
from ..models.physical_state import PhysicalState

class PhysicalStateForm(forms.ModelForm):
    """
    Форма для справочника Физическое состояние.
    """
    class Meta:
        model = PhysicalState
        fields = ["name", "score", "is_active"]