import eve.auth

class MyBasicAuth(eve.auth.BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource,
                   method):
        return username == 'admin' and password == 'secret'


class AlguitoTokenAuth(eve.auth.TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        return True

