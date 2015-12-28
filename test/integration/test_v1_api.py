from unittest import TestCase
import requests
from json import dumps, loads
from requests.auth import HTTPBasicAuth

from goalboost.model.timer_models import TimerEntity
from test.common.test_helper import TestObjects

test_server = "http://localhost:5000"
v1_api = test_server + "/api/v1"


class TestCredentials():
    credential_map = {}


    def get_auth_token(self):
        user = TestObjects().get_test_user()        # Force user creation
        credentials_tuple = TestObjects().get_test_user_credentials()
        credentials = dict(email=credentials_tuple[0], password=credentials_tuple[1])
        key = str(credentials)
        if (not key in self.credential_map):
            response = requests.post(url=test_server + "/login", data=dumps(credentials), headers={'content-type' : 'application/json'})
            assert(response.status_code == 200)
            response_object = response.json()
            # TODO Note also need error case -- this assumes we passed:
            user_response = response_object["response"]["user"]
            basic_auth_credentials = HTTPBasicAuth(credentials["email"],  user_response["authentication_token"])
            self.credential_map[key] = basic_auth_credentials
        return self.credential_map[key]

test_credentials = TestCredentials()

class SanityCheck(TestCase):
    def test_can_call_test_endpoint(self):
        response = requests.get(v1_api + "/test")
        assert(response.status_code == 200)

class TestSecureEndpoint(TestCase):
    def test_can_get_token(self):
        token1 = test_credentials.get_auth_token()
        token2 = test_credentials.get_auth_token()
        assert(id(token1) == id(token2))

    def test_secure_endpoint_returns_401_without_token(self):
        response = requests.get(v1_api + "/secure_test")
        assert(response.status_code == 401)


    def test_secure_endpoint_returns_200_with_token(self):
        token = test_credentials.get_auth_token()
        response = requests.get(v1_api + "/secure_test", headers={'content-type' : 'application/json'}, auth=token)
        assert(response.status_code == 200)


class TestV1Timer(TestCase):
    def test_post_timer(self):
        token = test_credentials.get_auth_token()
        timer = TimerEntity(notes="Testing V1 Post, chief")
        response = requests.post(v1_api + "/timer", headers={'content-type' : 'application/json'}, auth=token, data="")