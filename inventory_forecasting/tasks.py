from celery import shared_task
from django.core.mail import send_mail
#from .ml_forecast import train_and_forecast
#from .models import Inventory

@shared_task
def daily_forecast():
    for product in Product.objects.all():
        train_and_forecast(product.id)

@shared_task
def check_reorder_alerts():
    low_stock = Inventory.objects.filter(current_stock__lte=models.F('reorder_point'))
    # Send alerts (see Step 9)

def my_task():
    print("Hello from Celery")

@shared_task
def process_message(data):
    # Do something with the data
    print(f"Processing: {data}")

@shared_task
def check_reorder_alerts():
    low_stock = Inventory.objects.filter(current_stock__lte=models.F('reorder_point'))
    for item in low_stock:
        send_mail('Low Stock Alert', f'Reorder {item.product.name}', 'from@example.com', ['manager@example.com'])
        # Integrate Twilio for SMS