from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='http://127.0.0.1:8080/astronaut_selection'>Отбор астронавтов</a>"


@app.route('/astronaut_selection')
def prom_img():
    return render_template('astronaut.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
