from django import forms
from ..models.mrp_activity import MrpActivity

class MrpActivityForm(forms.ModelForm):
    """
    Форма для справочника Активность в МРП.
    """
    class Meta:
        model = MrpActivity
        fields = ["name", "score", "is_active"]