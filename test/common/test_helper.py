import random
import string
import alguito.app
from pymongo import MongoClient

class TestHelper():
    """Helper or delegate class with functions for unit and integration tests
    For now we assume that one database connection per TestDelegate is sufficient

    """
    def __init__(self):
        self._app = alguito.app
        eve_settings = self.eve_settings()
        self.client = MongoClient(eve_settings['MONGO_HOST'], eve_settings['MONGO_PORT'])
        self.db = self.client[eve_settings['MONGO_DBNAME']]

    def __del__(self):
        self.client.disconnect()
        pass

    def app(self):
        return self._app

    def test_client(self):
        return self._app.app.test_client()

    def eve_settings(self):
        return self._app.eve_settings

    def database(self):
        return self.db

    def site_root(self):
        return "http://localhost:5001/"

    def api_root(self):
        return self.site_root() + "api/"

    def random_string(self, length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))
