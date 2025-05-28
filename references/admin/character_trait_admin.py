# /references/admin/character_trait_admin.py

from django.contrib import admin
from references.models.character_trait import CharacterTrait, TraitType

@admin.register(CharacterTrait)
class CharacterTraitAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'slug')