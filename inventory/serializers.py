from rest_framework import serializers
from .models import Product, Inventory, SalesHistory, Forecast

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Similarly for Inventory, SalesHistory, Forecast