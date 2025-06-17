# residents/repositories/__init__.py
from .resident_repository import ResidentRepository, DjangoResidentRepository

__all__ = [
    "ResidentRepository", "DjangoResidentRepository"
]
