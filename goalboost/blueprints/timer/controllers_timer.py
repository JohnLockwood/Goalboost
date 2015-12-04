# Import flask dependencies
from flask import Blueprint, render_template, current_app
from flask.ext.login import login_required
from flask_security.core import current_user
from goalboost.model.business_objects import UserTimer
from goalboost.model import db


# Define the blueprint: 'auth', set its url prefix: app.url/auth
bp_timer = Blueprint('timer', __name__, url_prefix='/timer')

# Set the route and accepted methods
@bp_timer.route('/user', methods=['GET'])
@login_required
def index():
    user = current_user
    user_timer = UserTimer(user, db)
    #return render_template("timer/user_timer.html", user=user, user_timer=user_timer)
    return render_template("index/index.html", userId=user.id)



