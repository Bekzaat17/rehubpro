from ..factories.base_factory import BaseReferenceFactory
from ...models.daily_dynamics import DailyDynamics
from ...forms.daily_dynamics_form import DailyDynamicsForm

class DailyDynamicsFactory(BaseReferenceFactory):
    def get_model(self):
        return DailyDynamics

    def get_form(self):
        return DailyDynamicsForm

    def get_verbose_name(self):
        return "Ежедневная динамика"

    def get_columns(self):
        return ["name", "score", "is_active"]