'''
    Todo get mongo config working then
    see which of the following test setups correctly grabs the tests
'''

from unittest import TestCase
from test.common.test_helper import TestHelper
from alguito.model.mongo_models import Task

class TestTask(TestCase):

    def setUp(self):
        self.testHelper= TestHelper()

    def test_can_create_and_save_task(self):
        with self.testHelper.app().app_context():
            try:
                task = Task(name="Write a 1st mongo entity", description="Try to write a simple Task entity and save it")
                task.save()
            finally:
                pass

    # This "works" ok, but when we add configuration to go to the correct MONGODB database, password, etc.
    # It will not work without further configuration
    def test_can_save_without_app(self):
        task = Task(name="Write another mongo entity", description="Save without an app!")
        task.save()

    def test_can_create_and_save_task_another_way(self):
        with self.testHelper.app().test_request_context():
            try:
                task = Task(name="Write a 1st mongo entity", description="Try to write a simple Task entity and save it")
                task.save()
            finally:
                pass

