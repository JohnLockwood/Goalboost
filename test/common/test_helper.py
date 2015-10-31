import random
import string
from alguito import app
from pymongo import MongoClient

class TestHelper():
    """Helper or delegate class with functions for unit and integration tests
    For now we assume that one database connection per TestDelegate is sufficient

    """
    def __init__(self):
        self._app = app

    def __del__(self):
        pass

    def app(self):
        return self._app

    def test_client(self):
        return self._app.test_client()

    def site_root(self):
        return "http://localhost:5001/"

    def api_root(self):
        return self.site_root() + "api/"

    # C.f. http://nullege.com/codes/search/eve.Eve.test_request_context
    # and http://flask.pocoo.org/docs/0.10/api/#flask.Flask.test_request_context
    def test_request_context(self):
        return self._app.test_request_context()

    def random_string(self, length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))


