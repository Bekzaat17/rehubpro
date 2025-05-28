# rehabpro/references/admin/resident_function_admin.py

from django.contrib import admin
from references.models.resident_function import ResidentFunction

@admin.register(ResidentFunction)
class ResidentFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'slug')