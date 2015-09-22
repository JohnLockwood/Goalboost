from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

_engine = create_engine("mysql+pymysql://root:Newacct1@localhost/alguito", encoding='utf8', echo=True)
_Session = sessionmaker(bind=_engine)

def get_session():
    return _Session()
