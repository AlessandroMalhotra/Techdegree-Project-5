import datetime
import sys

from peewee import *

DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
    entry_id = AutoField()
    title = CharField()
    date = DateField(default=datetime.datetime.now)
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
                    resources=resources,
                )
        except IntegrityError:
            raise ValueError("Journal entry already exists.")



if __name__ == '__main__':
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
    