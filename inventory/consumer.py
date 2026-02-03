import paho.mqtt.client as mqtt
from .models import Inventory

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    Inventory.objects.filter(product_id=data['product_id']).update(current_stock=data['stock'])

client = mqtt.Client()
client.on_message = on_message
client.connect("mqtt_broker_ip", 1883)
client.subscribe("inventory/updates")
client.loop_forever()