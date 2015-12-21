from bson import ObjectId
from marshmallow_mongoengine import ModelSchema
from goalboost.model import db

'''
For Marshmallow and the MongoEngine integration, see:
https://marshmallow.readthedocs.org/en/latest/
https://github.com/touilleMan/marshmallow-mongoengine
'''
class GoalboostModelSchema(ModelSchema):
    # Adds exclude param to ModelSchema, to allow filtering out certain fields
    # Usage exclude = ("password", "id"), for example
    def dump_exclude(self, obj, many=None, update_fields=True, exclude=None):
        dumped = self.dump(obj, many, update_fields)
        if exclude is not None:
            for key in exclude:
                del(dumped.data[key])
        return dumped

    # def dump(self, obj, many=None, update_fields=True, **kwargs):
    #     dumped = super(GoalboostModelSchema, self).dump(obj, many, update_fields)
    #     fixed = {key: value for key, value in dumped.data.items()}
    #     return fixed

class ModelFormatter(object):
    # Deprecated?
    def model_to_dict(self, object_as_model, include):

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

