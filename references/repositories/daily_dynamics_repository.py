
from abc import abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID
from django.db.models import QuerySet # Ensure QuerySet is imported
from core.patterns.repository import AbstractRepository
from references.models.daily_dynamics import DailyDynamics

if TYPE_CHECKING:
    from django.db.models import QuerySet

class DailyDynamicsRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[DailyDynamics]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[DailyDynamics]: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[DailyDynamics]: pass
    @abstractmethod
    def list_all(self) -> Sequence[DailyDynamics]: pass
    @abstractmethod
    def add(self, daily_dynamics: DailyDynamics) -> DailyDynamics: pass
    @abstractmethod
    def update(self, daily_dynamics: DailyDynamics) -> DailyDynamics: pass
    @abstractmethod
    def delete(self, daily_dynamics: DailyDynamics) -> None: pass

class DjangoDailyDynamicsRepository(DailyDynamicsRepository):
    def get_by_id(self, id: UUID) -> Optional[DailyDynamics]:
        try: return DailyDynamics.objects.get(id=id)
        except DailyDynamics.DoesNotExist: return None
    def get_by_slug(self, slug: str) -> Optional[DailyDynamics]:
        try: return DailyDynamics.objects.get(slug=slug)
        except DailyDynamics.DoesNotExist: return None
    def get_by_name(self, name: str) -> Optional[DailyDynamics]:
        try: return DailyDynamics.objects.get(name=name)
        except DailyDynamics.DoesNotExist: return None
    def list_all(self) -> 'QuerySet[DailyDynamics]': # Added quotes for forward ref if TYPE_CHECKING not enough
        return DailyDynamics.objects.all()
    def add(self, daily_dynamics: DailyDynamics) -> DailyDynamics:
        daily_dynamics.save(); return daily_dynamics
    def update(self, daily_dynamics: DailyDynamics) -> DailyDynamics:
        daily_dynamics.save(); return daily_dynamics
    def delete(self, daily_dynamics: DailyDynamics) -> None:
        daily_dynamics.delete()
