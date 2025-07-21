# rehubpro/config/celery.py

import os
from celery import Celery

tz = os.getenv("TZ", "Asia/Almaty")
os.environ.setdefault("TZ", tz)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('rehubpro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()