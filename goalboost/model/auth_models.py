from json import loads, dumps
from flask import current_app
from flask.ext.security import RoleMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from mongoengine import signals
from goalboost.model import db
from goalboost.model.model_formatter import ModelFormatter

class Account(db.Document):
    name = db.StringField(max_length=255, unique=True)

# User and Role use flask security mixins and are used by flask security
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

# TODO Note if we are consistent here use ReferenceField for account
# TODO Also we need to add a UserName, which should be unique for itself + Account
class User(db.Document, UserMixin):
    email = db.EmailField(max_length=255, unique=True, required=True)
    password = db.StringField(max_length=255)
    account= db.ReferenceField(Account, required=False)       # Todo make this required
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    # TODO DEPRECATED  -- YANK!
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

    def __repr__(self):
        accountId = None
        confirmed_at = None
        if self.accountId is not None:
            accountId= self.accountId.__repr__()
        if self.confirmed_at is not None:
            confirmed_at = self.confirmed_at.__repr__()
        return ('User(id={}, emaitype(self.user)l="{}", password="{}", accountId={}, active={}, confirmed_at={}, roles={})'.format(
            self.id.__repr__(), self.email, self.password, accountId, confirmed_at, self.roles.__repr__(),
            None))

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

# ModelFormatter only defines an interface, and even there
# the Python idiom is unclear
class UserModelFormatter(ModelFormatter):
    def model_to_dict(self, object_as_model):
        if object_as_model is None:
            return None
        user_dict = dict()
        user_string_properties = ["id", "email", "confirmed_at"] # Password omitted - do not display
        for prop in user_string_properties:
            self.add_string_property(prop, object_as_model, user_dict)
        self.add_property("active", object_as_model, user_dict)

        # Make into AccountModelFormatter.model_to_dict
        user_dict["account"] = AccountModelFormatter().model_to_dict(object_as_model.account)

        return user_dict
        # Needs more testing:  roles = db.ListField(db.ReferenceField(Role), default=[])

    def dict_to_model(self, object_as_dict):
        raise NotImplementedError("UserModelFormatter::dict_to_model not implemented")

class AccountModelFormatter(ModelFormatter):
    def model_to_dict(self, object_as_model):
        if object_as_model is None:
            return None
        account_dict = dict()
        account_string_properties = ["id", "name"]
        for prop in account_string_properties:
            self.add_string_property(prop, object_as_model, account_dict)
        return account_dict

    def dict_to_model(self, object_as_dict):
        raise NotImplementedError("UserModelFormatter::dict_to_model not implemented")
