from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_form():
    return render_template('form.html')

@app.route('/submit', methods=['GET'])
def submit_form():
    data = {
        'first_name': request.args.get('first_name'),
        'last_name': request.args.get('last_name'),
        'email': request.args.get('email'),
        'age': request.args.get('age'),
        'gender': request.args.get('gender'),
        'hobbies': request.args.getlist('hobbies'),
        'city': request.args.get('city')
    }
    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
    