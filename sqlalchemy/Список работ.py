from data import db_session
from flask import Flask, url_for, render_template
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/get_jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = [f'{i.name} {i.surname}' for i in db_sess.query(User).all()]
    return render_template('Список работ.html', jobs=jobs, users=users)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
