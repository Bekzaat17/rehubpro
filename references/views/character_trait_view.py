from .base_reference_view import BaseReferenceView
from ..models.character_trait import CharacterTrait
from ..forms.character_trait_form import CharacterTraitForm

class CharacterTraitView(BaseReferenceView):
    """
    API-вьюха для справочника 'Чертa характера'.
    Обрабатывает GET, POST, DELETE.
    """
    model = CharacterTrait
    form_class = CharacterTraitForm