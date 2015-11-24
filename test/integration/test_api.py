from unittest import TestCase
import requests
from json import dumps, loads
api_root = "http://localhost:5000/api/"

class TestTimer(TestCase):
    def setUp(self):
        pass

    def get_test_timer(self):
        test_timer = dict(entries = [dict(seconds=300, dateRecorded='2015-11-23 00:00:00')], notes='Just writing integration tests here, boss!')
        return test_timer

    def test_can_post_and_delete_timer(self):
        response = requests.post(url=api_root + "timer", data = dumps(self.get_test_timer()), headers={'content-type' : 'application/json'})
        assert(response.status_code == 201)
        id = response.json()["id"];
        assert(id is not None)
        assert(type(id) is str)
        assert(len(id) > 0)

        response = requests.get(url=api_root + "timer/" + id)
        assert(response.status_code == 200)

        response = requests.delete(url=api_root + "timer/" + id)
        assert(response.status_code == 204)

        response = requests.get(url=api_root + "timer/" + id)
        assert(response.status_code == 404)


