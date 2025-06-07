from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        flash(f'Спасибо, {name}! Ваше сообщение отправлено. Мы ответим на {email}', 'success')
        return redirect(url_for('form'))
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)