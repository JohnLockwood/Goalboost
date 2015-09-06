# from test.common.test_helper import TestHelper
import requests
import json

class TimerTest():
    def add_timer_and_create_john_lockwood(self):
        one_hour = 60 * 60
        # See DATE_FORMAT under http://python-eve.org/config.html#schema to customize
        sample_timer = {"firstname": "John", "lastname": "Lockwood", "current_timer": {"start": "Fri, 04 Sep 2015 14:50:00 GMT", "length": 3600, "notes": "Victory is mine if this comes back"}}
        timer_url = "http://localhost:5001/api/people"
        print(json.dumps(sample_timer))
        resp = requests.post(timer_url, headers={'Content-type': 'application/json'}, data = json.dumps(sample_timer))
        assert(resp.status_code == 201)

    def patch_my_timer(self):
        # See DATE_FORMAT under http://python-eve.org/config.html#schema to customize

        # Here's the whole sequence.  In practice however we would not look up John Lockwood, we'd know his user id as logged in user
        lookup_url = "http://localhost:5001/api/people?where={%22firstname%22:%20%22John%22,%20%22lastname%22:%22Lockwood%22}"
        lookup_response = requests.get(lookup_url)
        lookup_response_data = json.loads(lookup_response.text)
        id = lookup_response_data["_items"][0]["_id"]
        sample_timer = {"current_timer": {"start": "Fri, 04 Sep 2015 14:50:00 GMT", "length": 7200, "notes": "Two hours is awesome!"}}
        timer_url = "http://localhost:5001/api/people/55ea26b18c57cf57605d250d"
        print(json.dumps(sample_timer))
        resp = requests.patch(timer_url, headers={'Content-type': 'application/json',  "X-HTTP-Method-Override": "PATCH", "If-Match":"cb9739d50f2f7414ae9fa6354db094e71f8b5ff2"}, data = json.dumps(sample_timer))
        assert(resp.status_code == 201)

if __name__ == "__main__":
    test = TimerTest()
    test.patch_my_timer()
    # test.add_timer_and_create_john_lockwood()

