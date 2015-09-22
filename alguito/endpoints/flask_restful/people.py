from flask_restful import Resource

class People(Resource):
    def get(self):
        return [{'name': 'Johnsin'}, {'name': 'Jenniffer'}]

    def post(self):
        return {'name': 'Johnsin Chiquilin'}, 201
class Person(Resource):
    def get(self, id):
        return {'name': 'Johnsin!'}
