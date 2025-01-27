# Инициализация инвентаря
inventory = {
    101: {"name": "Smartphone", "category": "Electronics", "price": 29000, "quantity": 50},
    102: {"name": "Laptop", "category": "Electronics", "price": 54000, "quantity": 30},
    103: {"name": "Coffee Maker", "category": "Appliances", "price": 7000, "quantity": 20},
}

# Множество для хранения уникальных категорий
categories = set(item['category'] for item in inventory.values())

# Функция добавления нового товара
def add_product(inventory, product_id, name, category, price, quantity):
    if product_id in inventory:
        inventory[product_id]['quantity'] += quantity
    else:
        inventory[product_id] = {"name": name, "category": category, "price": price, "quantity": quantity}
    categories.add(category)

# Функция удаления товара
def remove_product(inventory, product_id):
    if product_id in inventory:
        category = inventory[product_id]['category']  # Сохраняем категорию перед удалением
        del inventory[product_id]
        # Проверяем, остались ли товары в этой категории
        if not any(item['category'] == category for item in inventory.values()):
            categories.discard(category)
    else:
        print(f"Товар с ID {product_id} не найден.")

# Функция обновления количества товара
def update_quantity(inventory, product_id, quantity):
    if product_id in inventory:
        if quantity <= 0:
            remove_product(inventory, product_id)  # Используем функцию удаления
        else:
            inventory[product_id]['quantity'] = quantity
    else:
        print(f"Товар с ID {product_id} не найден.")

# Функция получения списка уникальных категорий
def get_unique_categories():
    return categories

# Примеры использования функций

# Добавление нового товара
add_product(inventory, 104, "Blender", "Appliances", 5000, 15)
print("Инвентарь после добавления товара:")
print(inventory)

# Удаление товара
remove_product(inventory, 102)
print("Инвентарь после удаления товара:")
print(inventory)

# Обновление количества товара
update_quantity(inventory, 101, 60)
print("Инвентарь после обновления количества товара:")
print(inventory)

# Получение уникальных категорий
unique_categories = get_unique_categories()
print("Уникальные категории товаров:")
print(unique_categories)