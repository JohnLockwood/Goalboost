from flask import Blueprint, jsonify
from goalboost.blueprints.api.timer_resource import TimerResource
from goalboost.blueprints.auth.token_auth import httpBasicAuth

v1_api = Blueprint('api/v1', __name__, url_prefix='/api/v1')

# Production resources are derived from RestfulResource.  Adding to this list will wire them up
v1_api_resources = [TimerResource("/timer")]
for resource in v1_api_resources:
    resource.register_routes(v1_api)


@v1_api.route('/test')
def test():
    message = {"status": "Open for business"}
    return jsonify(message)

@v1_api.route('/secure_test')
@httpBasicAuth.login_required
def secure_test():
    message = {"status": "Open for SECURE business only"}
    return jsonify(message)
