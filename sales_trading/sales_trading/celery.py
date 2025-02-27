import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales_trading.settings')

app = Celery('sales_trading')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()