from unittest import TestCase

from goalboost.model.auth_models import UserSchema, AccountSchema, UserModelFormatter
from goalboost.model.goalboost_model_schema import ModelFormatter
from test.common.test_helper import TestObjects
from json import dumps, loads
class TestUserSchema(TestCase):

    # Use provided "dump" method to get all fields.  This is insecure
    def test_can_dump_dict(self):
        user = TestObjects().get_test_user()
        user_schema = UserSchema()
        dumped = user_schema.dump(user)
        data = dumped.data
        assert(type(data) == type(dict()))
        assert("password" in data)
        assert(data["password"] is not None)

        # This whole test works but proves nothing inasmuch as the following line doesn't work
        # json_data = dumps(data)

        # --> print("The user's password (this is bad!!!) is: " + data["password"])

    # Use dump_exclude (goalboost_model_schema.py) method to exclude password
    def test_can_filter_password(self):
        user = TestObjects().get_test_user()
        user_schema = UserSchema()
        data = user_schema.dump_exclude(user, exclude=["password"]).data
        assert(not "password" in data)
        assert("id" in data)

    def test_can_load_user_account(self):
        user = TestObjects().get_test_user()
        print(user.to_json())
        print(user.account.to_json())

class TestAccountSchema(TestCase):

    def test_can_dump_and_load_account(self):
        account = TestObjects().get_test_account()
        account_schema = AccountSchema()
        data = account_schema.dump(account).data
        assert data is not None

        # It's a a dict, awesome, can return it in API
        assert(type(data) == type(dict()))

        # Data looks good
        assert(data["name"] == account.name)

        # And we can filter if needed, for example...
        # Now we have the id field...
        assert("id" in data)

        # And now we don't
        data2 = account_schema.dump_exclude(account, exclude=["id"]).data
        assert "id" not in data2

        # Try reloading from dict --> object
        # Note that we need the "data" off of what's loaded, load doesn't return the
        # object directly (just like "dump")
        account2 = account_schema.load(data).data
        assert(type(account2) == type(account))
        assert(account.name == account2.name)
        assert(account.id == account2.id)

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
