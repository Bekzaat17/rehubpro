from .character_trait_repository import CharacterTraitRepository, DjangoCharacterTraitRepository
from .daily_dynamics_repository import DailyDynamicsRepository, DjangoDailyDynamicsRepository
from .emotional_state_repository import EmotionalStateRepository, DjangoEmotionalStateRepository
from .family_activity_repository import FamilyActivityRepository, DjangoFamilyActivityRepository
from .motivation_repository import MotivationRepository, DjangoMotivationRepository
from .mrp_activity_repository import MrpActivityRepository, DjangoMrpActivityRepository
from .physical_state_repository import PhysicalStateRepository, DjangoPhysicalStateRepository
from .resident_role_repository import ResidentRoleRepository as ReferenceResidentRoleRepository # Alias to avoid name clashes
from .resident_role_repository import DjangoResidentRoleRepository as DjangoReferenceResidentRoleRepository # Alias

__all__ = [
    "CharacterTraitRepository", "DjangoCharacterTraitRepository",
    "DailyDynamicsRepository", "DjangoDailyDynamicsRepository",
    "EmotionalStateRepository", "DjangoEmotionalStateRepository",
    "FamilyActivityRepository", "DjangoFamilyActivityRepository",
    "MotivationRepository", "DjangoMotivationRepository",
    "MrpActivityRepository", "DjangoMrpActivityRepository",
    "PhysicalStateRepository", "DjangoPhysicalStateRepository",
    "ReferenceResidentRoleRepository", "DjangoReferenceResidentRoleRepository",
]
