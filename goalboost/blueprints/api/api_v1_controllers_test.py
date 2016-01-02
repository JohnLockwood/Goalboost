from flask import jsonify, request

from goalboost.blueprints.auth.token_auth import httpBasicAuth


#@v1_api.route('/test')
def test():
    message = {"status": "Open for business"}
    return jsonify(message)

#@v1_api.route('/secure_test')
@httpBasicAuth.login_required
def secure_test():
    message = {"status": "Open for SECURE business only"}
    return jsonify(message)

routes = [
    dict(rule='/test', view_func=test),
    dict(rule='/test/secure_test', view_func=secure_test)
]


class ProofOfConcept(object):

    def __init__(self, root):
        if not root.startswith("/"):
            self.root = "/" + root
        else:
            self.root = root

    def one_item_router(self, id):
        method = request.method
        if (method == 'GET'):
            return self.get_one(id)
        elif(method == 'PUT'):
            return self.put(id)
        else:
            return self.delete(id)

    def many_item_router(self):
        method = request.method
        if (method == 'GET'):
            return self.get_many()
        elif(method == 'POST'):
            return self.post()

    def get_one(self, id):
        message = {"status": "Proof of concept - get one, open for business, id = " + id}
        return jsonify(message)

    def get_many(self):
        message = {"status": "Proof of concept - get many, open for business"}
        return jsonify(message)

    def post(self):
        return jsonify({"status": "Proof of concept POST"})

    def put(self, id):
        return jsonify({"status": "Proof of concept PUT, id = " + id })


    def delete(self, id):
        return jsonify({"status": "Proof of concept DELETE, id = " + id })

    def register_routes(self, blueprint):
        many_item_route = self.root
        one_item_route = self.root + "/<string:id>"

        routes = [
            dict(rule=one_item_route, endpoint= one_item_route, view_func=self.one_item_router, methods=["PUT", "GET", "DELETE"]),
            dict(rule=many_item_route, endpoint= many_item_route, view_func=self.many_item_router, methods=["GET", "POST"]),
        ]
        for r in routes:
            blueprint.add_url_rule(r["rule"], endpoint=r["endpoint"], view_func=r["view_func"], methods=r["methods"])


