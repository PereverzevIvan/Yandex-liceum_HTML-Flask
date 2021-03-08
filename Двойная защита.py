from flask import Flask, url_for, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    astro_id = IntegerField('id астронавта', validators=[DataRequired()])
    astro_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    captain_id = IntegerField('id капитана', validators=[DataRequired()])
    captain_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('Двойная защита/base.html')


@app.route('/success')
def success():
    return '<h1>Успех</h1>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('Двойная защита/double_defends.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
