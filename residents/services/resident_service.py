# residents/services/resident_service.py
from abc import ABC, abstractmethod
from typing import List, Optional, Sequence # Changed List to Sequence for return types
from residents.models import Resident
from residents.repositories.resident_repository import ResidentRepository
# from residents.forms import ResidentForm # For validation in create/update later

class ResidentService(ABC):
    @abstractmethod
    def get_resident_by_id(self, id: int) -> Optional[Resident]:
        pass

    @abstractmethod
    def get_all_residents(self) -> Sequence[Resident]: # Changed
        pass

    @abstractmethod
    def get_active_residents(self) -> Sequence[Resident]: # Changed
        pass

    @abstractmethod
    def search_active_residents(self, query: str) -> Sequence[Resident]: # Changed
        pass

    # We might add create, update, delete methods here later,
    # which would handle form validation and then call the repository.
    # For now, focusing on read operations as per ResidentsDataView.


class DefaultResidentService(ResidentService):
    def __init__(self, resident_repository: ResidentRepository):
        self.resident_repository = resident_repository

    def get_resident_by_id(self, id: int) -> Optional[Resident]:
        return self.resident_repository.get_by_id(id)

    def get_all_residents(self) -> Sequence[Resident]: # Changed
        return self.resident_repository.list_all()

    def get_active_residents(self) -> Sequence[Resident]: # Changed
        return self.resident_repository.list_active()

    def search_active_residents(self, query: str) -> Sequence[Resident]: # Changed
        return self.resident_repository.search_by_full_name(query)
