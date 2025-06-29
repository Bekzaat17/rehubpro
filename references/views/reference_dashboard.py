from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .factories.character_trait_defect_factory import CharacterTraitDefectFactory
from .factories.character_trait_strength_factory import CharacterTraitStrengthFactory
from .factories.daily_dynamics_factory import DailyDynamicsFactory
from .factories.emotional_state_factory import EmotionalStateFactory
from .factories.family_activity_factory import FamilyActivityFactory
from .factories.motivation_factory import MotivationFactory
from .factories.mrp_activity_factory import MrpActivityFactory
from .factories.physical_state_factory import PhysicalStateFactory


class ReferenceDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "references/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Регистрируем нужные справочники
        factories = [
            CharacterTraitStrengthFactory(),
            CharacterTraitDefectFactory(),
            DailyDynamicsFactory(),
            EmotionalStateFactory(),
            MotivationFactory(),
            FamilyActivityFactory(),
            MrpActivityFactory(),
            PhysicalStateFactory(),
        ]

        # Генерируем вкладки из фабрик
        context["reference_tabs"] = [
            {
                "slug": factory.get_slug(),  # ✅ важно — уникальные slug-и
                "verbose": factory.get_verbose_name(),
                "columns": factory.get_columns(),
                "trait_type": getattr(factory, "get_trait_type", lambda: None)()  # ✅ только для CharacterTrait
            }
            for factory in factories
        ]

        return context