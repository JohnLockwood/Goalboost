
# Setup to run test
from sys import path
import sys
import os
import unittest
# Allow import of api and api.whatever etc. from root folder, in such
# a way that the test can be run from the test folder or the root folder.
# Based on answers given here:
# http://stackoverflow.com/questions/6323860/sibling-package-imports
# IMPORTANT These lines must be in this order
#sys.path.insert(0, os.path.abspath('..'))
#sys.path.insert(0, os.path.abspath("."))

# modules under test
import alguito.app as app

class TestStringMethods(unittest.TestCase):

    def test_domain_includes_people(self):
        assert("people" in app.eve_settings["DOMAIN"])


if __name__ == "__main__":
	unittest.main()

