from celery import Celery
import os

# Set default Django settings module if using Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_forecasting.settings')

app = Celery('inventory_forecasting')

# Load settings from Django settings.py with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Only if you use Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_forecasting.settings')

