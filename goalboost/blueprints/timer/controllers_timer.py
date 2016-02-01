# Import flask dependencies
from flask import Blueprint, render_template, current_app
from flask.ext.login import login_required
from flask_security.core import current_user

# Define the blueprint: 'auth', set its url prefix: app.url/auth
from goalboost.model.auth_models import Account
from goalboost.model.timer_models import TimerDAO

bp_timer = Blueprint('timer', __name__, url_prefix='/timer')


@bp_timer.route('/user', methods=['GET'])
@login_required
def index():
    user = current_user
    return render_template("timer/user_timer.html", userId=user.id, userEmail=user.email, authToken=user.get_auth_token())
    #return render_template("index/index.html", userId=user.id)


# Give some thought to the routes we're going to use.
@bp_timer.route('/hours/goalboost', methods=['GET'])
def project_hours():
    timerDao = TimerDAO()
    account = Account.objects(name="Goalboost").first()
    users = [user.id for user in account.get_users()]
    timer_stats = timerDao.get_weekly_timer_statistics(users, ["Goalboost"])
    return render_template("timer/project_hours.html", stats = timer_stats)




