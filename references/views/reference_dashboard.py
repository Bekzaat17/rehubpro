from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .factories.character_trait_factory import CharacterTraitFactory
from .factories.daily_dynamics_factory import DailyDynamicsFactory
from .factories.emotional_state_factory import EmotionalStateFactory
from .factories.family_activity_factory import FamilyActivityFactory
from .factories.motivation_factory import MotivationFactory
from .factories.mrp_activity_factory import MrpActivityFactory
from .factories.physical_state_factory import PhysicalStateFactory


# Можно добавить другие фабрики

class ReferenceDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "references/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Регистрируем нужные справочники
        factories = [
            CharacterTraitFactory(),
            DailyDynamicsFactory(),
            EmotionalStateFactory(),
            MotivationFactory(),
            FamilyActivityFactory(),
            MrpActivityFactory(),
            PhysicalStateFactory(),
        ]

        context["reference_tabs"] = [
            {
                "slug": factory.get_model().__name__.lower(),
                "verbose": factory.get_verbose_name(),
                "columns": factory.get_columns(),
            }
            for factory in factories
        ]
        return context