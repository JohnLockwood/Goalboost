# mongo mint, because it's wafer thin, and hence, pythonic


class MongoMintDocument(object):

    # Initialize with a connection, which is a PyMongoClient instance
    def __init__(self, pymongo_client_object, collection, database="goalboost"):
        self.connection = pymongo_client_object
        self.database = database
        self.collection = collection
        self._clear_validation_errors()

    # TODO finish
    def upsert(self, model_dictionary):
        if self._is_valid(model_dictionary):
            if "_id" in model_dictionary:   # Update case
                return True
            else:
                return True
        else:
            return False

    # TODO
    def json_to_dictionary(self, json):
        pass

    def get_collection(self):
        return self.connection[self.database][self.collection]

    def _clear_validation_errors(self):
        self.errors = []

    def get_validation_errors(self):
        return self.errors

    def _is_valid(self, model_dictionary):
        self._clear_validation_errors()
        self.validate(model_dictionary)
        return len(self.errors) > 0

    # If you don't want data validation, don't implement
    # If you do implement, then add one string per validation failure to
    # self.errors
    def validate(self, model_dictionary):
        pass
