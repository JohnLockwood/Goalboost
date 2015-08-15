# Setup to run test
from sys import path
import sys
import os
import unittest

# modules under test
import alguito.app as app

class TestStringMethods(unittest.TestCase):

    def test_domain_includes_people(self):
        assert("people" in app.eve_settings["DOMAIN"])


if __name__ == "__main__":
	unittest.main()

