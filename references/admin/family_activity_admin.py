from django.contrib import admin
from references.models.family_activity import FamilyActivity
from .base_reference_admin import BaseReferenceAdmin

@admin.register(FamilyActivity)
class FamilyActivityAdmin(BaseReferenceAdmin):
    pass