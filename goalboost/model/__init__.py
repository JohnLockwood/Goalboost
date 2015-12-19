'''
goalboost.model package
The goalboost model package consists of MongoEngine models along with
Marshmallow schemas.  MongoEngine is our database ORM to MongoDB,
and Marshmallow is a serialization library that helps us validate, consume,
and expose these Orm objects for clients that need it at the API layer.

For MongoEngine, see http://mongoengine.org/

For Marshmallow and the MongoEngine integration piece, see:
https://marshmallow.readthedocs.org/en/latest/
https://github.com/touilleMan/marshmallow-mongoengine

'''

from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

def init_db(app):
    global db
    db.init_app(app)

