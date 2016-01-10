from unittest import TestCase

from bson import ObjectId

from goalboost.model.mongomint import MongoMintDocument
from test.common.test_helper import TestHelper
from goalboost.model import db
from pymongo import MongoClient

class SampleDocumentClass(MongoMintDocument):
    def validate(self, model_dictionary):
        if ("valid" not in model_dictionary):
            self.errors.append("Valid is a required field")
        elif "invalid" in model_dictionary:
            self.errors.append("Who stuck this invalid field on here?")


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
        model1 = dict(name="John")
        assert("_id" not in model1)
        doc.upsert(model1)
        assert("_id" in model1)

        model1["name"] = "Jenniffer"

        doc.upsert(model1)

        # JCL todo wrap in method
        model2 = doc.collection.find_one({"_id" : model1["_id"]})
        assert(model2["_id"] == model1["_id"])
        assert(model2["name"] == "Jenniffer")

        doc.collection.drop()

    def test_can_find_by_id(self):
        doc = MongoMintDocument(db.connection, "mint_object_upsert")
        genius = "Spencer Reid"
        model1 = dict(name=genius)
        doc.upsert(model1)
        id = model1["_id"]
        assert(type(id) == ObjectId)

        # Triial case, already right type:
        model2 = doc.find_by_id(id)
        assert(model2["name"] == genius)

        # Validate can load by string
        # Convert to string first
        model3 = doc.find_by_id(str(id))
        assert(model3["name"] == genius)
        doc.collection.drop()

    def test_validation(self):
        doc = SampleDocumentClass(db.connection, "mint_object_validation")

        model1 = dict(valid="Yes, this will be valid because key there")
        assert(True == doc.upsert(model1))
        assert(len(doc.errors) == 0)


        model1 = dict(valid="This would have been valid based on this", invalid="But this makes it invalid")
        assert(False == doc.upsert(model1))
        assert(len(doc.errors) == 1)

        # This doesn't contain the valid tag, so invalid
        model2 = dict(fish="Wanda")
        assert(False == doc.upsert(model2))
        assert(len(doc.errors) == 1)
        assert("required" in doc.errors[0])



        doc.collection.drop()




