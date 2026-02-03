import requests

def create_purchase_order(product_id, quantity):
    response = requests.post('https://supplier-api.com/orders', json={
        'product_id': product_id,
        'quantity': quantity
    })
    return response.json()