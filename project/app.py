from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Пользователи
users = {
    'admin': {'password': '1234', 'role': 'Администратор'},
    'user': {'password': 'abcd', 'role': 'Пользователь'}
}

@app.route("/", methods=["GET", "POST"])
def index():
    result1 = ""
    result2 = ""
    result3 = ""
    result4 = ""

    # Задание 1: Авторизация
    if request.method == "POST" and "login" in request.form and "password" in request.form and "firstname" not in request.form:
        login = request.form["login"]
        password = request.form["password"]
        user = users.get(login)
        if user and user["password"] == password:
            result1 = f"Добро пожаловать, {login}! Уровень доступа: {user['role']}"
        else:
            result1 = "❌ Неверный логин или пароль."

    # Задание 2: Работа с числами
    if request.method == "POST" and "num1" in request.form:
        try:
            a = float(request.form["num1"])
            b = float(request.form["num2"])
            c = float(request.form["num3"])
            action = request.form["operation"]
            if action == "min":
                result2 = f"Минимум: {min(a, b, c)}"
            elif action == "max":
                result2 = f"Максимум: {max(a, b, c)}"
            elif action == "avg":
                result2 = f"Среднее: {(a + b + c) / 3:.2f}"
        except:
            result2 = "❌ Ошибка ввода чисел."

    # Задание 3: Анкета + логин/пароль
    if request.method == "POST" and "firstname" in request.form:
        data = {
            "Имя": request.form["firstname"],
            "Фамилия": request.form["lastname"],
            "Возраст": request.form["age"],
            "Email": request.form["email"],
            "Пол": request.form["gender"],
            "Адрес": request.form["address"],
            "Логин": request.form["login_reg"],
            "Пароль": request.form["password_reg"],
            "Подписка": "Да" if "subscribe" in request.form else "Нет"
        }
        result3 = "<br>".join([f"<b>{k}</b>: {v}" for k, v in data.items()])

    # Задание 4: 256-й день года
    if request.method == "POST" and "year" in request.form:
        try:
            year = int(request.form["year"])
            day = datetime(year, 1, 1) + timedelta(days=255)
            result4 = f"{day.strftime('%d %B (%A)')}"
        except:
            result4 = "❌ Введите корректный год."

    return render_template("index.html", result1=result1, result2=result2, result3=result3, result4=result4)

if __name__ == "__main__":
    app.run(debug=True)
