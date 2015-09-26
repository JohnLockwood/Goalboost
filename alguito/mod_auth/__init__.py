from flask import url_for
from flask.ext.login import LoginManager, login_required, logout_user
login_manager = LoginManager()
from .models import User

def init_login_manager(app):

    login_manager.init_app(app)
    login_manager.login_view = "/auth/login"

@login_manager.user_loader
def load_user_by_id(id):
    try:
        return User.get(id)
    except:
        return None
