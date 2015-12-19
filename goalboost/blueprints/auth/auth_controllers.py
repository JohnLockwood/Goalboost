# Import flask dependencies
from flask import Blueprint, jsonify
import flask.ext.login
from flask.ext.login import login_required, logout_user, current_user
from flask.ext.httpauth import HTTPBasicAuth
from flask_security.forms import RegisterForm, Required
from mongoengine import StringField
from goalboost.model.auth_models import User


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('UserName', [Required()])

# -------------------- Flask Security - custom forms ------------------------------


# ----- Standard Blueprint stuff, logout redirects and samples --------------------
# Define the blueprint: 'auth', set its url prefix: app.url/auth
bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

auth = HTTPBasicAuth()

@bp_auth.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % current_user.email })

@auth.verify_password
def verify_password(username, password):
    global current_user
    user = User.verify_auth_token(password)
    # Todo review -- Is verifying user part of auth token sufficient?  Seems to me we should also be verifying the generated token?
    if not user:
        return False
    current_user = user
    return True



@bp_auth.route('/get_token')
@login_required
def get_auth_token():
    token = current_user.get_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


@bp_auth.route("/logged_out")
def logged_out():
    return flask.render_template("mod_auth/logged_out.html")

# Just a demo of using login required - TODO delete when not needed
@bp_auth.route("/protected/",methods=["GET"])
@login_required
def protected():
    return flask.render_template("mod_auth/protected.html")

