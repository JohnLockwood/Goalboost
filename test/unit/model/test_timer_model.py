# -------------- Timers ---------------------------
from datetime import datetime, timedelta
from json import dumps
from unittest import TestCase
import dateutil
from bson import ObjectId
from goalboost.model.datastore import create_timer
from goalboost.model.auth_models import User
from goalboost.model.timer_models import Timer, TimerEntity
from test.common.test_helper import TestHelper, TestObjects

class TestTimerEntity(TestCase):

    def test_can_save_and_load_timer(self):
        user = TestObjects().get_test_user()
        t = TimerEntity(id=TestObjects().get_any_id(), notes="Saved from unit test", user=user )
        t.save()
        t2 = TimerEntity.objects(id = t.id).first()
        assert(t.__repr__() == t2.__repr__())
        t.delete()

    def test_eval_ok(self):
        user = TestObjects().get_test_user()
        t1 = TimerEntity(id=ObjectId(b"Timer1Timer2"), notes="I want a shrubbery", user=user)
        print(t1.__repr__())
        t2 = eval(t1.__repr__())
        # Note this part works partly because compare is brain-dead, compares id only and only works for non-null id
        # But that may be what we need for MongoEngine purposes, so don't override
        assert(t1 == t2)
        # A better check
        assert(t1.__repr__() == t2.__repr__())
        print(t1.to_json())

    def test_user_not_updated_on_save(self):
        user = TestObjects().get_test_user()
        t1 = TimerEntity(id=ObjectId(b"Timer1Timer3"), notes="I want a shrubbery", user=user)
        t1.save()
        t1.user.password = "foo"
        t1.save()
        # TODO ETC...


# Derive from object temporarily to disable
class TestTimerLegacy(object):
    def test_can_create_with_utc_now(self):
        #userId = "561dcd3c8c57cf2c17b7f4f9"
        my_notes = "I want to know how long this took, but my code is brain dead so far.  Woe is me."
        timer = create_timer(notes=my_notes)
        assert(my_notes == timer.notes)
        timer.save()

    def test_can_start_and_stop(self):
        notes = "Testing start and stop"
        t = Timer(notes=notes)
        t.start()
        t.stop()


    def test_can_create_with_explicit_start(self):
        my_notes = "I am another timer"
        timer = create_timer(notes=my_notes, startTime=datetime(2007, 12, 5, 0, 0))
        assert(my_notes == timer.notes)
        assert(timer.startTime == timer.lastRestart)

    # timers created this way display an ugly ui bug -- so there's a bug either in the GUI or here or both.
    # Entered as
    # https://github.com/CodeSolid/Goalboost/issues/12
    def test_can_create_without_datastore(self):
        pass
        # Uncomment the following to see (and delete "pass" of course).
        # my_notes = "We don't need no steenkin datastore."
        # timer = Timer(id="56259a278c57cf02f9692ccc", userId = "561dcd3c8c57cf2c17b7f4f9", notes=my_notes)
        #
        # # This will be a bug that will appear in the UI -- no entry in the entries array is created for today!
        # # timer = Timer(id="56259a278c57cf02f9692ccc", userId = "561dcd3c8c57cf2c17b7f4f9", notes=my_notes, startTime=datetime(2007, 12, 5, 0, 0))
        # timer.save()
        # timer2 = Timer.objects(id="56259a278c57cf02f9692ccc").first()
        # assert(timer2.notes == timer.notes)
        # assert(my_notes == timer.notes)
        # assert(timer.startTime == timer.lastRestart)

    # Don't run in debugger, a breakpoint in right place will throw off elapsed calculation.
    # Otherwise elapsed converts to int, which shaves off any "running time" error
    def test_elapsed_time_correct(self):
        now = datetime.utcnow()
        tenSecondsAgo = now - timedelta(seconds=10)
        # Timer must be running or elapsed time will be zero
        timer = Timer(startTime = tenSecondsAgo, running=True)
        timer.set_seconds_today(20)
        elapsed = timer.current_elapsed()
        total = timer.total_elapsed()
        assert(elapsed == 10)
        assert(total == 30)

    def test_to_api_dict_correct(self):
        start_time = dateutil.parser.parse('2008-09-03T20:00:00.000000Z')
        # Timer must be running or elapsed time will be zero
        timer = Timer(startTime = start_time, running=True, id=ObjectId("56259a278c57cf02f9692b31"))
        d = timer.to_api_dict()
        json = dumps(d)
        assert('"notes": null' in json)
        assert('"id": "56259a278c57cf02f9692b31"' in json)
        assert('"entries": []' in json)
        #assert('"seconds": 20' in json)
        timer.notes = "Testing the JSON!"
        timer.set_seconds_today(99)
        d = timer.to_api_dict()
        json = dumps(d)
        assert('"notes": "Testing the JSON!"' in json)
        assert('"seconds": 99' in json)

    def test_can_load_from_api_dict(self):
        start_time = dateutil.parser.parse('2008-09-03T20:00:00.000000Z')
        # Timer must be running or elapsed time will be zero
        timer = Timer(startTime = start_time,  running=True, id=ObjectId("56259a278c57cf02f9692b31"))
        timer.set_seconds_today(99)
        d = timer.to_api_dict()
        t2 = Timer.load_from_dict(d)
        assert(timer.notes == t2.notes)
        assert(timer.id == t2.id)
        assert(timer.entries[0].dateRecorded == t2.entries[0].dateRecorded)
        assert(len(timer.entries) == len(t2.entries))
        assert(timer.entries[0].seconds == t2.entries[0].seconds)
        d["notes"] = "Testing"
        t2 = Timer.load_from_dict(d)
        assert(t2.notes == "Testing")
