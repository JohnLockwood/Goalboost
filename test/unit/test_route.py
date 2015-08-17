import unittest
from test.common.test_helper import TestHelper

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.testHelper = TestHelper()
        self.client = self.testHelper.test_client()

    def test_root(self):
        rv = self.client.get("/")
        assert b"Alguito" in rv.data

    def test_can_find_george(self):
        rv = self.client.get('/api/people?where={"firstname": "George"}')
        assert b"Clooney" in rv.data

if __name__ == "__main__":
	unittest.main()

