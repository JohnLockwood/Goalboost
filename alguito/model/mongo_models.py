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
    seconds = db.IntField(min_value=0, default=0)
    userId = db.ObjectIdField(null=True)
    running = db.BooleanField(default=False)

    def start(self):
        if self.is_running():
            raise ValueError("Timer cannot be started.  Already running")
        setattr(self, "lastRestart", datetime.utcnow())
        setattr(self, "running", True)
        self.save()

    def stop(self):
        self._update_time_on_stop()
        setattr(self, "running", False)
        self.save()

    def current_elapsed(self):
        # current_elapsed is only diff between lastRestart and now if we're running.
        # If we're stopped then the total should haved been added to the seconds field
        # and current_elapsed is 0
        if not self.is_running():
            return 0
        now = datetime.utcnow()
        then = getattr(self, "lastRestart")
        return int((now - then).total_seconds())

    def total_elapsed(self):
        return self.current_elapsed() + self.get_seconds()

    def get_seconds(self):
        return getattr(self, "seconds")

    def is_running(self):
        return getattr(self, "running")

    def _update_time_on_stop(self):
        setattr(self, "seconds", self.total_elapsed())