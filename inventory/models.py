from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)  # optional


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    current_stock = models.IntegerField()
    reorder_point = models.IntegerField()  # Threshold for alerts
    last_updated = models.DateTimeField(auto_now=True)

class SalesHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    # Add TimescaleDB hypertable here if using raw SQL

class Forecast(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    predicted_demand = models.FloatField()
    forecast_date = models.DateField()
    confidence = models.FloatField(default=0.95)  # <-- add default here

