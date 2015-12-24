from unittest import TestCase
import requests
from json import dumps, loads

from requests.auth import HTTPBasicAuth

from test.common.test_helper import TestObjects
# from goalboost.model.models_auth import User

test_server = "http://localhost:5000"

class TestTimer(TestCase):
    def setUp(self):
        pass

    def get_test_timer(self):
        test_timer = dict(entries = [dict(seconds=300, dateRecorded='2015-11-23 00:00:00')], notes='Just writing integration tests here, boss!')
        return test_timer

    def test_can_post_and_delete_timer(self):
        response = requests.post(url=test_server + "/api/timer", data = dumps(self.get_test_timer()), headers={'content-type' : 'application/json'})
        assert(response.status_code == 201)
        id = response.json()["id"];
        assert(id is not None)
        assert(type(id) is str)
        assert(len(id) > 0)

        response = requests.get(url=test_server + "/api/timer/" + id)
        assert(response.status_code == 200)

        response = requests.delete(url=test_server + "/api/timer/" + id)
        assert(response.status_code == 204)

        response = requests.get(url=test_server + "/api/timer/" + id)
        assert(response.status_code == 404)

    # Todo cleanup dupication this and next test
    def test_login(self):
        # Ensure test user created
        test_objects = TestObjects()
        userOriginal = test_objects.get_test_user()
        try:
            email, password = test_objects.get_test_user_credentials()
            credentials = dict(email = email , password = password)
            login_payload = dumps(credentials)
            response = requests.post(url=test_server + "/login", data=login_payload, headers={'content-type' : 'application/json'})
            assert(response.status_code == 200)
            response_object = response.json()

            user = response_object["response"]["user"]
            assert(user["id"] is not None)
            assert(user["authentication_token"] is not None)
        finally:
            # Cleanup
            userOriginal.delete()

    # This shows how to login user for API, to get
    def test_login_and_use_resource(self):
        # Ensure test user created
        test_objects = TestObjects()
        userOriginal = test_objects.get_test_user()
        try:
            email, password = test_objects.get_test_user_credentials()
            credentials = dict(email = email, password = password)
            login_payload = dumps(credentials)
            response = requests.post(url=test_server + "/login", data=login_payload, headers={'content-type' : 'application/json'})
            assert(response.status_code == 200)
            response_object = response.json()

            user = response_object["response"]["user"]

            basic_auth_credentials = HTTPBasicAuth(email, user["authentication_token"])
            response = requests.get(url=test_server + "/auth/api/resource", headers={'content-type' : 'application/json'}, auth=basic_auth_credentials)
            assert(response.status_code == 200)
            assert("hello" in str(response.json()))
            print(response.json())
        finally:
            #Cleanup
            userOriginal.delete()








