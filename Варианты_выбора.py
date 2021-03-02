from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='http://127.0.0.1:8080/choice/Марс'>Предложение: Марс</a>"


@app.route('/choice/<planet_name>')
def choice_planet(planet_name="Пусто"):
    about_planet = 'Пусто'
    arguments = ['Пусто' for i in range(5)]
    image_name = ''
    if planet_name == 'Марс':
        about_planet = 'Эта планета близка к земле'
        arguments = ['На ней много необходимых ресурсов',
                     'На ней есть вода и атмосфера',
                     'На ней есть небольшое магнитное поле',
                     'Сутки на Марсе дляться немного дольше земных',
                     'Наконец, она просто красива']
        image_name = url_for("static", filename="img/mars.png")
    else:
        about_planet = 'Извините, принимаем только Марс ¯\_¯_¯_/¯'
    return render_template('Варианты_выбора.html', planet_name=planet_name,
                           about_planet=about_planet, arguments=arguments,
                           image_name=image_name)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
