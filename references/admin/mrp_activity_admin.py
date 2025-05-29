from django.contrib import admin
from references.models.mrp_activity import MrpActivity
from .base_reference_admin import BaseReferenceAdmin

@admin.register(MrpActivity)
class MrpActivityAdmin(BaseReferenceAdmin):
    pass