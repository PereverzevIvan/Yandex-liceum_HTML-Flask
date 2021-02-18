from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def general_page():
    return "Миссия Колонизация Марса. <br>" \
           "<a href='http://127.0.0.1:8080/promotion_image'> " \
           "Перейти на страницу рекламы с картинкой</a>"


@app.route('/promotion_image')
def promotion_image():
    with open('design.html', mode='r', encoding='utf-8') as html_stream:
        return html_stream.read()


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
