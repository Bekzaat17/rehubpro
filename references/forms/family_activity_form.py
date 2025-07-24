from django import forms
from ..models.family_activity import FamilyActivity

class FamilyActivityForm(forms.ModelForm):
    """
    Форма для справочника Активность с семье.
    """
    class Meta:
        model = FamilyActivity
        fields = ["name", "score", "is_active"]