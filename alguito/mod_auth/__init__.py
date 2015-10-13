from flask import url_for
from flask.ext.login import LoginManager, login_required, logout_user
login_manager = LoginManager()
from .models import User, Role
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from alguito.datastore import db


def init_login_manager(app):

    #login_manager.init_app(app)
    #login_manager.login_view = "/auth/login"
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)


@login_manager.user_loader
def load_user_by_id(id):
    try:
        return User.get(id)
    except:
        return None
