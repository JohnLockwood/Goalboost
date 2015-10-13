from flask import Flask, render_template

from config import config
from .mod_auth import init_login_manager
from .mod_auth.controllers import mod_auth
from .mod_api import init_api
from .mod_index.controllers import mod_index
from .datastore import init_db, db
from flask_mail import Mail

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(mod_index)
    app.register_blueprint(mod_auth)
    init_api(app)

    config[config_name].init_app(app)

    init_db(app)

    # Creates a security object we do nothing with;
    # do we need it?
    init_login_manager(app)

    mail = Mail(app)

    return app