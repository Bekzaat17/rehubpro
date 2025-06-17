# residents/repositories/resident_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional, Sequence, TYPE_CHECKING

from django.db.models import QuerySet

from core.patterns.repository import AbstractRepository
from residents.models import Resident # Assuming Resident model is in residents.models

if TYPE_CHECKING:
    from django.db.models import QuerySet

class ResidentRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Resident]:
        pass

    @abstractmethod
    def list_all(self) -> Sequence[Resident]:
        pass

    @abstractmethod
    def list_active(self) -> Sequence[Resident]:
        pass

    @abstractmethod
    def search_by_full_name(self, query: str) -> Sequence[Resident]:
        pass

    @abstractmethod
    def add(self, resident: Resident) -> Resident:
        pass

    @abstractmethod
    def update(self, resident: Resident) -> Resident:
        pass

    @abstractmethod
    def delete(self, resident: Resident) -> None:
        pass


class DjangoResidentRepository(ResidentRepository):
    def get_by_id(self, id: int) -> Optional[Resident]:
        try:
            return Resident.objects.get(id=id)
        except Resident.DoesNotExist:
            return None

    def list_all(self) -> 'QuerySet[Resident]':
        return Resident.objects.all().order_by('full_name')

    def list_active(self) -> 'QuerySet[Resident]':
        return Resident.objects.filter(is_active=True).order_by('full_name')

    def search_by_full_name(self, query: str) -> 'QuerySet[Resident]':
        return Resident.objects.filter(full_name__icontains=query, is_active=True).order_by('full_name')

    def add(self, resident: Resident) -> Resident:
        resident.save()
        return resident

    def update(self, resident: Resident) -> Resident:
        resident.save()
        return resident

    def delete(self, resident: Resident) -> None:
        resident.delete()
