import os
from celery import Celery


if os.environ.get("CELERY_BACKEND"):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mlconductor.settings')
    app = Celery('mlconductor')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()