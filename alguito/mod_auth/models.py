from flask import current_app
#from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from alguito.datastore import db
from alguito.model.entities.base import Base
from flask.ext.security import UserMixin, RoleMixin
from passlib.hash import pbkdf2_sha256

'''
from passlib.hash import pbkdf2_sha256

from alguito.datastore import db
from alguito.model.entities.base import Base

class UserEntity(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    email = Column(String(120), unique=True)
    fullname = Column(String(120))
    _password = Column(String(120), name="password")


    @hybrid_property
    def password(self):
        return ""

    @password.setter
    def password(self, password):
        hash_rounds = current_app.config["USER_PASSWORD_HASH_ROUNDS"]
        hash = pbkdf2_sha256.encrypt(password, rounds=hash_rounds, salt_size=16)
        self._password = hash

    @hybrid_method
    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self._password)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)


class User(UserMixin):

    def __init__(self, username, password):
        self.id = username
        self.password = password


    #@property
    def is_active(self):
        return True

    #@property
    def is_authenticated(self):
        if (self.password is not None):
            u = UserEntity(email=self.id, password = self.password)
            return u.verify_password(self.password)
        else:
            return True

    #@property
    def is_anonymous(self):
        return False

    @classmethod
    def get(cls,id):
        userEntity = db.session.query(UserEntity).filter(UserEntity.email == id).one()
        if (userEntity):
            return User(userEntity.email, None)
        else:
            return None

    @classmethod
    def getEntity(cls, id):
        try:
            return db.session.query(UserEntity).filter(UserEntity.email == id).one()
        except:
            return None

    def get_id(self):
        return self.id

'''

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # _password = Column(String(120), name="password")
'''
    @hybrid_method
    def verify_password(self, password):
        return True
        #return pbkdf2_sha256.verify(password, self._password)

    @hybrid_property
    def password(self):
        return ""

    @password.setter
    def password(self, password):
        hash_rounds = current_app.config["USER_PASSWORD_HASH_ROUNDS"]
        hash = pbkdf2_sha256.encrypt(password, rounds=hash_rounds, salt_size=16)
        self._password = hash

    @classmethod
    def get(cls,id):
        user = db.session.query(User).filter(User.email == id).one()
        if (user):
            return user
        else:
            return None
'''




