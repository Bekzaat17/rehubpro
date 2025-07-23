from celery import shared_task
from licenses.tasks.check_license_expiration import check_license_expiration as internal

@shared_task
def check_license_expiration():
    internal()