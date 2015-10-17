from flask.ext.login import LoginManager

login_manager = LoginManager()
from alguito.model.mongo_models import User, Role
from flask.ext.security import Security, SQLAlchemyUserDatastore, MongoEngineUserDatastore
from alguito.datastore import db


def init_flask_security_sqlalchemy(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    # Not sure we need this step, YAGNI?
    app.security = security


def init_flask_security(app):
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    # Not sure we need this step, YAGNI?
    app.security = security


@login_manager.user_loader
def load_user_by_id(id):
    try:
        return User.get(id)
    except:
        return None
