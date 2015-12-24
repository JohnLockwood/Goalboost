from flask import Blueprint, jsonify
from goalboost.blueprints.auth.token_auth import httpBasicAuth

api_v1_root = '/api/v1'
v1_api = Blueprint('api/v1', __name__, url_prefix=api_v1_root)

@v1_api.route('/test')
def test():
    message = {"status": "Open for business"}
    return jsonify(message)

@v1_api.route('/secure_test')
@httpBasicAuth.login_required
def test_secure():
    message = {"status": "Open for SECURE business only"}
    return jsonify(message)
