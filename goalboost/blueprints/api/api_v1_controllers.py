from flask import Blueprint, jsonify, request
from goalboost.blueprints.auth.token_auth import httpBasicAuth
from goalboost.model.timer_models import TimerFormatter, TimerEntity, TimerDAO

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

# LegacyTimer
@v1_api.route('/timer', methods=["POST"])
@httpBasicAuth.login_required
def timer_post():
    timer_entity = TimerFormatter().dict_to_model(TimerEntity, request.json)
    dao = TimerDAO()
    dao.put(timer_entity)

    resp = jsonify(dict(id=str(timer_entity.id)))
    resp.status_code = 201
    return resp