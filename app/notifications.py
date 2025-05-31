# notifications.py
from modules.redis_client import subscribe_to_channel

def handle_inventory_update(message):
    print(f"Обновление запасов: Товар {message['product_id']}")
    print(f"Новый остаток: {message['new_stock']}")
    print(f"Обновил: {message['updated_by']}")

if __name__ == "__main__":
    subscribe_to_channel("inventory_updates", handle_inventory_update)