from unittest import TestCase

from goalboost.model.timer_models import Timer
from test.common.test_helper import TestObjects
from goalboost.blueprints.auth import can_access_user_owned_resource

class TestResourceAccess(TestCase):
    test_objects = TestObjects()

    def test_user_can_access_their_own_resource(self):
        test_objects = TestObjects()
        test_user = test_objects.get_test_user()
        timer = Timer(notes="More testing, boss", user=test_user)
        timer.save()
        assert(can_access_user_owned_resource(test_user, timer))
        timer.delete()

    def test_account_admin_can_access_resource_if_account_same(self):
        test_objects = TestObjects()
        test_user = test_objects.get_test_user()
        timer = Timer(notes="More testing, boss", user=test_user)
        timer.save()
        assert(can_access_user_owned_resource(test_user, timer))
        timer.delete()

    def test_account_admin_cannot_access_resource_if_account_different(self):
        test_objects = TestObjects()
        test_user = test_objects.get_test_user()
        timer = Timer(notes="More testing, boss", user=test_user)
        timer.save()
        assert(can_access_user_owned_resource(test_user, timer))
        timer.delete()


