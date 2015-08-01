# Setup to run test
from sys import path
import sys
import os
import unittest
# These lines must be in this order
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath("."))


# modules under test
import goalboost.endpoints.eve.settings as settings


class TestStringMethods(unittest.TestCase):

    def test_domain_includes_people(self):
        assert("people" in settings.DOMAIN)

    def test_foo(self):
        assert(True)
# Allow import of api and api.whatever etc. from root folder, in such 
# a way that the test can be run from the test folder or the root folder.
# Based on answers given here:
# http://stackoverflow.com/questions/6323860/sibling-package-imports

if __name__ == "__main__":
	unittest.main()

