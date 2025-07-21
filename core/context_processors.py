from django.utils import timezone

def global_variables(request):
    return {
        'PROJECT_NAME': 'RehubPro',
        'now': timezone.now(),
        'DATE_FORMAT': 'd.m.Y',  # Глобальный формат даты для шаблонов
    }