'''
Some helpful queries:
db.teams.find({"_etag": {"$exists": false}})
db.teams.find({"name": {"$eq": "NPYEejtoudpdyHGiDOiT"}}) # or some other name
'''

import unittest
from test.common.test_helper import TestHelper

import alguito.model.registration as registration

class TestRegistration(unittest.TestCase):

    def setUp(self):
        self.testHelper= TestHelper()
        self.regModel = registration.RegistrationModel(self.testHelper.database())

    def test_existing_team_returns_true_if_exists(self):
        self.assertEqual(self.regModel.team_exists("CodeSolid"), True)

    def test_existing_team_returns_false_if_team_does_not_exist(self):
        # Well, let's hope and pray it doesn't exist
        self.assertEqual(self.regModel.team_exists("Chupacabra2019MyBrother"), False)

    def test_existing_team_returns_false_for_None(self):
        # Well, let's hope and pray it doesn't exist
        self.assertEqual(self.regModel.team_exists(None), False)

    def test_can_insert_and_delete_a_record(self):
        random_string = self.testHelper.random_string(20)
        # self.assertEqual(len(random_string), 20)
        success = self.regModel.insert_team(random_string)
        self.assertEqual(success, True)
        success = self.regModel.delete_team(random_string)
        self.assertEqual(success, True)

    def test_can_insert_and_delete_a_with_mongo_io(self):
        random_string = self.testHelper.random_string(20)
        # self.assertEqual(len(random_string), 20)
        success = self.regModel.insert_team_mongo(random_string)
        self.assertEqual(success, True)
        success = self.regModel.delete_team(random_string)
        self.assertEqual(success, True)


if __name__ == '__main__':
    unittest.main()
