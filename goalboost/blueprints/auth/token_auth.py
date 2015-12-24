from flask.ext.httpauth import HTTPBasicAuth

from goalboost.model.auth_models import User
from flask.ext.login import current_user, login_user

httpBasicAuth = HTTPBasicAuth()


@httpBasicAuth.verify_password
def verify_password(username, password):
    global current_user
    user = User.verify_auth_token(password)
    if not user:
        return False

    # Adding these lines will (correctly -- was tested at one point) mean "current_user" can be used from
    # contexts that need it, but leaving them off for now as  it is not a good design for a restful API,
    # which verify_password is designed to support
    #
    # user.authenticated = True
    # login_user(user, remember=True)

    return True

