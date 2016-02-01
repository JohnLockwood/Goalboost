from datetime import datetime, date, timedelta

from bson import ObjectId
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
Timer
This class should include only what needs to go to / from MongoDB, maybe some
simple validation on fields, and that's it.
Clients:  API, TimerDAO TimerFormatter.  Note ALL saves must go through TimerDAO,
          not directly through here.
'''
class Timer(db.Document):
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
        s = 'Timer(id={}, dateEntered="{}", lastRestart="{}", notes={}, seconds={}, running={}, tags={})'.format(\
            self.id.__repr__(), self.dateEntered.__str__(), self.lastRestart.__str__(), notes, self.seconds, self.running,
            self.tags.__repr__())
        return s

    # ARRRGGGGHHHH!!!
    # For updates, we need a way to mark attributes dirty, otherwise we can't implement "put" since just loading the object
    # from JSON doesn't mark the attribute as SET.  It may be that we want to handle this in the formatter, but having
    # just spent SEVERAL hours getting the formatter to be generic, I don't want to break it just yet.
    def update_attributes(self, timer_new):
        attributes = ["dateEntered", "lastRestart", "seconds", "notes", "user", "running", "tags"]
        for key in attributes:
            setattr(self, key, getattr(timer_new, key))




'''
TimerDAO - DAO is "Data Access Object"
This class will be responsible for making sure a Timer is saved correctly
with respect to the the rest of the database, for example (and maybe this is all it does),
ensuring that there's only one active timer for users.  Other responsiblities might include
auto-shutoff.  Note there is already such a beast
'''
class TimerDAO():
    def put(self, timer_entity):
        # TODO add turning off all timers for user
        if timer_entity.user is None:
            raise InvalidDataError("TimerDAO.put - Timer.user cannot be None")
        if(True or timer_entity.running):
            # db.timer.update({userId: ObjectId("567421658c57cf2ef0028f03")}, {$set: {running: false}}, {multi: true})
            # Post.objects(comments__by="joe").update(**{'inc__comments__$__votes': 1})
            Timer.objects(user = timer_entity.user).update(running=False)
            timer_entity.save()

    def get(self, timer_id):
        return Timer.objects(id=timer_id).first()

    def get_all_timers_for_user(self, user_id):
        return [t for t in Timer.objects(user = ObjectId(user_id)).order_by("-lastRestart").all()]

    def delete(self, timer_id):
        return Timer.objects(id=timer_id).delete()

    # TODO Given a list of users, get the timers for the users
    def get_timers_for_users(self, users, tag_list=None):
        if tag_list is not None:
            return [timer for timer in Timer.objects(user__in=users, tags__in=tag_list)]
        else:
            return [timer for timer in Timer.objects(user__in=users)]

    def get_weekly_timer_statistics(self, users_list, tags_list):
        collection = Timer()._get_collection()
        cursor = collection.aggregate(
            [
                {"$match":  {"tags" : {"$in" : tags_list}, "user" : {"$in" : users_list} }},
                {"$group":
                    {
                        "_id": { "week": { "$week": "$dateEntered"}, "year": { "$year": "$dateEntered" } },
                        "total_seconds": { "$sum":   "$seconds"    },
                        "count": { "$sum": 1 }
                    }
                }
            ])

        # "seconds": { "$sum":  {"$divide": [ "$seconds" , 1 ] } },
        unsorted = []
        years = set()
        ids = set()

        formatter = TimerFormatter()
        for document in cursor:

            document["weekEnding"] = formatter.get_week_ending_date(document["_id"]["year"], document["_id"]["week"])
            hours, minutes = formatter.seconds_to_hours_and_minutes(document["total_seconds"])
            document["hours_minutes"] = "{0}:{1}".format(hours, minutes)
            unsorted.append(document)
            # Add years to a set, and add all "_ids" (years + weeks)
            years.add(document["_id"]["year"])
            id = (document["_id"]["year"], document["_id"]["week"])
            ids.add(id)
        '''
        # Make sure we are densely populated, add a zero hours entry if none exists
        # But this causes problems because adds to beginnning and end -- want to just add in middle.

        for year in years:
            for week in range(0, 52):
                key = (year, week)
                if (not key in ids):
                    entry = dict(_id=dict(year=year, week=week), totalHours=0, count=0)
                    unsorted.append(entry)
        '''
        def key_comparator(x):
            return x["_id"]["year"] + (x["_id"]["week"] / 100)

        sorted_list = sorted(unsorted, key=key_comparator, reverse=True)
        for i in sorted_list:
            print(i)

        return sorted_list

'''
        # Make sure for each year the set is complete:
        for year in years:
            for week in range(0, 52):
                key = (year, week)
                if (not key in ids):
                    unsorted(appen)
'''


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
    startTime = None
    seconds = 0
    is_running = False

    def __init__(self, startTime=None):
        if startTime is None:
            self.startTime = datetime.utcnow()
        else:
            self.startTime = startTime

    def start(self):
        self.startTime = datetime.utcnow()
        self.is_running = True

    def stop(self):
        self.seconds = self.seconds + self.current_elapsed()
        self.is_running = False

    def current_elapsed(self):
        # current_elapsed is only diff between lastRestart and now if we're running.
        # If we're stopped then the total should haved been added to the seconds field
        # and current_elapsed is 0
        if not self.is_running:
            return 0
        now = datetime.utcnow()
        then = self.startTime
        return int((now - then).total_seconds())

    def total_elapsed(self):
        return self.current_elapsed() + self.seconds

    def counter(self):
        return self.fmt_seconds(self.total_elapsed())

    def fmt_seconds(self, seconds):
        hrs = int(seconds/3600)
        mins_secs = seconds % 3600
        mins = int(mins_secs / 60)
        secs = mins_secs % 60
        return "{:0>2}:{:0>2}:{:0>2}".format(hrs, mins, secs)

class TimerFormatter(ModelFormatter):
    def model_to_dict(self, object_as_model, include=None, exclude=None):
        timer_dict = ModelFormatter.model_to_dict(self, object_as_model, include, exclude)
        timer_dict["id"] = None
        if object_as_model.id is not None:
            timer_dict["id"] = str(object_as_model.id)
        #timer_dict["dateEntered"] = str(object_as_model.dateEntered)
        timer_dict["dateEntered"] = self.fmt_date(object_as_model.dateEntered)
        timer_dict["lastRestart"] = str(object_as_model.lastRestart)
        return timer_dict

    def fmt_date_time(self, dt):
        return dt.strftime("%a, %b %d, %Y %H:%M")

    def fmt_date(self, dt):
        return dt.strftime("%m/%d/%Y")

    # Returns a tuple with (hours, minutes)
    # Rounds any seconds to the nearest minute.
    def seconds_to_hours_and_minutes(self, seconds):
        hours = int(seconds /  3600)
        minutes = int((seconds - (hours * 3600)) / 60)
        seconds_remaining = seconds % 60
        if seconds_remaining >= 30:
            minutes += 1
        return (hours, minutes)

    # year is just a number representing a year, week is the zero
    # based week of the year.  Returns a formatted
    # string representing the "week ending" MM/DD/YYYY value --
    # weeks end on Saturday following Mongo's $week operator
    def get_week_ending_date(self, year, week):
        new_years_day = date(year, 1, 1)
        new_years_weekday = new_years_day.weekday()
        SATURDAY = 5 # Python datetime implementation
        if(new_years_weekday <= SATURDAY):
            day_first_week_ends = 1 + (SATURDAY - new_years_weekday)
        else:
            day_first_week_ends = 1 + SATURDAY + 1 # Ends on Sunday

        date_first_week_ends = date(year, 1, day_first_week_ends)
        given_week_ends = date_first_week_ends + timedelta(weeks=(week))
        return self.fmt_date(given_week_ends)
