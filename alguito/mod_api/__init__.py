from flask import Flask, Blueprint
from flask_restful import Api, Resource, url_for
from .controllers import People, Person, UserResource, UserTimerResource

def init_api(app):
    bp_api = Blueprint('api', __name__, url_prefix='/api')
    api = Api(bp_api)

    api.add_resource(People, '/people')
    api.add_resource(Person,  '/people/<string:id>')
    api.add_resource(UserResource, '/users/<string:id>')
    api.add_resource(UserTimerResource, '/users/<string:id>/timer')
    app.register_blueprint(bp_api)

