'''from datetime import datetime
from eve.methods.common import document_etag
from eve.methods.put import put
from flask import current_app as app

# Todo To do a lot of this needs to be abstracted into it's own DB connection management class
# or better yet see about using Eve's
class RegistrationModel(object):
    ERROR_NONE = 0
    ERROR_DUPLICATE_TEAM = 101
    ERROR_DUPLICATE_EMAIL = 102
    ERROR_PASSWORD_MISMATCH = 110

    def __init__(self, db):
        self.db = db

    def get_db(self):
        if self.db:
            return self.db
        return app.data.driver.db

    def get_teams_collection(self):
        return self.get_db()["teams"]

    def get_document(self, teamName):
        return {'name': teamName}

    def team_exists(self, teamName):
        if teamName is None: return False
        teams = self.get_teams_collection()
        account = teams.find_one(self.get_document(teamName))
        return account is not  None

    def insert_team(self, teamName):
        if self.team_exists(teamName): return False
        teams = self.get_teams_collection()
        id = teams.save(self.get_document(teamName))
        return id is not None

    def insert_team_mongo(self, teamName):
        if self.team_exists(teamName): return False
        teams = self.get_teams_collection()
        doc = self.get_document(teamName)

        # TODO BUG -- Copying the implementation details out of Eve was likel the wrong thing
        # to do, at least without giving it some thought, keeping original references to eve config
        # for key names, setc.
        last_modified = datetime.utcnow().replace(microsecond=0)
        doc["_created"] = last_modified
        doc["_updated"] = last_modified
        doc["_etag"] = document_etag(doc)
        # TODO end bug

        id = teams.save(doc)

        return id is not None

    def delete_team(self, teamName):
        teams = self.get_teams_collection()
        result = teams.remove({"name": {"$eq": teamName}})
        return result['ok'] == 1

    def register_new_account(self, email, password, password2, team):
        if self.team_exists(team):
            return RegistrationModel.ERROR_DUPLICATE_TEAM
        elif password != password2:
            return RegistrationModel.ERROR_PASSWORD_MISMATCH
        return RegistrationModel.ERROR_NONE
'''


