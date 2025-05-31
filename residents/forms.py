from django import forms
from residents.models import Resident

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['full_name', 'date_of_birth', 'date_of_admission', 'dependency_type', 'notes']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_admission': forms.DateInput(attrs={'type': 'date'}),
        }