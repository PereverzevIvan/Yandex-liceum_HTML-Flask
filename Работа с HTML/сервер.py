from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def general_page():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    return "Человечество вырастает из детства. <br>" \
           "Человечеству мала одна планета.<br>" \
           "Мы сделаем обитаемыми безжизненные пока планеты.<br>" \
           "И начнем с Марса! Присоединяйся!"


@app.route('/image_mars')
def image_mars():
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <title>Привет, Марс!</title>
                      </head>
                      <body>
                        <h1>Жди нас, марс!</h1>
                        <img src="{url_for('static', filename='img/mars.jpg')}" 
               alt="здесь должна была быть картинка, но не нашлась">
               <h3>Вот она какая, краная планета!</h3>
                      </body>
                    </html>"""


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
