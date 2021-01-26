import datetime

from flask_wtf import Form
from wtforms import StringField, PasswordField, DateField, IntegerField, TextAreaField
from wtforms.validators import (DataRequired, Regexp,ValidationError, Email,
                               Length, EqualTo)

from models import User

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')
    
    

class RegistrationForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters,"
                         "numbers, and underscores_only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])


class AddForm(Form):
    title = StringField('Enter the Title', validators=[DataRequired()])
    date = DateField('Publish Year (format YYYY-MM-DD):', format='%Y-%m-%d', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent', validators=[DataRequired()])
    learned = TextAreaField('What did you learn?', validators=[DataRequired()])
    resources = TextAreaField('Resources to remember', validators=[DataRequired()])