import datetime

from peewee import *

DATABASE = SqliteDatabase('app.db')


class BaseModel(Model):
	class Meta:
		database = DATABASE


class Course(BaseModel):
	title = CharField()
	url = CharField(unique=True)
	created_at = DateTimeField(default=datetime.datetime.now)


class Review(BaseModel):
	course = ForeignKeyField(Course, related_name='review_set')
	rating = IntegerField()
	comment = TextField(default='')
	created_at = DateTimeField(default=datetime.datetime.now)

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Course, Review], safe=True)
	DATABASE.close()