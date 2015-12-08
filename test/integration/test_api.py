from unittest import TestCase
import requests
from json import dumps, loads

from bson import ObjectId
from requests.auth import HTTPBasicAuth

from test.common.test_helper import test_data
from goalboost.model.models_auth import User

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

    def test_login(self):
        # Assumes test user was created same SECRET KEY we're using in test

        email = test_data["TEST_USER_EMAIL"]
        password = test_data.get("TEST_USER_PASSWORD")
        credentials = dict(email = test_data["TEST_USER_EMAIL"], password = test_data["TEST_USER_PASSWORD"])
        login_payload = dumps(credentials)
        response = requests.post(url=test_server + "/login", data=login_payload, headers={'content-type' : 'application/json'})
        assert(response.status_code == 200)
        response_object = response.json()

        user = response_object["response"]["user"]
        assert(user["id"] is not None)
        assert(user["authentication_token"] is not None)

    def test_login_and_use_resource(self):
        # Assumes test user was created same SECRET KEY we're using in test

        email = test_data["TEST_USER_EMAIL"]
        password = test_data.get("TEST_USER_PASSWORD")
        credentials = dict(email = test_data["TEST_USER_EMAIL"], password = test_data["TEST_USER_PASSWORD"])
        login_payload = dumps(credentials)
        response = requests.post(url=test_server + "/login", data=login_payload, headers={'content-type' : 'application/json'})
        assert(response.status_code == 200)
        response_object = response.json()

        user = response_object["response"]["user"]

        basic_auth_credentials = HTTPBasicAuth(email, user["authentication_token"])
        response = requests.get(url=test_server + "/auth/api/resource", headers={'content-type' : 'application/json'}, auth=basic_auth_credentials)
        assert(response.status_code == 200)
        response_object = response.json()

        print (response_object)







