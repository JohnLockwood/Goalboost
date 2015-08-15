# Todo - LOTS OF CLEANUP needed here

from unittest import TestCase
from alguito.endpoints.eve.auth import encode_basicauth_username_and_password, TeamAndPasswordAuth
import alguito.app
from pymongo import MongoClient
import werkzeug.security as security

__author__ = 'john'

class TestAuth(TestCase):
    def setUp(self):
        self.app = alguito.app.app.test_client()

    def tearDown(self):
        pass # print("Outa here!")

    def test_check_auth_fails_if_no_username_sent(self):
        response = self.app.get("/api/alguitos")
        assert response.status_code == 401

    """ This test is commented out now because alguitos no longer uses this auth method
    def test_check_auth_succeeds_if_username_sent(self):
        This test is commented out now because alguitos no longer uses this auth method

            Since this authentication method is currently bogus, it works for any Username

            We send a valid Basic auth authorization header, 'Basic QW55QmFkVXNlcm5hbWU6',
            corresponding to username = 'AnyBadUsername' and password = ''.  We got
            this value from Postman.

            Note we send "AUTHORIATION", which becomes "HTTP_AUTHORIZATION" when werkzeug
            is through with it.

        header_value = 'Basic QW55QmFkVXNlcm5hbWU6'
        response = self.app.get("/api/alguitos", headers={'AUTHORIZATION': header_value})
        assert response.status_code == 200
    """

    '''
    Also deprecated because alguito doesn't use this now!
    # Todo this is really testing a function in Auth module, not part of TestAlguitoTokenAuth
    def test_with_auth_using_encoding_function(self):
        """  Same as test_check_auth_succeeds_if_username_sent, but not hardcoded.
        """
        header_value = encode_basicauth_username_and_password(b"AnyBadUsername", b"")
        response = self.app.get("/api/alguitos", headers={'AUTHORIZATION': header_value})
        assert response.status_code == 200
    '''

    def test_team_and_password_auth_succeeds_good_login(self):
        auth = TeamAndPasswordAuth()
        username = 'elitepropertiesbroker@gmail.com'
        password = 'Foopdewop1912'

        eve_settings =  alguito.app.eve_settings
        # assert eve_settings is not None

        # Try generating and checking using hash functions
        hashed_password = security.generate_password_hash(password)
        is_secret = security.check_password_hash(hashed_password, password)
        assert is_secret
'''
        client = MongoClient(eve_settings['MONGO_HOST'], eve_settings['MONGO_PORT'])
        db = client[eve_settings['MONGO_DBNAME']]
        new_app = {
            'username' : username,
            'password' : hashed_password,
            'team'     : 'CodeSolid'
        }
        db.accounts.insert(new_app)
'''
#        auth.check_auth(username, password, 0, 'alguitos', 'GET')
        #db.accounts.remove({'username': username})
