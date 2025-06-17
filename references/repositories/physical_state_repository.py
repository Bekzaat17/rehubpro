
from abc import abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID
from django.db.models import QuerySet # Ensure QuerySet is imported
from core.patterns.repository import AbstractRepository
from references.models.physical_state import PhysicalState

if TYPE_CHECKING:
    from django.db.models import QuerySet

class PhysicalStateRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[PhysicalState]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[PhysicalState]: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[PhysicalState]: pass
    @abstractmethod
    def list_all(self) -> Sequence[PhysicalState]: pass
    @abstractmethod
    def add(self, physical_state: PhysicalState) -> PhysicalState: pass
    @abstractmethod
    def update(self, physical_state: PhysicalState) -> PhysicalState: pass
    @abstractmethod
    def delete(self, physical_state: PhysicalState) -> None: pass

class DjangoPhysicalStateRepository(PhysicalStateRepository):
    def get_by_id(self, id: UUID) -> Optional[PhysicalState]:
        try: return PhysicalState.objects.get(id=id)
        except PhysicalState.DoesNotExist: return None
    def get_by_slug(self, slug: str) -> Optional[PhysicalState]:
        try: return PhysicalState.objects.get(slug=slug)
        except PhysicalState.DoesNotExist: return None
    def get_by_name(self, name: str) -> Optional[PhysicalState]:
        try: return PhysicalState.objects.get(name=name)
        except PhysicalState.DoesNotExist: return None
    def list_all(self) -> 'QuerySet[PhysicalState]': # Added quotes for forward ref if TYPE_CHECKING not enough
        return PhysicalState.objects.all()
    def add(self, physical_state: PhysicalState) -> PhysicalState:
        physical_state.save(); return physical_state
    def update(self, physical_state: PhysicalState) -> PhysicalState:
        physical_state.save(); return physical_state
    def delete(self, physical_state: PhysicalState) -> None:
        physical_state.delete()
