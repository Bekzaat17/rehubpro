from ..factories.base_factory import BaseReferenceFactory
from ...models.family_activity import FamilyActivity
from ...forms.family_activity_form import FamilyActivityForm

class FamilyActivityFactory(BaseReferenceFactory):
    def get_model(self):
        return FamilyActivity

    def get_form(self):
        return FamilyActivityForm

    def get_verbose_name(self):
        return "Активность с семье"

    def get_columns(self):
        return ["name", "score", "is_active"]