import datetime

from flask_bcrypt import generate_password_hash 
from flask_bcrypt import check_password_hash 
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(unique=True)
    date_joined = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-date_joined',)

    
    @classmethod
    def generate_user(cls, username, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(username=username, email=email,
                           password=generate_password_hash(password),
                           is_admin=admin)
        
        except IntegrityError:
            raise ValueError('Username already exists')


class Add(Model):
    entry_id = AutoField()
    title = CharField(unique=True)
    date = DatetimeField(default=datetime.datetime.now)
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()

    
    class Meta:
        database = DATABASE
        order_by = ('-date',)

    
    @classmethod
    def create_entry(cls, title, date, time_spent, learned, resources):
        try:
            with DATABASE.transaction():
                cls.create(
                    title=title,
                    date=date,
                    time_spent=time_spent,
                    learned=learned,
                    resources=resources
                )
        except IntegrityError:
            raise ValueError("Journal entry already exists.")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
    

if __name__ == '__main__':
    DATABASE.connect()
    DATABASE.create_tables([User, Add], safe=True)
    DATABASE.close()
    