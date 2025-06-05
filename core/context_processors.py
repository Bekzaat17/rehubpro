from datetime import datetime


def global_variables(request):
    return {
        'PROJECT_NAME': 'RehubPro',
        'now': datetime.now(),
    }