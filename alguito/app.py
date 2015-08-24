from eve import Eve
# from flask.ext.triangle import Triangle

# eve endpoints, i.e., in general, JSON restful endpoints
# See eve_settings.DOMAIN below for the mappings of routes to people for these endpoints
import alguito.endpoints.eve.people as people
import alguito.endpoints.eve.teams as teams
import alguito.endpoints.eve.alguitos as alguitos

# flask endpoints, i.e., web pages.
# For route information for these endpoints, see the app.add_url_rule calls further below
import alguito.endpoints.controllers.index as index
import alguito.endpoints.controllers.register as register

eve_settings = {
    # Please note that MONGO_HOST and MONGO_PORT could very well be left
    # out as they already default to a bare bones local 'mongod' instance.
    'MONGO_HOST': 'localhost',
    'MONGO_PORT': 27017,
    'MONGO_USERNAME': 'apitestUser',
    'MONGO_PASSWORD': 'asf$$95yXpiorE',
    'MONGO_DBNAME': 'apitest',

    # Allows us to serve static files from "static" folder in root, etc.  Cf http://stackoverflow.com/questions/27798842/serve-static-files-with-eve
    'URL_PREFIX': "api",

    'DOMAIN': {
        'people': people.people,
        'teams' : teams.teams,
        'alguitos': alguitos.alguitos
    },

    # Global RESOURCE and ITEM METHODS.  These can be overriden on a per-endpoint basis,
    # See: http://python-eve.org/config.html#resource-item-endpoints

    # Enable reads (GET), inserts (POST) and DELETE for resources/collections
    # (if you omit this line, the API will default to ['GET'] and provide
    # read-only access to the endpoint).
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],

    # Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
    # individual items  (defaults to read-only item access).
    'ITEM_METHODS': ['GET', 'PATCH', 'PUT', 'DELETE'],

    'XML': False
}
app = Eve(__name__, settings=eve_settings)


# But as long as you keep this in the root, everything works fine from a file, until it doesn't because
# of stupid import rules.
# app = Eve(__name__, settings='eve_')


# Define non-eve flask routes

# Non-eve flask routes are defined in functions in the package alguito.endpoints.controllers
# Routes are defined here.
app.add_url_rule('/', 'index', index.index)
app.add_url_rule('/home/<page>', '/home', index.home)
app.add_url_rule('/register/register', '/register/register', register.register)
app.add_url_rule('/register/login', '/register/login', register.login)

if __name__ == '__main__':
    app.secret_key = 'O#WQiCRf%b*u%XLCDGO8tT31AIyCQ48TN5KkXqHQrkyS*%$jZ#hgiInYtNUC1aWUeu1PdcZNHBgcWv3%9h&lmFZg&kc7Gv'
    app.run(debug=True, port=5001)



