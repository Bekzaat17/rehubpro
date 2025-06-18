from django import forms
from ..models.character_trait import CharacterTrait

class CharacterTraitForm(forms.ModelForm):
    """
    Форма для создания и редактирования черт характера.
    Используется во view и передаётся через фабрику.
    """
    class Meta:
        model = CharacterTrait
        fields = ["name", "is_active"]