# Import flask dependencies
from flask import Blueprint, jsonify
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
        query_set = User.objects(id=id)
        try:
            u = query_set.first()
            user_timer = UserTimer(u, db)
            timer = user_timer.timer_get()
            if timer is not None:
                return timer.to_json()
            else:
                return ErrorHandler.not_found()
        except:
            return ErrorHandler.not_found()
# Throwaway test / demo stuff
class People(Resource):
    def get(self):
        return [{'name': 'Johnsin'}, {'name': 'Jenniffer'}]

    def post(self):
        return {'name': 'Johnsin Chiquilin'}, 201
class Person(Resource):
    def get(self, id):
        return {'name': 'Johnsin!'}
