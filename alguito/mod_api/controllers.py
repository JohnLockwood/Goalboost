# Import flask dependencies
from flask import Blueprint, redirect, render_template

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_api = Blueprint('api', __name__, url_prefix='/api')



from flask_restful import Resource

class People(Resource):
    def get(self):
        return [{'name': 'Johnsin'}, {'name': 'Jenniffer'}]

    def post(self):
        return {'name': 'Johnsin Chiquilin'}, 201
class Person(Resource):
    def get(self, id):
        return {'name': 'Johnsin!'}
