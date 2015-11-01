# Import flask dependencies
from flask import Blueprint, redirect
import flask.ext.login
from flask.ext.login import login_required, logout_user

from goalboost.model.mongo_models import User
from goalboost.mod_auth.forms import LoginForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        #userEntity = User(id=form.email.data, password=form.password.data)
        userEntity = User.get(id=form.email.data)

        if(userEntity is not None and userEntity.verify_password(form.password.data)):
            #user = User(form.email.data, form.password.data)
            if(flask.ext.login.login_user(userEntity)):

                flask.flash('Logged in successfully.')
                next = flask.request.args.get('next')
                #next_is_valid should check if the user has valid
                # permission to access the `next` url
                #if not next_is_valid(next):
                #    return flask.abort(400)
                return flask.redirect(next or flask.url_for('index.index'))
        else:
            flask.flash("Login failed")

    return flask.render_template('mod_auth/login.html',
                                 title='Sign In',
                                 form=form)

@mod_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@mod_auth.route("/protected/",methods=["GET"])
@login_required
def protected():
    return flask.render_template("mod_auth/protected.html")



