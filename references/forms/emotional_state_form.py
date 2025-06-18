from django import forms
from ..models.emotional_state import EmotionalState

class EmotionalStateForm(forms.ModelForm):
    """
    Форма для создания и редактирования эмоционального состояния.
    """
    class Meta:
        model = EmotionalState
        fields = ["name", "score", "is_active"]