
from abc import abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID
from django.db.models import QuerySet # Ensure QuerySet is imported
from core.patterns.repository import AbstractRepository
from references.models.motivation import Motivation

if TYPE_CHECKING:
    from django.db.models import QuerySet

class MotivationRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Motivation]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Motivation]: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Motivation]: pass
    @abstractmethod
    def list_all(self) -> Sequence[Motivation]: pass
    @abstractmethod
    def add(self, motivation: Motivation) -> Motivation: pass
    @abstractmethod
    def update(self, motivation: Motivation) -> Motivation: pass
    @abstractmethod
    def delete(self, motivation: Motivation) -> None: pass

class DjangoMotivationRepository(MotivationRepository):
    def get_by_id(self, id: UUID) -> Optional[Motivation]:
        try: return Motivation.objects.get(id=id)
        except Motivation.DoesNotExist: return None
    def get_by_slug(self, slug: str) -> Optional[Motivation]:
        try: return Motivation.objects.get(slug=slug)
        except Motivation.DoesNotExist: return None
    def get_by_name(self, name: str) -> Optional[Motivation]:
        try: return Motivation.objects.get(name=name)
        except Motivation.DoesNotExist: return None
    def list_all(self) -> 'QuerySet[Motivation]': # Added quotes for forward ref if TYPE_CHECKING not enough
        return Motivation.objects.all()
    def add(self, motivation: Motivation) -> Motivation:
        motivation.save(); return motivation
    def update(self, motivation: Motivation) -> Motivation:
        motivation.save(); return motivation
    def delete(self, motivation: Motivation) -> None:
        motivation.delete()
