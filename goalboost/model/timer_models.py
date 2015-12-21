from datetime import datetime, date, timedelta
from json import dumps, loads

from dateutil import parser
from pytz import timezone

from goalboost.model import db
from goalboost.model.auth_models import User

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

    def __init__(self, dateEntered=None, lastRestart=None, **kwargs):
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
    pass

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

# LEGACY Code before refactoring -----------------------------------------------------------

# This is a "mixin" which has knowledge of Timer internals.
# From a design point of view maybe that's not ideal.
class TimerFormat(object):
    def __str__(self):
        fmtstr="{:<20}:  {}"
        start = self.fmt_date(self.utc_to_pacific_datetime(getattr(self, "startTime")))
        last_restart = self.fmt_date(self.utc_to_pacific_datetime(getattr(self, "lastRestart")))
        seconds = self.get_seconds()
        total_elapsed = self.total_elapsed()
        formatted = \
            fmtstr.format("startTime (PST)", start) + "\n" + \
            fmtstr.format("lastRestart (PST)", last_restart) + "\n" + \
            fmtstr.format("elapsed (total)", total_elapsed) + "\n" + \
            fmtstr.format("seconds", seconds)

        return formatted

    # assumes naive utc_datetime
    def utc_to_pacific_datetime(self, utc_datetime):
        tz_pacific = timezone("America/Los_Angeles")
        tz_utc = timezone("UTC")
        utc2 = utc_datetime.replace(tzinfo = tz_utc)
        return utc2.astimezone(tz_pacific)

    # I've hard coded the contributor for now since I'm collaborating with myself.  Todo, collaborate with someone else, then
    # fix this.  Really this shouldn't be part of basic formatting, but moved into a report class.
    def to_output_json(self):
        snapshot = self.snapshot_dict()
        start = self.utc_to_pacific_datetime(getattr(self, "startTime")).strftime("%m/%d/%Y")
        notes = getattr(self, "notes")
        seconds = self.total_elapsed()
        hours = round((seconds / 3600), 1)
        fmt_str = '{{"contributor": "", "date": "{}", "hours": {}, "description": "{}"}}'
        return fmt_str.format(start, hours, notes)

    def fmt_date(self, dt):
        return dt.strftime("%a, %b %d, %Y %H:%M")

    def fmt_seconds(self, seconds):
        hrs = int(seconds/3600)
        mins_secs = seconds % 3600
        mins = int(mins_secs / 60)
        secs = mins_secs % 60

        return "{:0>2}:{:0>2}:{:0>2}".format(hrs, mins, secs)

    def counter(self):
        return self.fmt_seconds(self.total_elapsed())

    def __repr__(self):
        #startTime = getattr(self, "startTime")
        #s = "startTime: " + self.fmt_date(startTime) + " UTC (pacific time:  " + self.fmt_date(self.utc_to_pacific_datetime(startTime)) + ")"
        return self.to_json()

    def public_json(self):
        vals = self.snapshot_dict()
        # Datetime to string
        vals["startTime"] = self.fmt_date(vals["startTime"])
        vals["lastRestart"] = self.fmt_date(vals["lastRestart"])
        #return dumps(vals, indent=4, separators=(',', ': '))
        return dumps(vals)

    def fmt_string_or_null(self, val):
        sval = ""
        if val:
            sval = "".join(['"', str(val), '"'])
        else:
            sval = None
        return sval

    @classmethod
    def load_from_dict(cls, input):
        # More pythonic way
        t = Timer(**input) # id = input["id"], notes = input["notes"])
        for item in t.entries:
            item.dateRecorded = parser.parse(item.dateRecorded)
        return t

    # BUG!!! None becomes "None", not null
    def to_api_dict(self):
        entries = [ dict(dateRecorded = str(item.dateRecorded), seconds = item.seconds) for item in self.entries]
        d = dict(id = str(self.id or None), \
                 notes = self.notes, \
                 entries = entries, \
                 startTime = self._convert_datetime(self.startTime), \
                 lastRestart = self._convert_datetime(self.lastRestart), \
                 userId = str(self.userId or None), \
                 running = self.running)
        return d

    def _convert_datetime(self, dt):
        if type(dt) is datetime:
            return dt.isoformat()
        return dt

class TimerForDate(db.EmbeddedDocument):
    dateRecorded = db.DateTimeField(default=datetime.fromordinal(date.today().toordinal()))
    seconds = db.IntField(min_value=0, default=0)

    def __repr__(self):
        return "dateRecorded={{{0}, seconds={1}}}".format(self.dateRecorded, self.seconds)

class Timer(TimerFormat, db.Document):
    startTime = db.DateTimeField()
    lastRestart = db.DateTimeField()
    notes = db.StringField()
    # seconds = db.IntField(min_value=0, default=0)
    userId = db.ObjectIdField(null=True)
    running = db.BooleanField(default=False)
    entries = db.EmbeddedDocumentListField(TimerForDate)

    #def __init__(self, userId=None, startTime=datetime.utcnow(), **kwargs):
    def __init__(self, userId=None, startTime=None, **kwargs):
        super().__init__(userId=userId, startTime=startTime, **kwargs)
        setattr(self, "lastRestart", startTime)
        #self.set_seconds_today(seconds)

    def get_todays_time_record(self):
        # Ensure we have a recrod for today
        if 0 == len([x.dateRecorded for x in self.entries if x.dateRecorded.toordinal() == date.today().toordinal()]):
            self.entries.append(TimerForDate())
        todays_record = self.entries.get(dateRecorded=datetime.fromordinal(date.today().toordinal()))
        return todays_record

    def set_seconds_today(self, seconds):
        todays_record = self.get_todays_time_record()

        # Need to rework if rework total elapsed I think?
        todays_record.seconds = seconds

    def start(self):
        if self.is_running():
            raise ValueError("Timer cannot be started.  Already running")
        setattr(self, "lastRestart", datetime.utcnow())
        setattr(self, "startTime", datetime.utcnow())
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
        return sum([x.seconds for x in self.entries])
        # return getattr(self, "seconds")

    def is_running(self):
        return getattr(self, "running")

    def _update_time_on_stop(self):
        self.set_seconds_today(self.get_seconds_today() + self.current_elapsed())

    def get_seconds_today(self):
        return self.get_todays_time_record().seconds

    def snapshot_dict(self):
        vals = dict()
        vals["startTime"] = self.startTime
        vals["lastRestart"] = self.lastRestart
        vals["notes"] = self.notes
        vals["seconds"] = self.get_seconds()
        vals["userId"] = self.userId
        vals["running"] = self.running
        vals["total_elapsed"] = self.total_elapsed()
        vals["current_elapsed"] = self.current_elapsed()
        return vals
