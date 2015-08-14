from unittest import TestCase
from alguito.endpoints.eve.auth import encode_basicauth_username_and_password
import alguito.app

__author__ = 'john'

class TestAlguitoTokenAuth(TestCase):
    def setUp(self):
        self.app = alguito.app.app.test_client()

    def test_check_auth_fails_if_no_username_sent(self):
        response = self.app.get("/api/alguitos")
        assert response.status_code == 401

    def test_check_auth_succeeds_if_username_sent(self):
        """ Since this authentication method is currently bogus, it works for any Username

            We send a valid Basic auth authorization header, 'Basic QW55QmFkVXNlcm5hbWU6',
            corresponding to username = 'AnyBadUsername' and password = ''.  We got
            this value from Postman.

            Note we send "AUTHORIATION", which becomes "HTTP_AUTHORIZATION" when werkzeug
            is through with it.
        """
        header_value = 'Basic QW55QmFkVXNlcm5hbWU6'
        response = self.app.get("/api/alguitos", headers={'AUTHORIZATION': header_value})
        assert response.status_code == 200

    # Todo this is really testing a function in Auth module, not part of TestAlguitoTokenAuth
    def test_with_auth_using_encoding_function(self):
        """  Same as test_check_auth_succeeds_if_username_sent, but not hardcoded.
        """
        header_value = encode_basicauth_username_and_password(b"AnyBadUsername", b"")
        response = self.app.get("/api/alguitos", headers={'AUTHORIZATION': header_value})
        assert response.status_code == 200
