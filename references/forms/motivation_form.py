from django import forms
from ..models.motivation import Motivation

class MotivationForm(forms.ModelForm):
    """
    Форма для справочника Мотивация.
    """
    class Meta:
        model = Motivation
        fields = ["name", "score", "is_active"]