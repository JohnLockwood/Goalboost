from flask import jsonify, request
import http.client
from flask import abort

class RestfulResource(object):

    def __init__(self, root):
        if not root.startswith("/"):
            self.root = "/" + root
        else:
            self.root = root

    def _one_item_router(self, id):
        method = request.method
        if (method == 'GET'):
            return self.get_one(id)
        elif(method == 'PUT'):
            return self.put(id)
        else:
            return self.delete(id)

    @classmethod
    def not_found(cls):
        # raise NotImplementedError()
        abort(http.client.NOT_FOUND)

    def _many_item_router(self):
        method = request.method
        if (method == 'GET'):
            return self.get_many()
        elif(method == 'POST'):
            return self.post()

    def get_one(self, id):
        return RestfulResource.not_found()

    def get_many(self):
        return RestfulResource.not_found()

    def post(self):
        return RestfulResource.not_found()

    def put(self, id):
        return RestfulResource.not_found()

    def delete(self, id):
        return RestfulResource.not_found()

    def register_routes(self, blueprint):
        many_item_route = self.root
        one_item_route = self.root + "/<string:id>"

        routes = [
            dict(rule=one_item_route, endpoint= one_item_route, view_func=self._one_item_router, methods=["PUT", "GET", "DELETE"]),
            dict(rule=many_item_route, endpoint= many_item_route, view_func=self._many_item_router, methods=["GET", "POST"]),
        ]
        for r in routes:
            blueprint.add_url_rule(r["rule"], endpoint=r["endpoint"], view_func=r["view_func"], methods=r["methods"])

