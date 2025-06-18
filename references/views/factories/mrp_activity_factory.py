from ..factories.base_factory import BaseReferenceFactory
from ...models.mrp_activity import MrpActivity
from ...forms.mrp_activity_form import MrpActivityForm

class MrpActivityFactory(BaseReferenceFactory):
    def get_model(self):
        return MrpActivity

    def get_form(self):
        return MrpActivityForm

    def get_verbose_name(self):
        return "Активность в МРП"

    def get_columns(self):
        return ["name", "score", "is_active"]