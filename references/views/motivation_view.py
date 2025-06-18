from .base_reference_view import BaseReferenceView
from ..models.motivation import Motivation
from ..forms.motivation_form import MotivationForm

class MotivationView(BaseReferenceView):
    """
    API-вьюха для справочника Мотивация.
    """
    model = Motivation
    form_class = MotivationForm