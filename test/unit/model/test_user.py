from unittest import TestCase
from alguito.datastore import db
from test.common.test_helper import TestHelper
from flask import current_app
from alguito.mod_auth.mongo_models import User

class TestAuth(TestCase):

    def setUp(self):

        self.testHelper= TestHelper()
        self.security = self.testHelper.app().security

    def test_can_create_and_save_user(self):
        with self.testHelper.app().app_context():
            user = None
            try:

                user_data_store = self.security.datastore
                user = user_data_store.create_user(email="melblank@bugs.com", account="foghorn", password="What'sUpDocument")
                user2 = user_data_store.find_user(email="melblank@bugs.com")
                assert(user.email == user2.email)
                assert(user.account == user2.account)
                # Clean up
            finally:
                if(user is not None):
                    user_data_store.delete_user(user)



