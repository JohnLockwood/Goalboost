from bson import ObjectId
from goalboost.model import db

class ModelFormatter(object):
    # Deprecated?
    def model_to_dict(selfg, object_as_model, include):
        #
        d = dict()
        for key in include:
            value = getattr(object_as_model, key)
            if isinstance(value, ObjectId):
                value = str(value)
            if isinstance(value, db.Document):
                print("Found a doc reference ", key)
            d[key] = value
        return d

    # Adds a key / value pair to model_dict.  If the property on model_object
    # identified by the key is None, add None as value, otherwise stringify
    # the value
    def add_string_property(self, key, model_object, model_dict):
        val = getattr(model_object, key)
        if val is None:
            model_dict[key] = None
        else:
            model_dict[key] = str(val)

    def add_property(self, key, model_object, model_dict):
        model_dict[key] = getattr(model_object, key)

    def dict_to_model(self, object_as_dict):
        pass

