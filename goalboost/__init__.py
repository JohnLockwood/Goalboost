from flask import Flask
from flask_mail import Mail

from config import config
from goalboost.blueprints import api
from goalboost.blueprints.auth import init_flask_security
from goalboost.blueprints.auth.controllers import bp_auth
from goalboost.blueprints.index.controllers import bp_index
from goalboost.blueprints.timer.controllers import bp_timer
from goalboost.blueprints.api import init_api

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
    init_api(app)

    config[config_name].init_app(app)
    #
    init_flask_security(app)

    mail = Mail(app)

    return app

create_app("production")
