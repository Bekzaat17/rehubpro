from django.urls import path

from .views.daily_dynamics_view import DailyDynamicsView
from .views.emotional_state_view import EmotionalStateView
from .views.family_activity_view import FamilyActivityView
from .views.motivation_view import MotivationView
from .views.mrp_activity_view import MrpActivityView
from .views.physical_state_view import PhysicalStateView
from .views.reference_dashboard import ReferenceDashboardView
from .views.character_trait_view import CharacterTraitView  # API

app_name = "references"


urlpatterns = [
    path("dashboard/", ReferenceDashboardView.as_view(), name="reference_dashboard"),
    path("api/charactertrait/", CharacterTraitView.as_view(), name="character_trait_api"),
    path("api/dailydynamics/", DailyDynamicsView.as_view(), name="daily_dynamics_api"),
    path("api/emotionalstate/", EmotionalStateView.as_view(), name="emotional_state_api"),
    path("api/motivation/", MotivationView.as_view(), name="motivation_api"),
    path("api/familyactivity/", FamilyActivityView.as_view(), name="family_activity_api"),
    path("api/mrpactivity/", MrpActivityView.as_view(), name="mrp_activity_api"),
    path("api/physicalstate/", PhysicalStateView.as_view(), name="physical_state_api"),
]