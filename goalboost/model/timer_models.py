from datetime import datetime, date, timedelta
from dateutil import parser

from goalboost.model import db
from goalboost.model.auth_models import User, UserModelFormatter
from goalboost.model.model_formatter import ModelFormatter


class Error(Exception):
    pass

class InvalidDataError(Error):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "InvalidDataError(msg={})".format(self.message)
'''
TimerEntity
This class should include only what needs to go to / from MongoDB, maybe some
simple validation on fields, and that's it.
Clients:  API, TimerDAO TimerFormatter.  Note ALL saves must go through TimerDAO,
          not directly through here.
'''
class TimerEntity(db.Document):
    dateEntered = db.DateTimeField()        # Actual date, no time
    lastRestart = db.DateTimeField()
    seconds = db.IntField(min_value=0, default=0)
    notes = db.StringField(required=False)
    user = db.ReferenceField(User, required=True)
    running = db.BooleanField(required= True, default=False)
    tags = db.ListField(db.StringField(), default=list)

    def __init__(self, dateEntered=None, lastRestart=None, *args, **kwargs):
        # TODO enhance type checking.  If datetime given for dateEntered, currently not converted to date
        # only.  Also, what if a string is passed in -- probably should parse.
        if dateEntered is None:
            today_as_int = datetime.utcnow().toordinal()
            dateEntered = datetime.fromordinal(today_as_int)
        if lastRestart is None:
            lastRestart = datetime.utcnow()
            lastRestart = lastRestart - timedelta(microseconds=lastRestart.microsecond)

        dateEntered = self.cast_date_time(dateEntered)
        lastRestart = self.cast_date_time(lastRestart)
        super().__init__(dateEntered, lastRestart, **kwargs)

    # Type checker for __init__.  Ensure we can handle date, datetime, and str as input to date fields
    def cast_date_time(self, val):
        if type(val) is type(""):
            return parser.parse(val)
        elif type(val) is type(datetime.utcnow()):
            return val
        elif type(val) is type(date.today()):
            return datetime.fromordinal(val.toordinal())
        raise TypeError("Invalid value for datetime:  " + str(type(val)) + ". Valid values are datetime, date, and string.")

    def __repr__(self):
        notes = None
        if self.notes is not None:
            notes = '"{}"'.format(self.notes)
        s = 'TimerEntity(id={}, dateEntered="{}", lastRestart="{}", notes={}, seconds={}, running={}, tags={})'.format(\
            self.id.__repr__(), self.dateEntered.__str__(), self.lastRestart.__str__(), notes, self.seconds, self.running,
            self.tags.__repr__())
        return s


'''
TimerDAO - DAO is "Data Access Object"
This class will be responsible for making sure a TimerEntity is saved correctly
with respect to the the rest of the database, for example (and maybe this is all it does),
ensuring that there's only one active timer for users.  Other responsiblities might include
auto-shutoff.  Note there is already such a beast
'''
class TimerDAO():
    def put(self, timer_entity):
        # TODO add turning off all timers for user
        if timer_entity.user is None:
            raise InvalidDataError("TimerDAO.put - TimerEntity.user cannot be None")
        if(True or timer_entity.running):
            # db.timer.update({userId: ObjectId("567421658c57cf2ef0028f03")}, {$set: {running: false}}, {multi: true})
            # Post.objects(comments__by="joe").update(**{'inc__comments__$__votes': 1})
            TimerEntity.objects(user = timer_entity.user).update(running=False)
        timer_entity.save()
        return timer_entity

'''
TimerFormatter
Should include formatting methods which consume or produce a timer entity, so this is
not part of timer any more.
'''
class TimerFormatter():
    #
    def model_to_dict(self, object_as_model):
        pass

    #
    def dict_to_model(self, object_as_dict):
        pass

'''
This represents what in the 1.0 timer world John used at the shell.
Implementing this is probably not a good idea.  The things that HAVE to work are the entity,
the DAO layer, and the API.  The rest is window dressing.
'''
class LocalTicker():
    pass

'''
RemoteTicker
This is a utility shell class that uses the API to allow us to save our time from the shell.
It will read a config file locally for email (NOT mongo userID) and password, etc.  Writing / testing this
will also be a good second set of integration tests around the API / authentication workflow.
TimeDog is a better name.
'''
class RemoteTicker(object):
    def start(self):
        pass

    def stop(self):
        pass

    def counter(self):
        pass

class TimerFormatter(ModelFormatter):
    pass