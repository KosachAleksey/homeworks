import requests

def fetch_data(url):
  
    try:
        response = requests.get(url, timeout=5)  # Тайм-аут 5 секунд
        response.raise_for_status()  # Проверяем HTTP-ошибки
        data = response.json()  # Преобразуем ответ в JSON
        log(f"Успешно получены данные с {url}, количество записей: {len(data)}")  # Проверяем размер данных
        return data
    except requests.exceptions.RequestException as e:
        log(f"Ошибка при запросе {url}: {e}")
        return None

def log(message): #Функция для записи вывода в файл и одновременного вывода в консоль
    print(message)  
    with open("my_answer.txt", "a", encoding="utf-8") as file:
        file.write(message + "\n")  # Записываем в файл

# Очистка файла перед записью новых данных
with open("my_answer.txt", "w", encoding="utf-8") as file:
    file.write("Лог работы программы:\n\n")

# 1. Получение списка постов
posts_url = "https://jsonplaceholder.typicode.com/posts"
posts = fetch_data(posts_url)

if posts:
    log("\nЗаголовки всех постов:")
    for post in posts:
        log(f"- {post['title']}")
else:
    log("Ошибка: список постов пуст или не загружен.")

# 2. Получение списка задач
todos_url = "https://jsonplaceholder.typicode.com/todos"
todos = fetch_data(todos_url)

if todos:
    log("\nПервые 10 задач:")
    for task in todos[:10]:
        status = "Выполнено" if task["completed"] else "Не выполнено"
        log(f"ID: {task['id']} | {task['title']} | {status}")
else:
    log("Ошибка: список задач пуст или не загружен.")

# 3. Получение списка комментариев
comments_url = "https://jsonplaceholder.typicode.com/comments"
comments = fetch_data(comments_url)

if comments:
    log("\nПервые 10 комментариев:")
    for comment in comments[:10]:
        log(f"ID: {comment['id']} | Пост {comment['postId']} | {comment['name']}:\n{comment['body']}\n")
else:
    log("Ошибка: список комментариев пуст или не загружен.")

log("\nПривет Борис! Все данные записаны в my_answer.txt  Это супер!!!")