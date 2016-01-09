from unittest import TestCase

from goalboost.model.mongomint import MongoMintDocument

class TestMongoMintDocument(TestCase):
    def test_can_create(self):
        doc = MongoMintDocument()
        assert(doc is not None)
