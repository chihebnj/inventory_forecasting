from celery import shared_task
from .ml_forecast import train_and_forecast
from .models import Inventory


@shared_task
def daily_forecast():
    for product in Product.objects.all():
        train_and_forecast(product.id)


@shared_task
def check_reorder_alerts():
    low_stock = Inventory.objects.filter(
        current_stock__lte=models.F('reorder_point'))
