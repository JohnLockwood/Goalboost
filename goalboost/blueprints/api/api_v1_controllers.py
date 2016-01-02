import http.client

from flask import Blueprint, jsonify, request, Response

from goalboost.blueprints.api.restful_resource import RestfulResource
from goalboost.blueprints.api.timer_resource import TimerResource
from goalboost.blueprints.auth.token_auth import httpBasicAuth
from goalboost.model.timer_models import TimerFormatter, TimerEntity, TimerDAO
from .api_v1_controllers_test import routes as test_routes, ProofOfConcept

api_v1_root = '/api/v1'
v1_api = Blueprint('api/v1', __name__, url_prefix=api_v1_root)

# One operation?
poc = ProofOfConcept("/poc")
poc.register_routes(v1_api)

poc2 = RestfulResource("/poc2")
poc2.register_routes(v1_api)

timer_resource = TimerResource("/timer")
timer_resource.register_routes(v1_api)

# # Timer post
# @v1_api.route('/timer', methods=["POST"])
# @httpBasicAuth.login_required
# def timer_post():
#     timer = TimerFormatter().dict_to_model(TimerEntity, request.json)
#     dao = TimerDAO()
#     dao.put(timer)
#     id = str(timer.id)
#     resp = jsonify(dict(id=id))
#     resp.headers["Location"] = api_v1_root + "/timer/" + id
#     resp.status_code = http.client.CREATED
#     return resp
#
# @v1_api.route('/timer/<string:timer_id>', methods=["GET"])
# @httpBasicAuth.login_required
# def timer_get_one(timer_id):
#     dao = TimerDAO()
#     timer = dao.get(timer_id)
#     as_dict = TimerFormatter().model_to_dict(timer)
#     resp = jsonify(as_dict)
#     return resp
#
# @v1_api.route('/timer/<string:timer_id>', methods=["PUT"])
# @httpBasicAuth.login_required
# def timer_put(timer_id):
#     timer_new = TimerFormatter().dict_to_model(TimerEntity, request.json)
#     dao = TimerDAO()
#     timer = dao.get(timer_id)
#     if timer is not None:
#         timer.update_attributes(timer_new)
#         dao.put(timer)
#         id = str(timer.id)
#         resp = jsonify(dict(id=id))
#         resp.headers["Location"] = api_v1_root + "/timer/" + id
#         resp.status_code = http.client.OK
#         return resp
#
# @v1_api.route('/timer/<string:timer_id>', methods=["DELETE"])
# @httpBasicAuth.login_required
# def timer_delete(timer_id):
#     dao = TimerDAO()
#     count_deleted = dao.delete(timer_id)
#     if count_deleted == 1:
#         return Response(status=204)
#     else:
#         return Response(status=404)


for r in test_routes:
    print(r["rule"], r["view_func"])
    v1_api.add_url_rule(r["rule"], endpoint=r["rule"], view_func=r["view_func"])
