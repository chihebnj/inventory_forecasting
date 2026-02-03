import csv
from collections import defaultdict
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from inventory.models import Product, SalesHistory, Inventory


def extract_from_csv(file_path):
    sales = []

    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            sales.append({
                "sku": row["sku"],
                "quantity_sold": int(row["quantity_sold"]),
                "timestamp": datetime.fromisoformat(row["timestamp"]),
            })

    return sales


def transform_sales(raw_sales):
    aggregated = defaultdict(int)

    for sale in raw_sales:
        day = sale["timestamp"].date()
        key = (sale["sku"], day)
        aggregated[key] += sale["quantity_sold"]

    return aggregated

    return grouped


@transaction.atomic
def load_sales(raw_sales, aggregated_sales):

    # 1. Insert raw sales history
    for sale in raw_sales:
        product = Product.objects.get(sku=sale["sku"])

        SalesHistory.objects.create(
            product=product,
            quantity_sold=sale["quantity_sold"],
            timestamp=sale["timestamp"],
        )

    # 2. Update inventory stock
    for (sku, day), total_qty in aggregated_sales.items():
        product = Product.objects.get(sku=sku)
        inventory = Inventory.objects.get(product=product)

        inventory.current_stock -= total_qty
        inventory.last_updated = timezone.now()
        inventory.save()


def run_etl(csv_path):
    raw_sales = extract_from_csv(csv_path)
    aggregated = transform_sales(raw_sales)
    load_sales(raw_sales, aggregated)
