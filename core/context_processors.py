from datetime import datetime


def global_variables(request):
    return {
        'PROJECT_NAME': 'RehabPro',
        'now': datetime.now(),
    }