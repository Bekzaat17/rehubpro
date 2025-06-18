from .base_reference_view import BaseReferenceView
from ..models.emotional_state import EmotionalState
from ..forms.emotional_state_form import EmotionalStateForm

class EmotionalStateView(BaseReferenceView):
    """
    API-вьюха для справочника Эмоциональных состояний.
    """
    model = EmotionalState
    form_class = EmotionalStateForm