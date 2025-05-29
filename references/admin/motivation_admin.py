from django.contrib import admin
from references.models.motivation import Motivation
from .base_reference_admin import BaseReferenceAdmin

@admin.register(Motivation)
class MotivationAdmin(BaseReferenceAdmin):
    pass