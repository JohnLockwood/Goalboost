from marshmallow_mongoengine import ModelSchema

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
