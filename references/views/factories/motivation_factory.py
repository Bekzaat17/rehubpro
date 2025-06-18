from ..factories.base_factory import BaseReferenceFactory
from ...models.motivation import Motivation
from ...forms.motivation_form import MotivationForm

class MotivationFactory(BaseReferenceFactory):
    def get_model(self):
        return Motivation

    def get_form(self):
        return MotivationForm

    def get_verbose_name(self):
        return "Мотивация"

    def get_columns(self):
        return ["name", "score", "is_active"]