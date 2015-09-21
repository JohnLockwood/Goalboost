from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from alguito.model.entities.base import Base
from passlib.hash import pbkdf2_sha256



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
        hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        self._password = hash

    @hybrid_method
    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self._password)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)
