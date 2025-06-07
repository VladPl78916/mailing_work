from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, URL

class RegistrationForm(FlaskForm):
    city = StringField('Город', validators=[DataRequired()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество')
    email = StringField('Email', validators=[DataRequired(), Email()])
    telegram_id = StringField('ID Telegram', validators=[DataRequired()])
    vk_link = StringField('Ссылка ВК', validators=[DataRequired(), URL()])
    submit = SubmitField('Зарегистрироваться')