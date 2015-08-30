from unittest import TestCase
from test.common.test_helper import TestHelper
from alguito.endpoints.eve.auth import TeamAndPasswordAuth

class TestAuth(TestCase):
    def setUp(self):
        self.testHelper= TestHelper()

    def test_team_and_password_auth_succeeds_good_login(self):
        auth = TeamAndPasswordAuth()
        username = 'elitepropertiesbroker@gmail.com'
        password = 'Foopdewop1912'
        authorized = False
        with self.testHelper.test_request_context():
            authorized = auth.check_auth(username, password, None, 'alguitos', 'PUT')
        assert(authorized)

    def test_team_and_password_auth_fails_bad_login(self):
        auth = TeamAndPasswordAuth()
        username = 'elitepropertiesbroker@gmail.com'
        password = 'no_i_am_not_your_password'
        authorized = True
        with self.testHelper.test_request_context():
            authorized = auth.check_auth(username, password, None, 'alguitos', 'PUT')
        assert(not authorized)