from flask import Blueprint, jsonify, request
from goalboost.model.mongo_models import User
from goalboost.model.business_objects import UserTimer, TimerDao
from goalboost.model import db
from flask import Blueprint
from flask_restful import Api
from mongoengine.errors import ValidationError
from flask.ext.login import login_required, logout_user
from flask import current_app
from flask_security.core import current_user

#from json import dumps, loads

bp_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp_api)

def init_api(app):
    api.add_resource(People, '/people')
    api.add_resource(Person,  '/people/<string:id>')
    api.add_resource(UserCurrentTimerResource, '/user/<string:id>')
    api.add_resource(TimerResource, '/user/<string:userid>/timer')
    api.add_resource(TimerResourceById, '/timer/<string:timer_id>')
    api.add_resource(UserTimerResource, '/user/<string:id>/timer/current')
    api.add_resource(EnvironmentLogger, "/env", )
    app.register_blueprint(bp_api)


# Define the blueprint: 'auth', set its url prefix: app.url/auth
# mod_api = Blueprint('api', __name__, url_prefix='/api')

from flask_restful import Resource

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

class TimerResource(Resource):
    # TODO implementation is wrong
    def get(self, userid):
        try:
            l = TimerDao.timers_for_user(userid)
            return [timer.to_api_dict() for timer in l]
        except ValidationError as detail:
            return ErrorHandler.bad_request("Invalid ID format")


def post(self, userid):
        return dict(todo="Handle timer post in TimerResource.post")

class TimerResourceById(Resource):

    # /api/timer/:timerid
    # Gets a specific timer by id
    # Working.  Review.
    # Need to verify that the logged in user is this user, or member of same account?
#    @login_required
    def get(self, timer_id):
        try:
            timer = TimerDao.timer_by_id(timer_id)
            if timer:
                return timer.to_api_dict()
            else:
                return ErrorHandler.not_found()
        except ValidationError as detail:
            return ErrorHandler.bad_request("Invalid ID format")

    # Todo
    def put(self, timer_id):
        return dict(todo="Replace the timer identified by timer_id in TimerResourceById.put")


# Todo authorization, and check id is valid ObjectId
class UserCurrentTimerResource(Resource):
    def get(self, id):
        query_set = User.objects(id=id)
        try:
            u = query_set.first()
            return loads(u.public_json())
        except:
            return ErrorHandler.not_found()

# Todo authorization, and check id is valid ObjectId
class UserTimerResource(Resource):
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

# Throwaway test / demo stuff
class People(Resource):
    def get(self):
        return [{'name': 'Johnsin'}, {'name': 'Jenniffer'}]

    def post(self):
        return {'name': 'Johnsin Chiquilin'}, 201
class Person(Resource):
    def get(self, id):
        return {'name': 'Johnsin!'}
