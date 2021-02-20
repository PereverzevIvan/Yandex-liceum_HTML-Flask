from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='http://127.0.0.1:8080/promotion_image'>Реклама с картинкой</a>"


@app.route('/promotion_image')
def prom_img():
    return render_template('prom_img.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

