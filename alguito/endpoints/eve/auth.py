import eve.auth
#import urllib2
import base64
from werkzeug.security import check_password_hash


class RolesAuth(eve.auth.BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        accounts = app.data.driver.db['accounts']
        lookup = {'username': username}
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        account = accounts.find_one(lookup)
        return account and check_password_hash(account['password'], password)

class MyBasicAuth(eve.auth.BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource,
                   method):
        return username == 'admin' and password == 'secret'


class AlguitoTokenAuth(eve.auth.TokenAuth):

    def check_auth(self, token, allowed_roles, resource, method):
        """ Check a a single token which should be passed in the basic auth Username header

            Currently this function does not really check a token, and it may be that using
            something derived from BasicAuth (see MyBasicAuth) makes more sense.
        """
        print("Checking auth, token is " + token)
        return True


def encode_basicauth_username_and_password(username, password):
    """ Return a correct base64 encoded value given a username and password """
    bytestr_formatted = b":".join([username, password])
    base64string = base64.encodebytes(bytestr_formatted).replace(b'\n', b'')
    #base64string = base64string.replace(b'\n', b'')
    return b'Basic ' + base64string
