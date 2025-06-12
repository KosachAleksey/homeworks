from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Регулярные выражения для валидации
USERNAME_REGEX = re.compile(r'^[a-zA-Zа-яА-Я][a-zA-Zа-яА-Я0-9_-]{2,19}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$')

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        errors = {}
        is_valid = True
        
        # Валидация юзернейма
        if not username:
            errors['username'] = 'Юзернейм обязателен'
            is_valid = False
        elif not USERNAME_REGEX.fullmatch(username):
            errors['username'] = 'Некорректный юзернейм. Должен содержать 3-20 символов (буквы, цифры, _, -), начинаться с буквы'
            is_valid = False
        
        # Валидация email
        if not email:
            errors['email'] = 'Email обязателен'
            is_valid = False
        elif not EMAIL_REGEX.fullmatch(email):
            errors['email'] = 'Некорректный email'
            is_valid = False
        
        # Валидация пароля
        if not password:
            errors['password'] = 'Пароль обязателен'
            is_valid = False
        elif not PASSWORD_REGEX.fullmatch(password):
            errors['password'] = 'Пароль должен содержать минимум 8 символов, заглавную букву, цифру и спецсимвол'
            is_valid = False
        
        # Проверка совпадения паролей
        if password != confirm_password:
            errors['confirm_password'] = 'Пароли не совпадают'
            is_valid = False
        
        if is_valid:
            # В реальном приложении здесь была бы сохранение данных в БД
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('register'))
        else:
            for field, message in errors.items():
                flash(message, field)
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)