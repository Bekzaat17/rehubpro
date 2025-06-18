from .base_reference_view import BaseReferenceView
from ..models.physical_state import PhysicalState
from ..forms.physical_state_form import PhysicalStateForm

class PhysicalStateView(BaseReferenceView):
    """
    API-вьюха для справочника Физическое состояние.
    """
    model = PhysicalState
    form_class = PhysicalStateForm