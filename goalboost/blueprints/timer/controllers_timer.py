# Import flask dependencies
from flask import Blueprint, render_template, current_app
from flask.ext.login import login_required
from flask_security.core import current_user

# Define the blueprint: 'auth', set its url prefix: app.url/auth
bp_timer = Blueprint('timer', __name__, url_prefix='/timer')

# Set the route and accepted methods
@bp_timer.route('/user', methods=['GET'])
@login_required
def index():
    user = current_user
    return render_template("timer/user_timer.html", userId=user.id, userEmail=user.email, authToken=user.get_auth_token())
    #return render_template("index/index.html", userId=user.id)




