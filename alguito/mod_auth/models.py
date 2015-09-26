from flask.ext.login import UserMixin
from alguito.model.entities.userentity import UserEntity
from alguito.datastore import db

class User(UserMixin):

    def __init__(self, username, password):
        self.id = username
        self.password = password

    #def __init__(self, username):
    #    self.username = username

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
