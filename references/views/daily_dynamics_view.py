from .base_reference_view import BaseReferenceView
from ..models.daily_dynamics import DailyDynamics
from ..forms.daily_dynamics_form import DailyDynamicsForm

class DailyDynamicsView(BaseReferenceView):
    """
    API-вьюха для справочника DailyDynamics.
    """
    model = DailyDynamics
    form_class = DailyDynamicsForm