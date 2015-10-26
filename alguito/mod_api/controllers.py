# Import flask dependencies
#from json import loads, dumps
from flask import Blueprint, jsonify, request
from alguito.model.mongo_models import User, Timer
from alguito.model.business_objects import UserTimer
from alguito.datastore import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_api = Blueprint('api', __name__, url_prefix='/api')

from flask_restful import Resource

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


# Todo authorization, and check id is valid ObjectId
class UserResource(Resource):
    def get(self, id):
        query_set = User.objects(id=id)
        try:
            u = query_set.first()
            return u.public_json()
        except:
            return ErrorHandler.not_found()

# Todo authorization, and check id is valid ObjectId
class UserTimerResource(Resource):
    def get(self, id):
        timer = self._get_timer(id)
        if timer is not None:
            return timer.to_json()
        else:
            return ErrorHandler.not_found()

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
