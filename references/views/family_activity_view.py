from .base_reference_view import BaseReferenceView
from ..models.family_activity import FamilyActivity
from ..forms.family_activity_form import FamilyActivityForm

class FamilyActivityView(BaseReferenceView):
    """
    API-вьюха для справочника Активность с семье.
    """
    model = FamilyActivity
    form_class = FamilyActivityForm