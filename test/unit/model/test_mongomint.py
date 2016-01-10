from unittest import TestCase

from goalboost.model.mongomint import MongoMintDocument
from test.common.test_helper import TestHelper
from goalboost.model import db
from pymongo import MongoClient

class TestMongoMintDocument(TestCase):

    def test_can_get_pymongo_client(self):
        assert(type(db.connection) == MongoClient)

    def test_can_create(self):
        doc = MongoMintDocument(db.connection, None)
        assert(doc is not None)

    def test_document_has_connection(self):
        doc = MongoMintDocument(db.connection, None)
        assert(type(doc.connection) == MongoClient)

    def test_can_do_bare_upsert(self):
        doc = MongoMintDocument(db.connection, None)
        connection = doc.connection
        model1 = dict(name="John")
        assert("_id" not in model1)
        collection = connection["goalboost"]["mint_test_bare_upsert"]
        collection.remove({})
        collection.insert_one(model1)
        assert("_id" in model1)
        model2 = collection.find_one()
        assert(model1["name"] == model2["name"])
        assert(model1["_id"] == model2["_id"])
        model1["name"] = "Jenniffer"
        collection.replace_one(filter = {"_id" : model1["_id"]}, replacement=model1)

        model3 = model2 = collection.find_one(model1)
        assert(model3["name"] == "Jenniffer")
        assert(model3["_id"] == model1["_id"])
        collection.drop()


    def test_can_do_object_upsert(self):
        doc = MongoMintDocument(db.connection, "mint_object_upsert")
        connection = doc.connection
        model1 = dict(name="John")
        assert("_id" not in model1)

        #
        # collection.insert_one(model1)
        # assert("_id" in model1)
        # model2 = collection.find_one()
        # assert(model1["name"] == model2["name"])
        # assert(model1["_id"] == model2["_id"])
        # model1["name"] = "Jenniffer"
        # collection.replace_one(filter = {"_id" : model1["_id"]}, replacement=model1)
        #
        # model3 = model2 = collection.find_one(model1)
        # assert(model3["name"] == "Jenniffer")
        # assert(model3["_id"] == model1["_id"])
        # collection.drop()


