from django.contrib import admin

class BaseReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)