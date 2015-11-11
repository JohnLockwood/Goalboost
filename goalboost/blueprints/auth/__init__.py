from flask.ext.login import LoginManager

login_manager = LoginManager()
from goalboost.model.mongo_models import User, Role
from flask.ext.security import Security, SQLAlchemyUserDatastore, MongoEngineUserDatastore
from goalboost.model import db


# def init_flask_security_sqlalchemy(app):
#     user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#     security = Security(app, user_datastore)
#     # Not sure we need this step, YAGNI?
#     app.security = security


def init_flask_security(app):
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    # Not sure we need this step, YAGNI?
    app.security = security

@login_manager.user_loader
def load_user_by_id(id):
    try:
        return User.get(id)
    except:
        return None

# Work in progress, cf.
# http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
# See also mongo_models.User.get_auth_token
# @login_manager.token_loader
# def verify_auth_token(token):
#     s = Serializer(app.config['SECRET_KEY'])
#     try:
#         data = s.loads(token)
#     except SignatureExpired:
#         return None # valid token, but expired
#     except BadSignature:
#         return None # invalid token
#     user = User.objects(id=query.get(data['id'])).first() #.query.get(data['id'])
#     return user
