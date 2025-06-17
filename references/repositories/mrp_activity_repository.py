
from abc import abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID
from django.db.models import QuerySet # Ensure QuerySet is imported
from core.patterns.repository import AbstractRepository
from references.models.mrp_activity import MrpActivity

if TYPE_CHECKING:
    from django.db.models import QuerySet

class MrpActivityRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[MrpActivity]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[MrpActivity]: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[MrpActivity]: pass
    @abstractmethod
    def list_all(self) -> Sequence[MrpActivity]: pass
    @abstractmethod
    def add(self, mrp_activity: MrpActivity) -> MrpActivity: pass
    @abstractmethod
    def update(self, mrp_activity: MrpActivity) -> MrpActivity: pass
    @abstractmethod
    def delete(self, mrp_activity: MrpActivity) -> None: pass

class DjangoMrpActivityRepository(MrpActivityRepository):
    def get_by_id(self, id: UUID) -> Optional[MrpActivity]:
        try: return MrpActivity.objects.get(id=id)
        except MrpActivity.DoesNotExist: return None
    def get_by_slug(self, slug: str) -> Optional[MrpActivity]:
        try: return MrpActivity.objects.get(slug=slug)
        except MrpActivity.DoesNotExist: return None
    def get_by_name(self, name: str) -> Optional[MrpActivity]:
        try: return MrpActivity.objects.get(name=name)
        except MrpActivity.DoesNotExist: return None
    def list_all(self) -> 'QuerySet[MrpActivity]': # Added quotes for forward ref if TYPE_CHECKING not enough
        return MrpActivity.objects.all()
    def add(self, mrp_activity: MrpActivity) -> MrpActivity:
        mrp_activity.save(); return mrp_activity
    def update(self, mrp_activity: MrpActivity) -> MrpActivity:
        mrp_activity.save(); return mrp_activity
    def delete(self, mrp_activity: MrpActivity) -> None:
        mrp_activity.delete()
