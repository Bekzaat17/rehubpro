from django.contrib import admin
from references.models.physical_state import PhysicalState
from .base_reference_admin import BaseReferenceAdmin

@admin.register(PhysicalState)
class PhysicalStateAdmin(BaseReferenceAdmin):
    pass