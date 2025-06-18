from .base_reference_view import BaseReferenceView
from ..models.mrp_activity import MrpActivity
from ..forms.mrp_activity_form import MrpActivityForm

class MrpActivityView(BaseReferenceView):
    """
    API-вьюха для справочника Активность в МРП.
    """
    model = MrpActivity
    form_class = MrpActivityForm