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
