from flask import Flask, render_template

from config import config
from .mod_auth import init_login_manager
from .mod_auth.controllers import mod_auth
from .mod_api import init_api
from .mod_index.controllers import mod_index
from .datastore import init_db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(mod_index)
    app.register_blueprint(mod_auth)
    init_api(app)

    config[config_name].init_app(app)

    init_db(app)

    init_login_manager(app)

    #app.add_url_rule('/', 'index', index.index)
    #app.add_url_rule('/home/<page>', '/home', index.home)

    # attach routes and custom error pages here

    return app