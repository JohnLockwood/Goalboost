from unittest import TestCase
from test.common.test_helper import TestHelper
from goalboost.model.mongo_models import Task
from goalboost.model import db
from datetime import datetime, timedelta
from goalboost.model.datastore import create_timer
from goalboost.model.mongo_models import Timer
import dateutil.parser
from json import dumps
from bson.objectid import ObjectId
# -------------- Tasks ---------------------------
class TestTask(TestCase):
    def setUp(self):
        self.testHelper= TestHelper()

    # This works ok as is and only relies on TestHelper() having been called, c.f. setUp, above,
    # since TestHelper's __init__ calls create_app, which configures mongodb correctly
    def test_can_save_without_app(self):
        task = Task(name="Write another mongo entity", description="Save without an app!")
        task.save()

    def test_can_create_and_save_task(self):
        with self.testHelper.app().app_context():
            task = Task(name="Write a 1st mongo entity", description="Save with app context -- no difference")
            task.save()

    def test_can_create_and_save_task_another_way(self):
        with self.testHelper.app().test_request_context():
            try:
                task = Task(name="Write a 1st mongo entity", description="Save task with test_request_context -- no difference")
                task.save()
            finally:
                pass

# -------------- Timers ---------------------------
class TestTimer(TestCase):
    def test_can_create_with_utc_now(self):
        #userId = "561dcd3c8c57cf2c17b7f4f9"
        my_notes = "I want to know how long this took, but my code is brain dead so far.  Woe is me."
        timer = create_timer(notes=my_notes)
        assert(my_notes == timer.notes)
        timer.save()

    def test_can_create_with_explicit_start(self):
        my_notes = "I am another timer"
        timer = create_timer(notes=my_notes, startTime=datetime(2007, 12, 5, 0, 0))
        assert(my_notes == timer.notes)
        assert(timer.startTime == timer.lastRestart)

    def test_can_create_without_datastore(self):
        my_notes = "We don't need no steenkin datastore."
        timer = Timer(userId = "561dcd3c8c57cf2c17b7f4f9", notes=my_notes, startTime=datetime(2007, 12, 5, 0, 0))
        timer.save()
        timer2 = Timer.objects(userId="561dcd3c8c57cf2c17b7f4f9").first()
        assert(timer2.notes == timer.notes)
        assert(my_notes == timer.notes)
        assert(timer.startTime == timer.lastRestart)

    # Don't run in debugger, a breakpoint in right place will throw off elapsed calculation.
    # Otherwise elapsed converts to int, which shaves off any "running time" error
    def test_elapsed_time_correct(self):
        now = datetime.utcnow()
        tenSecondsAgo = now - timedelta(seconds=10)
        # Timer must be running or elapsed time will be zero
        timer = Timer(startTime = tenSecondsAgo, seconds = 20, running=True)
        elapsed = timer.current_elapsed()
        total = timer.total_elapsed()
        assert(elapsed == 10)
        assert(total == 30)

    def test_to_api_dict_correct(self):
        start_time = dateutil.parser.parse('2008-09-03T20:00:00.000000Z')
        # Timer must be running or elapsed time will be zero
        timer = Timer(startTime = start_time, seconds = 20, running=True, id=ObjectId("56259a278c57cf02f9692b31"))
        d = timer.to_api_dict()
        json = dumps(d)
        assert('"notes": null' in json)
        assert('"id": "56259a278c57cf02f9692b31"' in json)
        assert('"seconds": 20' in json)
        timer.notes = "Testing the JSON!"
        d = timer.to_api_dict()
        json = dumps(d)
        assert('"notes": "Testing the JSON!"' in json)

    def test_can_load_from_api_dict(self):
        start_time = dateutil.parser.parse('2008-09-03T20:00:00.000000Z')
        # Timer must be running or elapsed time will be zero
        timer = Timer(startTime = start_time, seconds = 20, running=True, id=ObjectId("56259a278c57cf02f9692b31"))
        d = timer.to_api_dict()
        t2 = Timer.load_from_dict(d)
        assert(timer.notes == t2.notes)
        assert(timer.id == t2.id)
        assert(t2.seconds == 20)
        d["notes"] = "Testing"
        t2 = Timer.load_from_dict(d)
        assert(t2.notes == "Testing")



# -------------- Users -----------------------------

class TestAuth(TestCase):

    def setUp(self):
        self.testHelper= TestHelper()
        self.security = self.testHelper.app().security

    def test_can_create_and_save_user(self):
        with self.testHelper.app().app_context():
            user = None
            try:
                user_data_store = self.security.datastore
                # -- Should and do really use encrypted password in prod, but slows tests down
                # encrypted = encrypt_password("WhatsUpDocument")
                user = user_data_store.create_user(email="melblank@bugs.com", account="foghorn", password="chickens")
                user2 = user_data_store.find_user(email="melblank@bugs.com")
                assert(user.email == user2.email)
                assert(user.account == user2.account)
                # Clean up
            finally:
                if(user is not None):
                    user_data_store.delete_user(user)