import peewee as pw
import database as db

database = db.handler

TYPES_OF_RELATIONSHIP = {
    "Friend": 0,
    "Pending": 1,
    "Denied": 2
}

class BaseModel(pw.Model):
    class Meta:
        database = database


class User(BaseModel):
    user_id = pw.BigIntegerField(column_name="user_id", primary_key=True)
    username = pw.CharField(column_name='name', max_length=24)
    description = pw.TextField(column_name="description")
    profile_photo_path = pw.CharField(column_name="profile_photo")

    class Meta:
        table_name = 'User'


class Relationship(BaseModel):
    user_id = pw.BigIntegerField(column_name="user_id")
    other_id = pw.BigIntegerField(column_name='other_id')
    relationship = pw.IntegerField(column_name="relationship")

    class Meta:
        table_name = 'Relationship'


class Topic(BaseModel):
    name = pw.CharField(column_name="topic_name", max_length=24)

    class Meta:
        table_name = 'Topic'


class TopicToUser(BaseModel):
    user_id = pw.BigIntegerField(column_name="user_id")
    topic_id = pw.IntegerField(column_name="topic_id")

    class Meta:
        table_name = 'TopicToUser'


database.create_tables([User, Relationship, Topic, TopicToUser])
