from flask import jsonify, request, Response
import http.client
from flask import abort
from goalboost.blueprints.api.restful_resource import RestfulResource
from goalboost.blueprints.auth.token_auth import httpBasicAuth
from goalboost.model.timer_models import TimerDAO, TimerFormatter, TimerEntity


class TimerResource(RestfulResource):

    @httpBasicAuth.login_required
    def get_one(self, id):
    #    def timer_get_one(timer_id):
        dao = TimerDAO()
        timer = dao.get(id)
        as_dict = TimerFormatter().model_to_dict(timer)
        resp = jsonify(as_dict)
        return resp

    def get_many(self):
        return RestfulResource.not_found()

    @httpBasicAuth.login_required
    def post(self):
        api_v1_root = '/api/v1'
        timer = TimerFormatter().dict_to_model(TimerEntity, request.json)
        dao = TimerDAO()
        dao.put(timer)
        id = str(timer.id)
        resp = jsonify(dict(id=id))
        resp.headers["Location"] = self.make_location(request.url, id)
        resp.status_code = http.client.CREATED
        return resp

    @httpBasicAuth.login_required
    def put(self, id):
        #api_v1_root = '/api/v1'
        timer_new = TimerFormatter().dict_to_model(TimerEntity, request.json)
        dao = TimerDAO()
        timer = dao.get(id)
        if timer is not None:
            timer.update_attributes(timer_new)
            dao.put(timer)
            id = str(timer.id)
            resp = jsonify(dict(id=id))
            #resp.headers["Location"] = api_v1_root + self.root + "/" + id
            resp.headers["Location"] = self.make_location(request.url, id)
            resp.status_code = http.client.OK
            return resp

    @httpBasicAuth.login_required
    def delete(self, id):
        api_v1_root = '/api/v1'
        dao = TimerDAO()
        count_deleted = dao.delete(id)
        if count_deleted == 1:
            return Response(status=204)
        else:
            return Response(status=404)

    def make_location(self, request_url, id):
        location = request_url
        if not location.endswith("/"):
            location = location + "/"
        return location + id