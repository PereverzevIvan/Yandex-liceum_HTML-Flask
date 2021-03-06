from flask import Flask, url_for, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SDJFSDKJFSKJ'


@app.route('/')
def index():
    return '<a href="http://127.0.0.1:8080/training/инженер">Инженер</a><br>' \
           '<a href="http://127.0.0.1:8080/training/врач">Врач</a>'


@app.route('/training/<prof>')
def prof(prof):
    return render_template('Тренировки в полёте/index.html', prof=prof)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
