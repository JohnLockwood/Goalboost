from sqlalchemy import Column, Integer, String
from alguito.model.entities.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    email = Column(String(120), unique=True)
    fullname = Column(String(120))
    password = Column(String(120))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)
