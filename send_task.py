import sys
import os

# Add the project root to PYTHONPATH so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from inventory_forecasting.tasks import process_message

process_message.delay({"id": 1, "name": "Test"})
print("Task sent!")
