import unittest
from test.common.test_helper import TestHelper

class TestEveSettings(unittest.TestCase):
    def setUp(self):
        self.testHelper = TestHelper()

    def test_domain_includes_people(self):
        assert("people" in self.testHelper.eve_settings()["DOMAIN"])

if __name__ == "__main__":
	unittest.main()

