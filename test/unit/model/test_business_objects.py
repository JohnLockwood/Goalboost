from unittest import TestCase

from goalboost.model.business_objects import UserTimer
from goalboost.model import db
from goalboost.model.models_auth import User
from test.common.test_helper import TestHelper, test_object_ids

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
                self.user = user_data_store.create_user(email="hasTimers@scheduled.com", accountId=test_object_ids["DEMO"], password="foo")

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

    def test_can_create_john_timer(self):
        query_result = User.objects(email="elitepropertiesbroker@gmail.com")
        u = query_result.first()
        user_timer = UserTimer(u, db)
        timer = user_timer.timer_create()
        timer.set_seconds_today(300)
        timer.notes = "John's perpetual timer"
        timer.start()
        timer.save()

    def test_timer_not_running_when_created(self):
        user_timer = UserTimer(self.user, db)
        assert(user_timer.timer_get() is None)
        timer = user_timer.timer_create()
        assert(not timer.is_running())

    def test_timer_running_when_started(self):
        user_timer = UserTimer(self.user, db)
        assert(user_timer.timer_get() is None)
        timer = user_timer.timer_create()
        assert(not timer.is_running())
        timer.start()
        assert(timer.is_running())

    def test_timer_not_running_when_stopped(self):
        user_timer = UserTimer(self.user, db)
        assert(user_timer.timer_get() is None)
        timer = user_timer.timer_create()
        timer.start()
        timer.stop()
        assert(not timer.is_running())

    def test_can_restart_timer(self):
        user_timer = UserTimer(self.user, db)
        assert(user_timer.timer_get() is None)
        timer = user_timer.timer_create()
        timer.start()
        timer.stop()
        assert(not timer.is_running())
        timer.start()
        assert(timer.is_running())
        timer.stop()
        assert(not timer.is_running())

    # Possible business rule tests
    ##def test_clearing_active_timer_raises_exception(self):
    ##    pass
