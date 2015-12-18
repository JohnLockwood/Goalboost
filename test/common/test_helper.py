import random
import string
from goalboost.model.models_auth import User, Account

from bson import ObjectId
from goalboost import app


class TestObjects():
    test_data = dict(TEST_ACCOUNT_NAME="TestBoost",
                     TEST_ACCOUNT_ID=b"TestBoost123",
                     DEMO=ObjectId(b"DEMOdemoDEMO"),
                     TEST_USER_ID=ObjectId(b"TestUserDEMO"),
                     TEST_USER_EMAIL = "TestUser@examples.coop",
                     TEST_USER_PASSWORD = "Geronimo")

    def get_test_user(self):
        account = self.get_test_account()
        email, password = self.get_test_user_credentials()
        try:
            user = User(email=email, accountId=self.get_demo_account_id(), password=password)
            user.save()
        except: # Don't care if already created
            user = User.objects(email=email).first()
        return user

    def get_test_user_credentials(self):
        email = self.test_data["TEST_USER_EMAIL"]
        password = self.test_data.get("TEST_USER_PASSWORD")
        return (email, password)

    def get_demo_account_id(self):
        return self.test_data["DEMO"]

    def get_test_account(self):
        account = None
        try:
            account = Account.objects(name=self.test_data["TEST_ACCOUNT_NAME"]).first()
            if account is None:
                account = Account(name=self.test_data["TEST_ACCOUNT_NAME"], id=self.test_data["TEST_ACCOUNT_ID"] )
                account.save()
        except:
            pass
        return account

    def get_any_id(self):
        return self.test_data["DEMO"]

class TestHelper():
    """Helper or delegate class with functions for unit and integration tests
    For now we assume that one database connection per TestDelegate is sufficient

    """
    def __init__(self):
        self._app = app

    def __del__(self):
        pass

    def app(self):
        return self._app

    def test_client(self):
        return self._app.test_client()

    def site_root(self):
        return "http://localhost:5001/"

    def api_root(self):
        return self.site_root() + "api/"

    # C.f. http://nullege.com/codes/search/eve.Eve.test_request_context
    # and http://flask.pocoo.org/docs/0.10/api/#flask.Flask.test_request_context
    def test_request_context(self):
        return self._app.test_request_context()

    def random_string(self, length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))


