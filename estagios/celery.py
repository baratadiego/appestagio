import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estagios.settings')

app = Celery('estagios')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()