from ..factories.base_factory import BaseReferenceFactory
from ...models.physical_state import PhysicalState
from ...forms.physical_state_form import PhysicalStateForm

class PhysicalStateFactory(BaseReferenceFactory):
    def get_model(self):
        return PhysicalState

    def get_form(self):
        return PhysicalStateForm

    def get_verbose_name(self):
        return "Физическое состояние"

    def get_columns(self):
        return ["name", "score", "is_active"]