from flask import Flask, url_for, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SDJFSDKJFSKJ'


@app.route('/')
def index():
    return '<a href="http://127.0.0.1:8080/list_prof/ol">Нумерованный</a><br>' \
           '<a href="http://127.0.0.1:8080/list_prof/ul">Маркированный</a><br>' \
           '<a href="http://127.0.0.1:8080/list_prof/asdasd">Ошибка</a>'


@app.route('/list_prof/<list_t>')
def prof(list_t):
    profs = ['Врач', 'Технолог', 'Эколог', 'Каскадёр', 'Программист', 'Писатель', 'Инженер']
    return render_template('Список профессий/index.html', profs=profs, list_t=list_t)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
