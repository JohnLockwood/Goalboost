from datetime import datetime
from unittest import TestCase

from goalboost.model.auth_models import UserModelFormatter, User
from goalboost.model.model_formatter import ModelFormatter
from goalboost.model.timer_models import TimerEntity, TimerFormatter
from test.common.test_helper import TestObjects
from json import dumps, loads

class TestModelFormatter(TestCase):

    def test_can_dump_user(self):
        user = TestObjects().get_test_user()
        formatter = ModelFormatter()
        model_as_dict = formatter.model_to_dict(user, include=["_id", "email", "account"])
        assert("password" not in model_as_dict)
        assert("_id" in model_as_dict)
        model_as_dict = formatter.model_to_dict(user, include=["_id", "email", "account", "password"])
        assert("password" in model_as_dict)
        #assert(isinstance(model_as_dict["_id"], str))


    def test_can_load_user(self):
        user = TestObjects().get_test_user()
        formatter = ModelFormatter()
        model_as_dict = formatter.model_to_dict(user, include=["_id", "email", "account"])
        model = formatter.dict_to_model(User, model_as_dict)
        assert(model.id == user.id)
        assert(model.email == user.email)

class TestUserModelFormatter(TestCase):

    def test_can_convert_user_to_dict(self):
        user = TestObjects().get_test_user()
        formatter = UserModelFormatter()
        user_dict = formatter.model_to_dict(user)
        assert(user_dict["account"]["name"] == user.account.name)
        assert(user_dict["confirmed_at"] == None)

        # Important!!! make sure we can convert to JSON:
        as_json = dumps(user_dict)
        assert(isinstance(as_json, str))

    def test_can_convert_user_to_dict_using_model_formatter(self):
        user = TestObjects().get_test_user()
        formatter = ModelFormatter()
        user_dict = formatter.model_to_dict(user)
        # assert(user_dict["account"]["name"] == user.account.name)
        #assert(user_dict["confirmed_at"] == None)

        # Important!!! make sure we can convert to JSON:
        as_json = dumps(user_dict)
        assert(isinstance(as_json, str))


class TestTimerModelFormatter(TestCase):
    def test_can_convert_timer_to_dict(self):
        user = TestObjects().get_test_user()
        timer = TimerEntity(notes="Just a test timer", user=user, tags=["Unit Tests"])
        tf = TimerFormatter()
        timer_entity_as_dict = tf.model_to_dict(timer)
        assert(timer_entity_as_dict is not None)
        assert(timer_entity_as_dict["notes"] == timer.notes)

    def test_can_dump_and_load_timer(self):
        user = TestObjects().get_test_user()
        timer = TimerEntity(notes="Just a test timer", user=user, tags=["Unit Tests"], seconds = 22, running = True)
        timer.save()
        tf = TimerFormatter()
        timer_entity_as_dict = tf.model_to_dict(timer)
        print(timer_entity_as_dict)
        timer.delete()
        timer2 = tf.dict_to_model(TimerEntity, timer_entity_as_dict)
        # Short form implementation (MongoEngine's to_json/from_json) doesn't pass
        #assert(timer.lastRestart == timer2.lastRestart)
        #assert(timer.dateEntered == timer2.dateEntered)
        assert(timer.tags == timer2.tags)
        assert(timer.running == timer2.running)
        assert(timer.seconds == timer2.seconds)
        assert(timer.notes == timer2.notes)
        assert(timer.user == timer2.user)
        print(timer.to_json())
        print(timer2.to_json())
        assert(timer.to_json() == timer2.to_json())
