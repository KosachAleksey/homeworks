from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from validate_email import validate_email  # проверка email

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

# Подключение к базе данных SQLite
def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Функция инициализации таблицы
def init_db():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER CHECK(age >= 1 AND age <= 120),
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Создаем таблицу, если её ещё нет
init_db()

@app.route('/')
def index():
    # Отображаем страницу с формой регистрации
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Получаем данные из формы
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        age_str = request.form.get('age')
        
        # Проверяем заполнены ли поля
        if not all([name, email, age_str]):
            raise ValueError("Все поля обязательны!")
        
        # Преобразуем возраст в число
        try:
            age = int(age_str)
        except ValueError:
            raise ValueError("Возраст должен быть числом.")
        
        # Проверяем имя и электронную почту
        if len(name) > 100 or len(name) < 2:
            raise ValueError("Имя должно быть от 2 до 100 символов.")
        
        # Проверяем правильность email
        is_valid = validate_email(email)
        if not is_valid:
            raise ValueError("Некорректный адрес электронной почты.")
        
        # Проверяем диапазон возраста
        if age < 1 or age > 120:
            raise ValueError("Возраст должен быть от 1 до 120 лет.")

        # Сохраняем данные в базу
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users(name, email, age) VALUES (?, ?, ?)', 
                (name, email, age))
            conn.commit()

        # Перенаправляем на страницу успешного завершения регистрации
        return redirect(url_for('success'))
    except Exception as e:
        error_message = str(e)
        return render_template('form.html', error=error_message)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/users')
def show_users():
    # Подключаемся к базе данных и получаем всех пользователей
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY registration_date DESC')
        rows = cursor.fetchall()
    return render_template('users.html', users=rows)

if __name__ == '__main__':
    app.run(debug=True)