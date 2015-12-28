from json import dumps, loads

from bson import ObjectId
from goalboost.model import db

class ModelFormatter(object):
    # A default base class implementation.
    def model_to_dict(self, object_as_model, include=None, exclude=None):
        as_dict = loads(object_as_model.to_json())
        if exclude is not None:
            subset = {key: value for key, value in as_dict.items() if key not in include}
            return subset
        elif include is not None:
            subset = {key: value for key, value in as_dict.items() if key in include}
            return subset
        else:
            return as_dict

    def dict_to_model(self, class_name, object_as_dict):
        return class_name.from_json(dumps(object_as_dict))

    # Adds a key / value pair to model_dict.  If the property on model_object
    # identified by the key is None, add None as value, otherwise stringify
    # the value
    def add_string_property(self, key, model_object, model_dict):
        val = getattr(model_object, key)
        if val is None:
            model_dict[key] = None
        else:
            model_dict[key] = str(val)

    # Add a value that's not a string and that shouldn't be converted to
    # one.  E.g., boolean, number etc.
    def add_property(self, key, model_object, model_dict):
        model_dict[key] = getattr(model_object, key)

    # For List fields
    def add_list_property(self, key, object_as_model, as_dict):
        value = getattr(object_as_model, key)
        if value is None:
            as_dict[key] = None
        else:
            as_dict[key] = [item for item in value]       # Convert to python list

