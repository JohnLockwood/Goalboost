from unittest import TestCase
from test.common.test_helper import TestHelper, TestObjects # test_data
from datetime import datetime, timedelta
from goalboost.model.datastore import create_timer
from goalboost.model.mongo_models import Project, Tag
from goalboost.model.models_auth import Account, User
from goalboost.model.models_timer import Timer
import dateutil.parser
from json import dumps
from bson.objectid import ObjectId
import time


# Allows us to consider reserved object Ids for testing.
# Not so much a test as a proof of concept
class TestObjectId(TestCase):
    def test_can_get_non_random_object_id(self):
        oid = ObjectId(b"CodeSolid123")
        oid2 = ObjectId(b"CodeSolid123")
        assert (oid == oid2)

    def test_can_get_random_object_id(self):
        oid = ObjectId()
        oid2 = ObjectId()
        assert (oid != oid2)


# -------------- Timers ---------------------------
class TestTimer(TestCase):
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

# -------------- Accounts -------------------------
class TestAccount():
    def test_can_create_and_delete_account(self):
        id = ObjectId("TempTempTemp")
        account = Account(id=id, name="Los Pollos Hermanos")
        account.save()
        account2 = Account.objects(id=account.id).first()
        assert(account2.name == account.name)
        Account.objects(id=account.id).delete()

class TestTag(TestCase):
    def test_can_create_tag(self):
        t = Tag(accountId = TestObjects().get_demo_account_id(), name="Goalboost")
        assert(t is not None)
        t.save()
        t2 = Tag.objects(name="Goalboost").first()
        assert(t2.id == t.id)
        t2 = Tag.objects(name="Goalboost").delete()

# -------------- Projects -------------------------
class TestProject(TestCase):
    def setUp(self):
        self.testHelper= TestHelper()

    def test_can_save_load_delete_projects(self):
        p1 = Project(name="CodeSolid Awesome Stuff")
        p1.save()
        p2 = Project.objects(id=p1.id).first()
        assert(p2.name == p1.name)
        Project.objects(id=p1.id).delete()
#  -------------- Users -----------------------------


class TestAuth(TestCase):

    def setUp(self):
        self.testHelper= TestHelper()
        self.security = self.testHelper.app().security

    def test_can_create_and_save_user(self):
        with self.testHelper.app().app_context():
            user = None
            try:
                user_data_store = self.security.datastore

                uTemp = User.objects(email="melblank@bugs.com").first()
                if uTemp is not None:
                    uTemp.delete()

                # -- Should and do really use encrypted password in prod, but slows tests down
                # encrypted = encrypt_password("WhatsUpDocument")
                user = user_data_store.create_user(email="melblank@bugs.com", accountId=TestObjects().get_demo_account_id(), password="chickens")
                user2 = user_data_store.find_user(email="melblank@bugs.com")
                assert(user.email == user2.email)
                assert(user.accountId == user2.accountId)
                # Clean up
            finally:
                if(user is not None):
                    user_data_store.delete_user(user)

    def test_can_verify_token(self):
        with self.testHelper.app().app_context():
            user = None
            try:
                user_data_store = self.security.datastore
                # -- Should and do really use encrypted password in prod, but slows tests down
                # encrypted = encrypt_password("WhatsUpDocument")
                user = user_data_store.create_user(email="melblank@bugs.com", accountId=TestObjects().get_demo_account_id(), password="chickens")
                # print(str(type(user)))
                token = user.get_auth_token()
                token2 = token
                assert(token == token2)
                result = user.verify_auth_token(token)
                assert(result)
                # Clean up
            finally:
                if(user is not None):
                    user_data_store.delete_user(user)
