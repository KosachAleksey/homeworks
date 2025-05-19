from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        language = request.form.get('language')
        return redirect(url_for('thank_you', language=language))
    return render_template('index.html')

@app.route('/thank-you/<language>')
def thank_you(language):
    # Добавим иконки для каждого языка
    icons = {
        'Python': 'bi bi-filetype-py',
        'JavaScript': 'bi bi-filetype-js',
        'Java': 'bi bi-filetype-java',
        'C++': 'bi bi-filetype-cpp'
    }
    return render_template('thank_you.html', language=language, icon=icons.get(language, 'bi bi-code'))

if __name__ == '__main__':
    app.run(debug=True)
    