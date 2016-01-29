'''
It may be a good idea to break tlis file out
into test_timer_models, test_auth_models, etc.
'''

from unittest import TestCase

from bson.objectid import ObjectId

from goalboost.model.auth_models import Account, User
from goalboost.model.miscellaneous_models import Project, Tag
from test.common.test_helper import TestHelper, TestObjects # test_data


# Allows us to consider reserved object Ids for testing.
# Not so much a test as a proof of concept
class TestObjectId(TestCase):
    def test_can_get_non_random_object_id(self):
        oid = ObjectId(b"CodeSolid123")
        oid2 = ObjectId(b"CodeSolid123")
        assert (oid == oid2)

    def test_can_get_random_object_id(self):
        oid = ObjectId()
        oid2 = ObjectId()
        assert (oid != oid2)


# -------------- Accounts -------------------------
class TestAccount(TestCase):
    def test_can_create_and_delete_account(self):
        Account.objects(name="Los Pollos Hermanos").delete()
        account = Account(name="Los Pollos Hermanos")
        account.save()
        account2 = Account.objects(id=account.id).first()
        assert(account2.name == account.name)
        Account.objects(id=account.id).delete()

    def test_can_get_users(self):
        user = TestObjects().get_test_user()
        users_for_account = user.account.get_users()
        assert(users_for_account is not None)
        assert(len(users_for_account) > 0)

    def test_can_call_get_users_on_unsaved_account(self):
        Account.objects(name="Los Pollos Hermanos").delete()
        account = Account(name="Los Pollos Hermanos")
        users_for_account = account.get_users()
        assert(users_for_account is not None)
        assert(len(users_for_account) == 0)

class TestTag(TestCase):
    def test_can_create_tag(self):
        t = Tag(accountId = TestObjects().get_test_account().id, name="Goalboost")
        assert(t is not None)
        t.save()
        t2 = Tag.objects(name="Goalboost").first()
        assert(t2.id == t.id)
        t2 = Tag.objects(name="Goalboost").delete()

# -------------- Projects -------------------------
class TestProject(TestCase):
    def setUp(self):
        self.testHelper= TestHelper()

    def test_can_save_load_delete_projects(self):
        p1 = Project(name="CodeSolid Awesome Stuff")
        p1.save()
        p2 = Project.objects(id=p1.id).first()
        assert(p2.name == p1.name)
        Project.objects(id=p1.id).delete()
#  -------------- Users -----------------------------


class TestAuth(TestCase):

    def setUp(self):
        self.testHelper= TestHelper()
        self.security = self.testHelper.app().security

    def test_can_create_and_save_user(self):
        with self.testHelper.app().app_context():
            user = None
            try:
                user_data_store = self.security.datastore

                uTemp = User.objects(email="melblank@bugs.com").first()
                if uTemp is not None:
                    uTemp.delete()

                # -- Should and do really use encrypted password in prod, but slows tests down
                # encrypted = encrypt_password("WhatsUpDocument")
                user = user_data_store.create_user(email="melblank@bugs.com", account=TestObjects().get_test_account(), password="chickens")
                user2 = user_data_store.find_user(email="melblank@bugs.com")
                assert(user.email == user2.email)
                assert(user.account == user2.account)
                # Clean up
            finally:
                if(user is not None):
                    user_data_store.delete_user(user)

    def test_can_verify_token(self):
        with self.testHelper.app().app_context():
            user = None
            try:
                user_data_store = self.security.datastore
                # -- Should and do really use encrypted password in prod, but slows tests down
                # encrypted = encrypt_password("WhatsUpDocument")
                user = user_data_store.create_user(email="melblank@bugs.com", account=TestObjects().get_test_account(), password="chickens")
                # print(str(type(user)))
                token = user.get_auth_token()
                token2 = token
                assert(token == token2)
                result = user.verify_auth_token(token)
                assert(result)
                # Clean up
            finally:
                if(user is not None):
                    user_data_store.delete_user(user)

