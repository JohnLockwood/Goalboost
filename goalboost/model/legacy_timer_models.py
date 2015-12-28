from datetime import datetime, date
from json import dumps

from dateutil import parser
from pytz import timezone

from goalboost.model import db


#-------------------------------------------------------------------------------------------
# LEGACY Code before refactoring -----------------------------------------------------------
#-------------------------------------------------------------------------------------------

# This is a "mixin" which has knowledge of LegacyTimer internals.
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
        fmt_str = '{{"date": "{}", "hours": {}, "description": "{}"}}'
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
        t = LegacyTimer(**input) # id = input["id"], notes = input["notes"])
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


class LegacyTimer(TimerFormat, db.Document):
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
            raise ValueError("LegacyTimer cannot be started.  Already running")
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


class TimerDaoLegacy:
    # JCL review exceptions
    def timer_by_id(self, id):
        return LegacyTimer.objects(id = id).first()

    # JCL review exceptions and return values
    def timers_for_user(self, user_id):
        return [t for t in LegacyTimer.objects(userId = user_id).order_by("-lastRestart").all()]

    # JCL todo handle exception
    def save_timer(self, timer):
        timer.save()

    # Returns true if the timer is found and deleted.  False for not found.
    # Return value currently ignored by API
    def delete_timer(self, timer_id):
        timer = LegacyTimer.objects(id = timer_id).first()
        if (timer):
            # Todo can this still throw exception
            timer.delete()
            return True
        else:
            return False