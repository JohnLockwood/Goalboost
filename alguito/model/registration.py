import alguito.app
from pymongo import MongoClient

# Todo To do a lot of this needs to be abstracted into it's own DB connection management class
# or better yet see about using Eve's
class RegistrationModel(object):

    def __init__(self, db):
        self.db = db

    def open_db(self):
        pass

    def get_document(self, teamName):
        return {'name': teamName}

    def team_exists(self, teamName):
        if teamName is None: return False
        teams = self.db["teams"]
        account = teams.find_one(self.get_document(teamName))
        return account is not  None

    def insert_team(self, teamName):
        if self.team_exists(teamName): return False
        teams = self.db["teams"]
        id = teams.save(self.get_document(teamName))
        return id is not None

    def delete_team(self, teamName):
        teams = self.db["teams"]
        result = teams.remove({"name": {"$eq": teamName}})
        return result['ok'] == 1
