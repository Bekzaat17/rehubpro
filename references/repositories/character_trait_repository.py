
from abc import abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from uuid import UUID

from django.db.models import QuerySet

from core.patterns.repository import AbstractRepository
from references.models.character_trait import CharacterTrait, TraitType

if TYPE_CHECKING:
    from django.db.models import QuerySet

class CharacterTraitRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[CharacterTrait]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[CharacterTrait]: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[CharacterTrait]: pass
    @abstractmethod
    def list_all(self) -> Sequence[CharacterTrait]: pass
    @abstractmethod
    def list_by_type(self, trait_type: TraitType) -> Sequence[CharacterTrait]: pass
    @abstractmethod
    def add(self, character_trait: CharacterTrait) -> CharacterTrait: pass
    @abstractmethod
    def update(self, character_trait: CharacterTrait) -> CharacterTrait: pass
    @abstractmethod
    def delete(self, character_trait: CharacterTrait) -> None: pass

class DjangoCharacterTraitRepository(CharacterTraitRepository):
    def get_by_id(self, id: UUID) -> Optional[CharacterTrait]:
        try: return CharacterTrait.objects.get(id=id)
        except CharacterTrait.DoesNotExist: return None
    def get_by_slug(self, slug: str) -> Optional[CharacterTrait]:
        try: return CharacterTrait.objects.get(slug=slug)
        except CharacterTrait.DoesNotExist: return None
    def get_by_name(self, name: str) -> Optional[CharacterTrait]:
        try: return CharacterTrait.objects.get(name=name)
        except CharacterTrait.DoesNotExist: return None
    def list_all(self) -> 'QuerySet[CharacterTrait]':
        return CharacterTrait.objects.all()
    def list_by_type(self, trait_type: TraitType) -> 'QuerySet[CharacterTrait]':
        return CharacterTrait.objects.filter(type=trait_type)
    def add(self, character_trait: CharacterTrait) -> CharacterTrait:
        character_trait.save(); return character_trait
    def update(self, character_trait: CharacterTrait) -> CharacterTrait:
        character_trait.save(); return character_trait
    def delete(self, character_trait: CharacterTrait) -> None:
        character_trait.delete()
