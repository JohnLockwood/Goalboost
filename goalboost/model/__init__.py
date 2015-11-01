from flask.ext.mongoengine import MongoEngine
# from flask.ext.sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
db = MongoEngine()

def init_db(app):
    global db
    db.init_app(app)




