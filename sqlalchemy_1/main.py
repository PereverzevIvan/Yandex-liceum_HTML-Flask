from flask import Flask, render_template, url_for
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.login_form import LoginForm
from data.register import RegisterForm
from data.jobs import Jobs
from data.add_job_form import AddJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login-form.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    return render_template('login-form.html', title='Авторизация', form=form)


@app.route('/get_jobs')
def get_jobs():
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = [f'{i.name} {i.surname}' for i in db_sess.query(User).all()]
    return render_template('Список работ.html', jobs=jobs, users=users)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.team_leader = form.team_leader.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('add_job_form.html', title='Добавление работы', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.email = form.email.data
        user.address = form.address.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template('register_form.html', title='Регистрация', form=form)


def main():
    db_session.global_init('db/mars_one.db')
    app.run()


if __name__ == '__main__':
    main()
