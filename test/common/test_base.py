import alguito.app

class TestH():

    def setUp(self):
        self.app = alguito.app.app.test_client()
        print("Inside TestBase setup")

    def get_test_client(self):
        return self.app
