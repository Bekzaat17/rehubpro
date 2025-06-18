from ...models.character_trait import CharacterTrait
from ...forms.character_trait_form import CharacterTraitForm
from .base_factory import BaseReferenceFactory

class CharacterTraitFactory(BaseReferenceFactory):
    def get_model(self):
        return CharacterTrait

    def get_form(self):
        return CharacterTraitForm

    def get_verbose_name(self):
        return "Черты характера"

    def get_columns(self):
        return ["name", "type", "is_active"]