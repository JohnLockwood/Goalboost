from unittest import TestCase
import requests
from json import dumps, loads
from requests.auth import HTTPBasicAuth

from goalboost.model.timer_models import TimerEntity, TimerFormatter
from test.common.test_helper import TestObjects
import http.client

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
        assert(response.status_code == http.client.OK)

class TestSecureEndpoint(TestCase):
    def test_can_get_token(self):
        token1 = test_credentials.get_auth_token()
        token2 = test_credentials.get_auth_token()
        assert(id(token1) == id(token2))

    def test_secure_endpoint_returns_401_without_token(self):
        response = requests.get(v1_api + "/test/secure_test")
        assert(response.status_code == http.client.UNAUTHORIZED)

    def test_secure_endpoint_returns_200_with_token(self):
        token = test_credentials.get_auth_token()
        response = requests.get(v1_api + "/test/secure_test", headers={'content-type' : 'application/json'}, auth=token)
        assert(response.status_code == http.client.OK)

class TestV1Timer(TestCase):
    def test_timer_post_get_delete(self):
        token = test_credentials.get_auth_token()
        user = TestObjects().get_test_user()
        timer = TimerEntity(notes="Just a test timer", user=user, tags=["Unit Tests"], seconds = 22, running = True)
        timer_dict = TimerFormatter().model_to_dict(timer)

        # Not authorized w/o token
        response = requests.post(v1_api + "/timer", headers={'content-type' : 'application/json'}, data=timer.to_json())
        assert(response.status_code == http.client.UNAUTHORIZED)

        # With token, should get "CREATED"
        response = requests.post(v1_api + "/timer", headers={'content-type' : 'application/json'}, auth=token, data=timer.to_json())
        assert(response.status_code == http.client.CREATED)

        # Object location
        url = response.headers["Location"]

        # Not authorized without the token (401)
        response = requests.get(url)
        assert(response.status_code == http.client.UNAUTHORIZED)

        # Re-send the request with the token, this time get OK (200)
        response = requests.get(url, auth=token)
        assert(response.status_code == http.client.OK)
        timer_dict2 = loads(response.text)
        assert(timer_dict2["seconds"] == 22)

        # Update the seconds and PUT the request
        timer_dict2["seconds"] = 99
        response = requests.put(url, headers={'content-type' : 'application/json'}, auth=token, data=dumps(timer_dict2))
        assert(response.status_code == http.client.OK)
        response = requests.get(url, auth=token)
        assert(response.status_code == http.client.OK)
        timer_dict3 = loads(response.text)
        assert(timer_dict3["seconds"] == 99)



        # Delete the resource
        response = requests.delete(url, auth=token)
        assert(response.status_code == http.client.NO_CONTENT)

