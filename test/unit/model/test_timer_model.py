# -------------- Timers ---------------------------
from datetime import datetime, timedelta
from json import dumps
from unittest import TestCase
import dateutil
from bson import ObjectId

from goalboost.model.auth_models import Account
from goalboost.model.timer_models import Timer, TimerDAO
from test.common.test_helper import TestHelper, TestObjects

class TestTimerEntity(TestCase):

    def test_can_save_and_load_timer(self):
        user = TestObjects().get_test_user()
        t = Timer(id=TestObjects().get_any_id(), notes="Saved from unit test", user=user)
        t.save()
        t2 = Timer.objects(id = t.id).first()
        assert(t.__repr__() == t2.__repr__())
        t.delete()

    def test_eval_ok(self):
        user = TestObjects().get_test_user()
        t1 = Timer(id=ObjectId(b"Timer1Timer2"), notes="I want a shrubbery", user=user)
        # print(t1.__repr__())
        t2 = eval(t1.__repr__())
        # Note this part works partly because compare is brain-dead, compares id only and only works for non-null id
        # But that may be what we need for MongoEngine purposes, so don't override
        assert(t1 == t2)
        # A better check
        assert(t1.__repr__() == t2.__repr__())
        # print(t1.to_json())

    def test_user_not_updated_on_save(self):
        user = TestObjects().get_test_user()
        t1 = Timer(id=ObjectId(b"Timer1Timer3"), notes="I want a shrubbery", user=user)
        t1.save()
        t1.user.password = "foo"
        t1.save()
        # TODO ETC...
        t1.delete()


# This tests the new refactored TimerDAO that takes a Timer
class TestTimerDAO(TestCase):
    def test_save_timer(self):
        dao = TimerDAO()
        t1 = Timer(notes="My Test LegacyTimer Running!", user=TestObjects().get_test_user(), running=True)
        dao.put(t1)
        assert(t1.id is not None)

    def test_can_get_users(self):
        account = Account.objects(name="Goalboost").first()
        users = account.get_users()
        #print(len(users))
        goalboost_timers = TimerDAO().get_timers_for_users(users, tag_list=["Goalboost"])
        assert(len(goalboost_timers) >  0)
        assert(type(goalboost_timers[0] == type(Timer())))
        print(len(goalboost_timers))

        all_timers = TimerDAO().get_timers_for_users(users)
        assert(len(all_timers) > len(goalboost_timers))

    def test_can_get_timer_stats_by_week(self):
        account = Account.objects(name="Goalboost").first()
        users = [user.id for user in account.get_users()]
        goalboost_timers = TimerDAO().get_weekly_timer_statistics(users, ["Goalboost"])
        assert(len(goalboost_timers) > 5)

# Derive from object temporarily to disable
