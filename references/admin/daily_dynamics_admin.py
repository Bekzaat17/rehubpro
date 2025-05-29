from django.contrib import admin
from references.models.daily_dynamics import DailyDynamics
from .base_reference_admin import BaseReferenceAdmin

@admin.register(DailyDynamics)
class DailyDynamicsAdmin(BaseReferenceAdmin):
    pass