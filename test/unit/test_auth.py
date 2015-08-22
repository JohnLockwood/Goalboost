# Todo - LOTS OF CLEANUP needed here

from unittest import TestCase
from test.common.test_helper import TestHelper
from alguito.endpoints.eve.auth import encode_basicauth_username_and_password, TeamAndPasswordAuth
import werkzeug.security as security

class TestAuth(TestCase):
    def setUp(self):
        self.testHelper= TestHelper()

    def tearDown(self):
        pass # print("Outa here!")

    def test_team_and_password_auth_succeeds_good_login(self):
        pass
        '''
        auth = TeamAndPasswordAuth()
        username = 'elitepropertiesbroker@gmail.com'
        password = 'Foopdewop1912'

        eve_settings =  self.testHelper.eve_settings()
        db = self.testHelper.database()

        assert eve_settings is not None

        # Try generating and checking using hash functions
        hashed_password = security.generate_password_hash(password)
        is_secret = security.check_password_hash(hashed_password, password)
        assert is_secret
        # Todo remove me this is just some demo insert code.
        new_app = {
            'username' : username,
            'password' : hashed_password,
            'team'     : 'CodeSolid'
        }
        db.accounts.insert(new_app)
        # db.accounts.remove({'username': username})
        '''
