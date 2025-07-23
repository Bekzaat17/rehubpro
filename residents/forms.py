from django import forms
from residents.models import Resident


class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = [
            'last_name',
            'first_name',
            'middle_name',
            'date_of_birth',
            'date_of_admission',
            'dependency_type',
            'identical_number',
            'notes',
            'is_active',
            'status',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_admission': forms.DateInput(attrs={'type': 'date'}),
        }