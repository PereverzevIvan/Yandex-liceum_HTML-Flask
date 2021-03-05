from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return '<a href="http://127.0.0.1:8080/results/Megaman X/8/99.9"><h1>Megaman X</h1></a>'


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return render_template('Результат_отбора.html', nickname=nickname, rating=rating, level=level)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
