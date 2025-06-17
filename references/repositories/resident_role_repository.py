
from abc import abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID
from django.db.models import QuerySet # Ensure QuerySet is imported
from core.patterns.repository import AbstractRepository
from references.models.resident_role import ResidentRole

if TYPE_CHECKING:
    from django.db.models import QuerySet

class ResidentRoleRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[ResidentRole]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[ResidentRole]: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[ResidentRole]: pass
    @abstractmethod
    def list_all(self) -> Sequence[ResidentRole]: pass
    @abstractmethod
    def add(self, resident_role: ResidentRole) -> ResidentRole: pass
    @abstractmethod
    def update(self, resident_role: ResidentRole) -> ResidentRole: pass
    @abstractmethod
    def delete(self, resident_role: ResidentRole) -> None: pass

class DjangoResidentRoleRepository(ResidentRoleRepository):
    def get_by_id(self, id: UUID) -> Optional[ResidentRole]:
        try: return ResidentRole.objects.get(id=id)
        except ResidentRole.DoesNotExist: return None
    def get_by_slug(self, slug: str) -> Optional[ResidentRole]:
        try: return ResidentRole.objects.get(slug=slug)
        except ResidentRole.DoesNotExist: return None
    def get_by_name(self, name: str) -> Optional[ResidentRole]:
        try: return ResidentRole.objects.get(name=name)
        except ResidentRole.DoesNotExist: return None
    def list_all(self) -> 'QuerySet[ResidentRole]': # Added quotes for forward ref if TYPE_CHECKING not enough
        return ResidentRole.objects.all()
    def add(self, resident_role: ResidentRole) -> ResidentRole:
        resident_role.save(); return resident_role
    def update(self, resident_role: ResidentRole) -> ResidentRole:
        resident_role.save(); return resident_role
    def delete(self, resident_role: ResidentRole) -> None:
        resident_role.delete()
