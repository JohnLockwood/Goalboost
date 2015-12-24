from unittest import TestCase

from goalboost.model.auth_models import UserModelFormatter
from goalboost.model.model_formatter import ModelFormatter
from test.common.test_helper import TestObjects
from json import dumps, loads

class TestModelFormatter(TestCase):

    def test_can_dump_user(self):
        user = TestObjects().get_test_user()
        formatter = ModelFormatter()
        model_as_dict = formatter.model_to_dict(user, include=["id", "email", "account"])
        assert("id" in model_as_dict)
        assert(isinstance(model_as_dict["id"], str))
        print(model_as_dict)

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
