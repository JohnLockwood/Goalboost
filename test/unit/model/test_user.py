from unittest import TestCase
# from test.common.test_helper import TestHelper
from alguito.model.dal.database import get_session
# from alguito.model.dal.database import _engine
from alguito.model.entities.user import User

class TestAuth(TestCase):
    #def setUp(self):
    #    self.testHelper= TestHelper()

    def test_can_create_and_save_user(self):
        session = get_session()
        # Todo need to hash password, add authentication logic
        #u2 = User()
        #u2.metadata.create_all(bind=_engine)
        try:
            u = User(name="John", email="john@particlewave.com", fullname='John Lockwood', password="Foopdewop")
            session.add(u)
            session.commit()
        except Exception as e:
            print(e)

        # Need a new session now -- last is rolled back
        session = get_session()
        u2 = session.query(User).filter(User.fullname == "John Lockwood").one()
        assert(u2 is not None)
        assert(u2.name == "John")
