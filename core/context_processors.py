from datetime import datetime

def global_variables(request):
    return {
        'PROJECT_NAME': 'RehubPro',
        'now': datetime.now(),
        'DATE_FORMAT': 'd.m.Y',  # Глобальный формат даты для шаблонов
    }