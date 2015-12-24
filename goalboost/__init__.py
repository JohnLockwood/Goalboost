from flask import Flask
from flask_mail import Mail
import os

from config import config
from goalboost.blueprints import api
from goalboost.blueprints.auth import init_flask_security
from goalboost.blueprints.auth.auth_controllers import bp_auth
from goalboost.blueprints.index.index_controllers import bp_index
from goalboost.blueprints.timer.controllers_timer import bp_timer
from goalboost.blueprints.api.api_controllers import init_api
from goalboost.blueprints.api.api_v1_controllers import v1_api

from goalboost.model import init_db, db

app = Flask(__name__)

def create_app(config_name):
    global app
    app.config.from_object(config[config_name])

    # Setup database
    # Currently inits mongoDB
    init_db(app)

    # Todo make intializing blueprints consistent
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_timer)
    app.register_blueprint(v1_api)
    init_api(app)

    config[config_name].init_app(app)
    #
    init_flask_security(app)

    mail = Mail(app)

    return app

create_app(os.environ.get("GOALBOOST_CONFIGURATION") or "development")

