from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    return "<a href='http://127.0.0.1:8080/base'>Шаблон для первого задания</a>"


@app.route('/base')
def index():
    user = "Ученик Яндекс.Лицея"
    return render_template('base.html', title='Домашняя страница',
                           username=user)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
