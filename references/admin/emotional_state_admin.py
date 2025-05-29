from django.contrib import admin
from references.models.emotional_state import EmotionalState
from .base_reference_admin import BaseReferenceAdmin

@admin.register(EmotionalState)
class EmotionalStateAdmin(BaseReferenceAdmin):
    pass