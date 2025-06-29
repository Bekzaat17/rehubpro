from django import forms
from ..models.character_trait import CharacterTrait, TraitType

class CharacterTraitForm(forms.ModelForm):
    """
    Форма для создания и редактирования черт характера.
    Поле type скрытое, заполняется из фабрики.
    """
    type = forms.ChoiceField(choices=TraitType.choices, widget=forms.HiddenInput())

    class Meta:
        model = CharacterTrait
        fields = ["name", "type", "is_active"]

    def __init__(self, *args, **kwargs):
        trait_type = kwargs.pop("trait_type", None)
        super().__init__(*args, **kwargs)
        if trait_type:
            self.fields["type"].initial = trait_type