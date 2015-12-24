# Import flask dependencies
from flask import Blueprint, jsonify
import flask.ext.login
from flask.ext.login import login_required, current_user
from flask_security.forms import RegisterForm, Required
from mongoengine import StringField
from goalboost.model.auth_models import User
from goalboost.blueprints.auth.token_auth import httpBasicAuth


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('UserName', [Required()])

# -------------------- Flask Security - custom forms ------------------------------


# ----- Standard Blueprint stuff, logout redirects and samples --------------------
# Define the blueprint: 'auth', set its url prefix: app.url/auth
bp_auth = Blueprint('auth', __name__, url_prefix='/auth')



# This is just a hello world sort of resource for our API tests.
@bp_auth.route('/api/resource')
@httpBasicAuth.login_required
def get_resource():
    data = dict(hello = "world")
    return jsonify(data)


@bp_auth.route('/get_token')
@login_required
def get_auth_token():
    token = current_user.get_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


@bp_auth.route("/logged_out")
def logged_out():
    return flask.render_template("mod_auth/logged_out.html")


