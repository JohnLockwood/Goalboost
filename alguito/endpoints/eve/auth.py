import eve.auth
import base64
from werkzeug.security import check_password_hash
from flask import current_app as app



"""
    Notes:
    One way to structure this simply is to have a single auth for people, for example,
    which allows admin (aka ROOT aka God) to get in and do anything, or to allow
    edits if password checks out and is a member of team.
"""
class TeamAndPasswordAuth(eve.auth.BasicAuth):

    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        accounts = app.data.driver.db['accounts']
        account = accounts.find_one({'username': username})
        # set 'auth_field' value to the account's ObjectId
        # (instead of _id, you might want to use ID_FIELD)
        if account and 'team' in account:
            pass # self.set_request_auth_value(account['team'])

        return account and check_password_hash(account['password'], password)

def encode_basicauth_username_and_password(username, password):
    """ Return a correct base64 encoded value given a username and password """
    bytestr_formatted = b":".join([username, password])
    base64string = base64.encodebytes(bytestr_formatted).replace(b'\n', b'')
    return b'Basic ' + base64string

# ----------------------------------------------------------------------------------------------
# Todo:  Everything from here down is reference material only.  Incorporate somewhere or delete.
'''

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
'''
