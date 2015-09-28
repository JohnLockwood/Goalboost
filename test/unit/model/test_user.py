from unittest import TestCase
from alguito.datastore import db
from test.common.test_helper import TestHelper

from alguito.mod_auth.models import UserEntity

class TestAuth(TestCase):
    def setUp(self):

        self.testHelper= TestHelper()
        #self.client = self.testHelper.test_client()
        #self.testContext = self.testHelper.test_request_context()

    def test_can_create_and_save_user(self):
        with self.testHelper.app().app_context():
            session = db.session
            # Todo need to hash password, add authentication logic
            #u2 = User()
            #u2.metadata.create_all(bind=_engine)
            try:
                u = UserEntity(name="John", email="john@particlewave.com", fullname='John Lockwood', password="Foopdewop")
                session.add(u)
                session.commit()
            except Exception as e:
                # Swalliow excption if exists
                session.rollback()

            u2 = session.query(UserEntity).filter(UserEntity.fullname == "John Lockwood").one()
            assert(u2 is not None)
            assert(u2.name == "John")

            assert(not u2.verify_password('Not Foopdewop'))
            assert(u2.verify_password('Foopdewop'))

    def test_can_delete_user_and_recreate(self):
        with self.testHelper.app().app_context():
            session = db.session
            # Delete
            try:
                session.query(UserEntity).filter(UserEntity.email == "john@particlewave.com").delete()
                session.commit()
            except Exception as e:
                session.rollback()

            # Recreate
            try:
                u = UserEntity(name="John", email="john@particlewave.com", fullname='John Lockwood', password="Foopdewop")
                session.add(u)
                session.commit()
            except Exception as e:
                # Swalliow excption if exists
                session.rollback()



