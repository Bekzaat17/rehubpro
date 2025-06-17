
from abc import abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID

from django.db.models import QuerySet

from core.patterns.repository import AbstractRepository
from references.models.emotional_state import EmotionalState

if TYPE_CHECKING:
    from django.db.models import QuerySet

class EmotionalStateRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[EmotionalState]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[EmotionalState]: pass
    @abstractmethod
    def list_all(self) -> Sequence[EmotionalState]: pass
    @abstractmethod
    def add(self, emotional_state: EmotionalState) -> EmotionalState: pass
    @abstractmethod
    def update(self, emotional_state: EmotionalState) -> EmotionalState: pass
    @abstractmethod
    def delete(self, emotional_state: EmotionalState) -> None: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[EmotionalState]: pass

class DjangoEmotionalStateRepository(EmotionalStateRepository):
    def get_by_id(self, id: UUID) -> Optional[EmotionalState]:
        try: return EmotionalState.objects.get(id=id)
        except EmotionalState.DoesNotExist: return None
    def get_by_slug(self, slug: str) -> Optional[EmotionalState]:
        try: return EmotionalState.objects.get(slug=slug)
        except EmotionalState.DoesNotExist: return None
    def get_by_name(self, name: str) -> Optional[EmotionalState]:
        try: return EmotionalState.objects.get(name=name)
        except EmotionalState.DoesNotExist: return None
    def list_all(self) -> 'QuerySet[EmotionalState]':
        return EmotionalState.objects.all()
    def add(self, emotional_state: EmotionalState) -> EmotionalState:
        emotional_state.save(); return emotional_state
    def update(self, emotional_state: EmotionalState) -> EmotionalState:
        emotional_state.save(); return emotional_state
    def delete(self, emotional_state: EmotionalState) -> None:
        emotional_state.delete()
