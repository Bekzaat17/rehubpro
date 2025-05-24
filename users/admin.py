from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    # Отображаемые поля в списке
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    # Порядок и поля при просмотре пользователя
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Персональная информация", {"fields": ("role",)}),
        ("Права доступа", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    # Порядок и поля при создании пользователя
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)