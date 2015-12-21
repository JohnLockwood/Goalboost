# Import flask dependencies
from flask import Blueprint, jsonify
import flask.ext.login
from flask.ext.login import login_required, logout_user, current_user
from flask.ext.httpauth import HTTPBasicAuth
from flask_security.forms import RegisterForm, Required
from mongoengine import StringField
from goalboost.model.auth_models import User, UserSchema


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('UserName', [Required()])

# -------------------- Flask Security - custom forms ------------------------------


# ----- Standard Blueprint stuff, logout redirects and samples --------------------
# Define the blueprint: 'auth', set its url prefix: app.url/auth
bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

auth = HTTPBasicAuth()

# This is just a hello world sort of resource for our API tests.
@bp_auth.route('/api/resource')
@auth.login_required
def get_resource():
    # Flex our Marshmallow muscles a bit (that sounds bad):
    user_schema = UserSchema()
    data = user_schema.dump_exclude(current_user, exclude=["password", "account"]).data
    data2 = user_schema.dump_exclude(current_user, exclude=["password"]).data
    data["hello"] = "Hello %s" % current_user.email
    return jsonify(data)

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


