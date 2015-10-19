from alguito.datastore import db
from flask.ext.security import UserMixin, RoleMixin
from datetime import datetime

# User and Role use flask security mixins and are used by flask security
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.EmailField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    account = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    timer = db.ObjectIdField(null=True)

class Task(db.Document):
    name = db.StringField(max_length=80)
    description = db.StringField(max_length=255)

class Timer(db.Document):

    def __init__(self, userId=None, startTime=datetime.utcnow(), **kwargs):
        super().__init__(userId=userId, startTime=startTime, **kwargs)
        setattr(self, "lastRestart", startTime)


    startTime = db.DateTimeField()
    lastRestart = db.DateTimeField()
    notes = db.StringField()
    seconds = db.IntField(min_value=0)
    userId = db.ObjectIdField(null=True)
