from flask import Blueprint, jsonify, request
from flask.ext.login import login_required
from goalboost.model.auth_models import User
from goalboost.model.timer_models import Timer
from goalboost.model.datastore import TimerDao
from goalboost.model import db
from flask import Blueprint
from flask_restful import Api
from mongoengine.errors import ValidationError
from flask_restful import Resource
from json import loads, dumps

api_root = "/api"
bp_api = Blueprint('api', __name__, url_prefix=api_root)
api = Api(bp_api)

def init_api(app):
    # Just the User
    api.add_resource(UserResource, '/user/<string:id>')

    # All timers for a user
    api.add_resource(UserAllTimersResource, '/user/<string:userid>/timers')

    # Timers generally
    api.add_resource(TimerResource, '/timer')

    api.add_resource(TimerResourceById, '/timer/<string:timer_id>')

    api.add_resource(EnvironmentLogger, "/env", )
    app.register_blueprint(bp_api)


@bp_api.route("/protected_hello")
@login_required
def protected_hello():
    response = jsonify({'greeting': 'hello', 'recipient': 'world'})
    response.status_code = 200
    return response


# Define the blueprint: 'auth', set its url prefix: app.url/auth
# mod_api = Blueprint('api', __name__, url_prefix='/api')


class EnvironmentLogger(Resource):
    def get(self):
        #return os.getenv('GOALBOOST_MAIL_SERVER')
        return "Check the logs"

class ErrorHandler(Resource):
    @classmethod
    def not_found(cls):
        response = jsonify({'code': 404,'message': 'Not found'})
        response.status_code = 404
        return response

    @classmethod
    def bad_request(cls, msg):
        response = jsonify({'code': 400,'message': msg})
        response.status_code = 400
        return response

    @classmethod
    def bad_state_transition(cls, msg):
        response = jsonify({'code': 409,'message': msg})
        response.status_code = 409
        return response

class UserAllTimersResource(Resource):
    # /api/user/:id/timers
    # Gets all timers for a user. Most recent first. Need to work out pagination
    def get(self, userid):
        try:
            l = TimerDao().timers_for_user(userid)
            return [timer.to_api_dict() for timer in l]
        except ValidationError as detail:
            return ErrorHandler.bad_request("Invalid ID format")

class TimerResource(Resource):
    # /api/user/:userid/timer
    def post(self):
        json = request.json
        timer = Timer.load_from_dict(json)
        timer.save()
        location = api_root + "/timer/" + str(timer.id)
        response = jsonify(timer.to_api_dict())
        response.headers["location"] = location
        response.status_code = 201
        return response

class TimerResourceById(Resource):

    # /api/timer/:timerid
    # Gets a specific timer by id
    # Working.  Review.
    # Need to verify that the logged in user is this user, or member of same account?
    # @login_required
    def get(self, timer_id):
        try:
            timer = TimerDao().timer_by_id(timer_id)
            if timer:
                return timer.to_api_dict()
            else:
                return ErrorHandler.not_found()
        except ValidationError as detail:
            return ErrorHandler.bad_request("Invalid ID format")

    def put(self, timer_id):
        # To do review exceptions, also, does json ID match timer_id?
        # If not return bad request
        timer = Timer.load_from_dict(request.json)
        TimerDao().save_timer(timer)
        return(None, 204)

    def delete(self, timer_id):
        TimerDao().delete_timer(timer_id)
        return(None, 204)

# Todo authorization, and check id is valid ObjectId
# Todo design JCL Here we are loading JSON and then returning a dict.  Better
# if the formatting object or interface were always to_dict, from_dict.
class UserResource(Resource):
    def get(self, id):
        query_set = User.objects(id=id)
        try:
            u = query_set.first()
            return loads(u.public_json())
        except:
            return ErrorHandler.not_found()


