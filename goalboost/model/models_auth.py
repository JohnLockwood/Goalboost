from json import loads, dumps

from flask import current_app
from flask.ext.security import RoleMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from mongoengine import signals
from goalboost.model import db

# User and Role use flask security mixins and are used by flask security
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.EmailField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    accountId = db.ObjectIdField(null=True)                 # Todo make this required
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    timer = db.ObjectIdField(null=True)

    # http://docs.mongoengine.org/guide/signals.html
    def handle_pre_save(sender, document):
        pass
        # print("Inside pre_save handler")

    signals.pre_save.connect(handle_pre_save)

    # Work in progress, cf.
    # http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
    # See also blueprints.auth.__init__py verify_auth_token comments
    def get_auth_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': str(self.id) })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.objects(id=data['id']).first() #.query.get(data['id'])
        return user

    def public_json(self):
        json = self.to_json()
        as_dict = loads(json)
        del(as_dict["password"])
        return dumps(as_dict)


class Account(db.Document):
    name = db.StringField(max_length=255, unique=True)