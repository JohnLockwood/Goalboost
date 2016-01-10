"""
MongoMintDocument is a wafer thin wrapper around a PyMongo collection
"""
from bson import ObjectId

class MongoMintDocument(object):

    """Create a MongoMintDocument object.

    pymongo_client_object - a MongoClient instance
    collection_name - a name for the collection we want to validate on / operate against
    database (optional, default="goalboost"), a name for the database where the collection will live
    """
    def __init__(self, pymongo_client_object, collection_name, database="goalboost"):
        self.connection = pymongo_client_object
        self.database = database
        self.collection_name = collection_name
        self._clear_validation_errors()

    """upsert - easy single document save.

    If validate generates no error, then insert a new document or update
    the existing one, returning true.

    If validate did return an error, return false.  In that case. self.errors can
    be inspected to find what happened.
    """
    def upsert(self, model_dictionary):
        if self._is_valid(model_dictionary):
            if "_id" in model_dictionary:               # Update case
                self.collection.replace_one( \
                    filter = {"_id" : model_dictionary["_id"]}, replacement=model_dictionary)
            else:                                       # Insert case
                self.collection.insert_one(model_dictionary)
            return True
        else:
            return False

    """find_by_id - Return a single document by id or None, accepting either string or ObjectId as argument"""
    # Always create an ObjectId, correctly handles both string case and ObjectId case
    def find_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id) })

    """collection (property)

    Easily use the underlying collection to use native pymongo methods, e.g. drop, find_one, etc.
    """
    @property
    def collection(self):
        return self.connection[self.database][self.collection_name]


    """validate (optional override allows you to provide pre-save data validation

    To implement if needed, add one string per validation failure to self.errors.

    """
    def validate(self, model_dictionary):
        pass


    # Private methods
    def _clear_validation_errors(self):
        self.errors = []

    def _is_valid(self, model_dictionary):
        self._clear_validation_errors()
        self.validate(model_dictionary)
        return len(self.errors) == 0

