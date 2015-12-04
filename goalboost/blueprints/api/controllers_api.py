from flask import Blueprint, jsonify, request
from goalboost.model.mongo_models import User, Timer
from goalboost.model.business_objects import UserTimer
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

    # Current timer for user;
    api.add_resource(UserCurrentTimerResource, '/user/<string:id>/timer_current')

    # Timers generally
    api.add_resource(TimerResource, '/timer')

    api.add_resource(TimerResourceById, '/timer/<string:timer_id>')

    api.add_resource(EnvironmentLogger, "/env", )
    app.register_blueprint(bp_api)


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
class UserResource(Resource):
    def get(self, id):
        query_set = User.objects(id=id)
        try:
            u = query_set.first()
            return loads(u.public_json())
        except:
            return ErrorHandler.not_found()


# Todo authorization, and check id is valid ObjectId
class UserCurrentTimerResource(Resource):
    #@api.representation("application/json")
    def get(self, id):
        timer = self._get_timer(id)
        if timer is not None:
            timer.thisNeedsWork = "HEY-- THIS IS NOT WORKING YET.  JCL TODO FIX THIS"
            return timer.to_api_dict()  #loads(timer.to_json())
        else:
            return ErrorHandler.not_found()

    # JCL TODO !!!
    # Makes another timer the current timer.
    def put(self, id):
        return self.get(id)
        # query_set = User.objects(id=id)
        # try:
        #     u = query_set.first()
        #     user_timer = UserTimer(u, db)
        #     print(loads(user_timer.timer_get()))
        #     return loads(user_timer.timer_get())
        # except:
        #     return None

    # Based loosely on http://williamdurand.fr/2014/02/14/please-do-not-patch-like-an-idiot/,
    # but is probably still idiotic according to the purists.
    # Requi
    def patch(self, id):
        # Confirm json in body
        if request.json is None:
            return ErrorHandler.bad_request("Bad request - expected Content-Type is application/json")

        '''
        Valid ops:
            See http://williamdurand.fr/2014/02/14/please-do-not-patch-like-an-idiot and RFC:
            http://tools.ietf.org/html/rfc6902
        {"op":"replace", "path": "/running", "value": true} - Start or resume the timer
        {"op":"replace", "path": "/running", "value": false} - Stop (or "pause") the timer
        {"op":"replace", "path": "/notes", "value": "Some text value describing the notes."} - Set the notes
        '''
        # Try to get the timer
        timer = self._get_timer(id)
        if timer is not None:
            json = request.json
            # At this point everything needs a value, but that may change in future.
            if "op" not in json.keys() or "path" not in json.keys() or "value" not in json.keys():
                return ErrorHandler.bad_request("Bad request - see API documentation at ... ?")
            op = json["op"]
            path = json["path"]
            value = json["value"]

            if (op == "replace" and path == "/running"):
                if not isinstance(value, bool):
                    return ErrorHandler.bad_request("Bad request value for running must be boolean")
                # Start timer
                if(value == True):
                    if timer.running:
                        return ErrorHandler.bad_state_transition("Invalid state transition - timer alread running")
                    else:
                        timer.start()
                else:
                    timer.stop()

            return timer.public_json()
        else:
            return ErrorHandler.not_found()

    # Creates a new timer and sets it as user's timer
    # /api/user/:id/timer/current
    def post(self, id):
        return dict(todo="Replace the user timer with the new timer in UserTimerResource.post")

    def _get_timer(self, id):
        query_set = User.objects(id=id)
        try:
            u = query_set.first()
            user_timer = UserTimer(u, db)
            return user_timer.timer_get()
        except:
            return None

