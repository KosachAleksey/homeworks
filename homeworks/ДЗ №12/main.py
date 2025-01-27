from datetime import datetime, timedelta

purchases = [
    [1, "Phont", 150000, "electronics", "2024-12-01"],
    [2, "Shoes", 18000, "fashion", "2024-12-03"],
    [3, "T-shirt", 5000, "fashion", "2024-12-03"],
    [1, "TV", 120000, "electronics", "2024-12-05"],
    [2, "Trousers", 16000, "fashion", "2024-12-08"],
    [4, "Refrigerator", 120000, "electronics", "2024-12-05"],
]

# Фильтрация покупок по категории
def filter_by_category(purchases, category):
    return [purchase for purchase in purchases if purchase[3] == category]


# Фильтрация покупок за последние N дней
def filter_recent_purchases(purchases, days):

    threshold_date = datetime.now() - timedelta(days=days)
    return [purchase for purchase in purchases if datetime.strptime(purchase[4], "%Y-%m-%d") >= threshold_date]

# Подсчет общей суммы покупок каждого клиента
def total_spent_by_client(purchases, callback):
    total_spent = {}
    for purchase in purchases:
        client_id = purchase[0]
        amount = purchase[2]
        if client_id not in total_spent:
            total_spent[client_id] = 0
        total_spent[client_id] += amount
    return callback(total_spent)

# Пример коллбэк функции для total_spent_by_client
def callback_function(total_spent):
    return total_spent

# Сортировка покупок по сумме и категориям
def sort_purchases(purchases):
    return sorted(purchases, key=lambda x: (-x[2], x[3]))

# Генерация отчета о покупках для конкретного клиента
def generate_report(purchases, client_id):
    client_purchases = [purchase for purchase in purchases if purchase[0] == client_id]
    total_amount = sum(purchase[2] for purchase in client_purchases)
    return {
        'client_id': client_id,
        'purchases': [{'item': purchase[1], 'amount': purchase[2]} for purchase in client_purchases],
        'total_amount': total_amount
    }

# Примеры использования функций
if __name__ == "__main__":
    # Пример фильтрации по категории
    electronics_purchases = filter_by_category(purchases, 'electronics')
    print("Электроника:", electronics_purchases)

    

    # Пример фильтрации за последние N дней
    recent_purchases = filter_recent_purchases(purchases, 25)
    print("Недавние покупки за последние 25 дней: ", recent_purchases)

    # Пример подсчета общей суммы покупок каждого клиента
    total_spent = total_spent_by_client(purchases, callback_function)
    print("Общая сумма покупок по клиентам:", total_spent)

    # Пример сортировки покупок
    sorted_purchases = sort_purchases(purchases)
    print("Отсортированные покупки:", sorted_purchases)

    # Пример генерации отчета о покупках для клиента с ID 1
    report_for_client_1 = generate_report(purchases, 1)
    print("Отчет для клиента 1:", report_for_client_1)