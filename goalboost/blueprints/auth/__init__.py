from flask.ext.login import LoginManager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from goalboost.model.auth_models import Role, User
from flask.ext.security import Security, MongoEngineUserDatastore
from goalboost.model import db

login_manager = LoginManager()

def init_flask_security(app):
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    # This step may not be necessary
    app.security = security

@login_manager.user_loader
def load_user_by_id(id):
    try:
        return User.get(id)
    except:
        return None

# Work in progress, cf.
# http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
# http://thecircuitnerd.com/flask-login-tokens/
# See also mongo_models.User.get_auth_token
# TODO Duplicate code of user.verify_auth_token.  Consolidate!
@login_manager.token_loader
def verify_auth_token(token):
     s = Serializer(app.config['SECRET_KEY'])
     try:
         data = s.loads(token)
     except SignatureExpired:
         return None # valid token, but expired
     except BadSignature:
         return None # invalid token
     user = User.objects(id=data['id']).first() #.query.get(data['id'])
     return user
