# фрагмент кода с ошибками
#from flask import Flask, render_template, request

#app = Flask(__name__)

#@app.route("/",methods=["POST"])
#def home():
    #return render_template("form.html")

#@app.route("/submit", methods=["GET"])
#def submit():
    #name = request.forms.get("name")
    #return f"Hello {name}!"

#if __main__ == "__main__":
    #app.run(debug=True)

#Исправленный код
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])  # Ошибка 1: Добавлен GET метод. Главная страница должна быть доступна по GET для отображения формы
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])  # Ошибка 2: Изменен на POST метод. Данные формы обычно отправляются методом POST
def submit():
    name = request.form.get("name")  # Ошибка 3: Исправлено forms → form. В Flask используется request.form, а не request.forms
    return f"Hello {name}!"

if __name__ == "__main__":  # Ошибка 4: Исправлено __main__ → __name__
    app.run(debug=True)
