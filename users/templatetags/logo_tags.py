import os
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def logo_url():
    """
    Возвращает путь к логотипу в static/logo/logo.png, если он существует.
    Иначе — пустая строка.
    """
    rel_path = 'logo/logo.png'
    static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
    if not static_dirs:
        return ""

    static_dir = static_dirs[0]  # предполагаем, что один путь
    full_path = os.path.join(static_dir, rel_path)
    if os.path.exists(full_path):
        return settings.STATIC_URL + rel_path
    return ""