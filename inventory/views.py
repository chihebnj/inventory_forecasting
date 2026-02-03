from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Add similar viewsets for Inventory, SalesHistory, Forecast
# Include custom actions for forecasts, e.g., def get_forecast(self, request, pk=None): ...