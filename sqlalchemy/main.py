# <-- Данный файл является шаблоном -->
from data import db_session
from flask import Flask
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    # app.run()


if __name__ == '__main__':
    main()
