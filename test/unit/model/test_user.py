from unittest import TestCase
from test.common.test_helper import TestHelper
from flask_security.utils import encrypt_password

class TestAuth(TestCase):

    def setUp(self):

        self.testHelper= TestHelper()
        self.security = self.testHelper.app().security

    def test_can_create_and_save_user(self):
        with self.testHelper.app().app_context():
            user = None
            try:
                user_data_store = self.security.datastore
                encrypted = encrypt_password("WhatsUpDocument")
                user = user_data_store.create_user(email="melblank@bugs.com", account="foghorn", password=encrypted)
                user2 = user_data_store.find_user(email="melblank@bugs.com")
                assert(user.email == user2.email)
                assert(user.account == user2.account)
                # Clean up
            finally:
                if(user is not None):
                    user_data_store.delete_user(user)



