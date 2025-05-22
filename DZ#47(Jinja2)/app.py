from flask import Flask, render_template

app = Flask(__name__)

# Данные для передачи в шаблоны
users = [
    {"name": "Алексей", "role": "admin", "email": "alex@example.com"},
    {"name": "Мария", "role": "user", "email": "maria@example.com"},
    {"name": "Иван", "role": "moderator", "email": "ivan@example.com"},
    {"name": "Елена", "role": "user", "email": "elena@example.com"}
]

products = [
    {"name": "Ноутбук", "price": 45000, "in_stock": True},
    {"name": "Смартфон", "price": 25000, "in_stock": False},
    {"name": "Наушники", "price": 5000, "in_stock": True},
    {"name": "Планшет", "price": 30000, "in_stock": True}
]

@app.route('/')
def index():
    return render_template('index.html', 
                         is_logged_in=True, 
                         user_role='admin',
                         username='Алексей')

@app.route('/users')
def show_users():
    return render_template('users.html', 
                         users=users, 
                         products=products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)
