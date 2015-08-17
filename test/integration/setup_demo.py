from test.common.test_helper import TestHelper
import requests
import json

class SetupDemo():
    ''' This "integration test" class will take us through everything involved in:
            * Creating a new team
            * Creating an admin for the team
            * Creating objects (instances of resources) owned by the team, such as
                * Users
                * Other people
                * etc...
    '''
    def __init__(self):
        self.testHelper = TestHelper()

        pass

    def _create_demo_team_with_database(self):
        ''' Todo create demo directly from db not from API if needed
        '''
        # db = self.testHelper.database()

    def _create_demo_team_with_api(self):
        demo_team = {'name': 'Demo'}
        teams_url = self.testHelper.api_root() + "teams"
        resp = requests.post(teams_url, demo_team)
        assert(resp.status_code == 201)

        # cs_team =  {'name': 'CodeSolid'}

        # If we re-create it it will fail because name is Unique and now it is a duplicate record
        resp = requests.post(teams_url, demo_team)
        assert(resp.status_code == 422)
        # print(resp.text) gives {"_issues": {"name": "value 'Demo' is not unique"}, "_status": "ERR", "_error": {"code": 422, "message": "Insertion failure: 1 document(s) contain(s) error(s)"}}

    def _delete_demo_team(self):
        ''' Find the team named "Demo" with a GET request, parse the request, and if the team is found,
            delete it.
        '''

        # Important, do not use this where condition directly with DELETE -- you need
        # to follow the steps below.
        # Using "where..." may delete ALL the teams (apparently where clause is ignored!).
        # But NOTE that that will only happen if you foolishly enable "DELETE" on resource_methods
        # like this WRONG WRONG WRONG way:
        #       'resource_methods': ['GET', 'POST', 'DELETE'],
        #
        # The right ways is:
        #       'resource_methods': ['GET', 'POST'],
        #       'item_methods': ['PUT', 'DELETE'],
        #
        # SO anyway, having said all that... find the Demo team using a GET
        # but wait I managed yet more mistakes, so yet more notes.
        teams_url = self.testHelper.api_root() + 'teams?where={"name" : "Demo"}'
        resp = requests.get(teams_url)

        if resp.status_code == 200:
            demo_team = json.loads(resp.text)
            # You can't just check 200 error code as we did above, because if the where condition
            # fails the query will still "succeed" but return empty list. Therefore you also need to
            # verify non-zero-length _items list, which the following idiom does concisely:
            if demo_team["_items"]:
                demo_team_item = demo_team["_items"][0]
                # An extra sanity check.  Sometimes if you code the query wrong you'll get
                # a list with "CodeSolid" as teh first answer.  Ways to do this may include
                # using single quotes in the where clause (mongo db portion), or missing the =
                # after where (which is dumb, but it shouldn't give you the whole list?)
                if demo_team_item["name"] == "Demo":
                    delete_url = self.testHelper.api_root() + demo_team_item["_links"]["self"]["href"]
                    # Remember you need the _etag for update and delete
                    etag = demo_team_item["_etag"]
                    resp = requests.delete(delete_url, headers= {"If-Match": etag})
                    assert(resp.status_code == 204)

    def run(self):
        self._delete_demo_team()
        self._create_demo_team_with_api()

if __name__ == "__main__":
    demo = SetupDemo()
    demo.run()

