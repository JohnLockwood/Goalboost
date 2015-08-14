# Setup to run test
from sys import path
import sys
import os
import unittest

# These lines must be in this order
#sys.path.insert(0, os.path.abspath('..'))
#sys.path.insert(0, os.path.abspath("."))

# modules under test
import alguito.app

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.app = alguito.app.app.test_client()

    def test_root(self):
        rv = self.app.get("/")
        assert b"Alguito" in rv.data

    def test_can_find_george(self):
        rv = self.app.get('/api/people?where={"firstname": "George"}')
        assert b"Clooney" in rv.data

if __name__ == "__main__":
	unittest.main()

