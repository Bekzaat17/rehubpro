
from abc import abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID
from django.db.models import QuerySet # Ensure QuerySet is imported
from core.patterns.repository import AbstractRepository
from references.models.family_activity import FamilyActivity

if TYPE_CHECKING:
    from django.db.models import QuerySet

class FamilyActivityRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[FamilyActivity]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[FamilyActivity]: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[FamilyActivity]: pass
    @abstractmethod
    def list_all(self) -> Sequence[FamilyActivity]: pass
    @abstractmethod
    def add(self, family_activity: FamilyActivity) -> FamilyActivity: pass
    @abstractmethod
    def update(self, family_activity: FamilyActivity) -> FamilyActivity: pass
    @abstractmethod
    def delete(self, family_activity: FamilyActivity) -> None: pass

class DjangoFamilyActivityRepository(FamilyActivityRepository):
    def get_by_id(self, id: UUID) -> Optional[FamilyActivity]:
        try: return FamilyActivity.objects.get(id=id)
        except FamilyActivity.DoesNotExist: return None
    def get_by_slug(self, slug: str) -> Optional[FamilyActivity]:
        try: return FamilyActivity.objects.get(slug=slug)
        except FamilyActivity.DoesNotExist: return None
    def get_by_name(self, name: str) -> Optional[FamilyActivity]:
        try: return FamilyActivity.objects.get(name=name)
        except FamilyActivity.DoesNotExist: return None
    def list_all(self) -> 'QuerySet[FamilyActivity]': # Added quotes for forward ref if TYPE_CHECKING not enough
        return FamilyActivity.objects.all()
    def add(self, family_activity: FamilyActivity) -> FamilyActivity:
        family_activity.save(); return family_activity
    def update(self, family_activity: FamilyActivity) -> FamilyActivity:
        family_activity.save(); return family_activity
    def delete(self, family_activity: FamilyActivity) -> None:
        family_activity.delete()
