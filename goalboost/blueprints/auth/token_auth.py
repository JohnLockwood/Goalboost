from flask.ext.httpauth import HTTPBasicAuth

from goalboost.model.auth_models import User
from flask.ext.login import current_user, login_user

httpBasicAuth = HTTPBasicAuth()


@httpBasicAuth.verify_password
def verify_password(username, password):
    global current_user
    user = User.verify_auth_token(password)
    # Todo review -- Is verifying user part of auth token sufficient?  Seems to me we should also be verifying the generated token?
    if not user:
        return False

    # Todo - These lines allow test_login_and_use_resource to work since it looks up the current user,
    # but one could make the case that a restful API shouldn't do this since it effectively creates session state.
    user.authenticated = True
    login_user(user, remember=True)

    return True

