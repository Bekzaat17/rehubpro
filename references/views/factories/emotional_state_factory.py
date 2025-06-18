from ..factories.base_factory import BaseReferenceFactory
from ...models.emotional_state import EmotionalState
from ...forms.emotional_state_form import EmotionalStateForm

class EmotionalStateFactory(BaseReferenceFactory):
    def get_model(self):
        return EmotionalState

    def get_form(self):
        return EmotionalStateForm

    def get_verbose_name(self):
        return "Эмоциональные состояния"

    def get_columns(self):
        return ["name", "score", "is_active"]