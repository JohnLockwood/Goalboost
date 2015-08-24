import alguito.app
from pymongo import MongoClient

# Todo To do a lot of this needs to be abstracted into it's own DB connection management class
# or better yet see about using Eve's
class RegistrationModel(object):

    def __init__(self):
        self._app = None
        self.db = None
        self.client = None

    def open_db(self):
        if not self._app:
            self._app = alguito.app
            eve_settings = self.eve_settings()
            self.client = MongoClient(eve_settings['MONGO_HOST'], eve_settings['MONGO_PORT'])
            self.db = self.client[eve_settings['MONGO_DBNAME']]

    def close_db(self):
        self.client.disconnect()
        self.db = None
        self._app = None
        self.client = None

    def __del__(self):
        if self.client:
            self.close_db()
            self.client.disconnect()

    def __init__(self):
        self.db = None

    def open_db(self):
        pass

    def teamExists(self, teamName):
        return False
