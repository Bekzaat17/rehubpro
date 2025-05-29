
from django.contrib import admin
from references.models.resident_role import ResidentRole

@admin.register(ResidentRole)
class ResidentRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'slug')