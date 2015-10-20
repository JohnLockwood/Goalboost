from unittest import TestCase
from flask_security.utils import encrypt_password
from alguito.model.business_objects import UserTimer
from test.common.test_helper import TestHelper
from alguito.datastore import db
from alguito.model.mongo_models import Task
from datetime import datetime
from alguito.model.mongo_models import Timer

class UserTimerTest(TestCase):

    def setUp(self):
        self.testHelper = TestHelper()
        with self.testHelper.app().app_context():

            self.security = self.testHelper.app().security
            user_data_store = self.security.datastore
            user = user_data_store.find_user(email="hasTimers@scheduled.com")
            if (user):
                self.user = user
            else:
                # We don't need to encrypt password here -- slows tests down a LOT!!!
                #encrypted = encrypt_password("WhatsUpDocument")
                self.user = user_data_store.create_user(email="hasTimers@scheduled.com", account="foghorn", password="foo")

    def tearDown(self):
        with self.testHelper.app().app_context():
            user_data_store = self.security.datastore
            user_data_store.delete_user(self.user)



    def test_can_create_user_timer(self):
        user_timer = UserTimer(self.user, db)
        assert(user_timer.timer_get() is None)

    def test_can_create_timer_on_user_timer(self):
        assert(self.user.timer is None)
        user_timer = UserTimer(self.user, db)
        timer = user_timer.timer_create()
        assert(self.user.timer is not None)
        assert(timer is not None)
        assert(timer.userId is not None)

    def test_can_create_and_clear_timer_on_user_timer(self):
        assert(self.user.timer is None)
        user_timer = UserTimer(self.user, db)
        timer = user_timer.timer_create()
        assert(self.user.timer is not None)
        assert(timer is not None)
        assert(timer.userId is not None)

        user_timer.timer_clear()
        timer = user_timer.timer_get()
        assert(timer is None)
        assert(user_timer.user.timer is None)

    def test_can_start_timer(self):
        pass

    def test_can_stop_timer(self):
        pass

    def test_can_restart_timer(self):
        pass

    def test_can_restart_timer(self):
        pass

    # Possible business rule tests

    def test_clearing_active_timer_raises_exception(self):
        pass
