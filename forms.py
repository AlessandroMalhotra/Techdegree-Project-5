import datetime

from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, TextAreaField

from wtforms.validators import (DataRequired)

from models import Entry

class EntryForm(Form):
    title = StringField('Enter the Title', validators=[DataRequired()])
    date = DateField('Publish Year (format YYYY-MM-DD):', format='%Y-%m-%d', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent')
    learned = TextAreaField('What did you learn?', validators=[DataRequired()])
    resources = TextAreaField('Resources to remember')