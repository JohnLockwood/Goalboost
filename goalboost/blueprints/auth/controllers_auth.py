# Import flask dependencies
from flask import Blueprint, jsonify
import flask.ext.login
from flask.ext.login import login_required, logout_user, current_user
from flask.ext.httpauth import HTTPBasicAuth
from flask_security.forms import RegisterForm, Required
from mongoengine import StringField
from goalboost.model.models_auth import User


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
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

@auth.verify_password
def verify_password(username, password):
    user = User.verify_auth_token(password)
    if not user or not user.verify_password(password):
        return False
    g.user = user
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


# ----------------------------- UNUSED Todo delete ---------------------------------
# # # Set the route and accepted methods
# @bp_auth.route('/login/', methods=['GET', 'POST'])
# def signin():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         #userEntity = User(id=form.email.data, password=form.password.data)
#         userEntity = User.get(id=form.email.data)
#
#         if(userEntity is not None and userEntity.verify_password(form.password.data)):
#             #user = User(form.email.data, form.password.data)
#             if(flask.ext.login.login_user(userEntity)):
#
#                 flask.flash('Logged in successfully.')
#                 next = flask.request.args.get('next')
#                 #next_is_valid should check if the user has valid
#                 # permission to access the `next` url
#                 #if not next_is_valid(next):
#                 #    return flask.abort(400)
#                 return flask.redirect(next or flask.url_for('index.index'))
#         else:
#             flask.flash("Login failed")
#
#     return flask.render_template('mod_auth/login.html',
#                                  title='Sign In',
#                                  form=form)
