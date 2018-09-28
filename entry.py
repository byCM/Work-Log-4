from peewee import *

import datetime

db = SqliteDatabase('entries.db')

class Entry(Model):
    employee_name = CharField(max_length=30)
    date = DateTimeField(default=datetime.datetime.now)
    task_name = CharField(max_length=50)
    minutes = IntegerField(default=0)
    notes = CharField(max_length=100)
    
    
    
    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    
        

