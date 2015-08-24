import unittest
from test.common.test_helper import TestHelper

import alguito.model.registration as registration

class TestRegistration(unittest.TestCase):

    def setUp(self):
        self.testHelper= TestHelper()

    def test_db_lazy_initialized(self):
        regModel = registration.RegistrationModel()
        self.assertEqual(regModel.db, None)

    def test_existing_team_returns_true_if_exists(self):
        regModel = registration.RegistrationModel()
        self.assertEqual(regModel.teamExists("CodeSolid"), True)


if __name__ == '__main__':
    unittest.main()
