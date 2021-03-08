from flask import Flask, url_for, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SDJFSDKJFSKJ'


@app.route('/')
def index():
    params = {}
    params['title'] = 'Главная страница'
    return render_template('Автоматический ответ/base.html', params=params)


@app.route('/answer')
def answer():
    params = {}
    params['title'] = 'Ответ'
    return render_template('Автоматический ответ/base.html', params=params)


@app.route('/auto_answer')
def auto_answer():
    params = {}
    params['title'] = 'Авто-ответ'
    params['Фамилия'] = 'Васильев'
    params['Имя'] = 'Прокофий'
    params['Образование'] = 'Высшее'
    params['Профессия'] = 'Водитель маршрутки'
    params['Пол'] = 'Мужской'
    params['Мотивация'] = 'У меня высшее образование... Не хочу быть водителем обычной маршрутки'
    params['Готовность остаться на Марсе'] = True
    return render_template('Автоматический ответ/auto_answer.html', params=params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
