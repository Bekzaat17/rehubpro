from django.contrib import admin
from .models import Resident
from .enums import DependencyType

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    """
    Админка для модели Resident с фильтрацией и отображением зависимости.
    """
    list_display = ('full_name', 'date_of_birth', 'date_of_admission', 'dependency_type')
    list_filter = ('dependency_type',)
    search_fields = ('full_name',)