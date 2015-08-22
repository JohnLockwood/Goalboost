from eve import Eve
from flask import render_template
from flask import session


# Sample (was working) alternate configuration from dict
import alguito.endpoints.eve.people as people
import alguito.endpoints.eve.teams as teams
import alguito.endpoints.eve.alguitos as alguitos

from flask import request, url_for

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
@app.route('/')
def index():
    # return app.send_static_file('index.html') -- use this if in static dir
    # Or return "Hello world" for example to simply display a string
    return render_template('index.html')

@app.route('/login/register')
def register():
    session['test'] = 'Passed!'
    return render_template('login/register.html')

@app.route('/login/login')
def login():
    return render_template('login/login.html')

if __name__ == '__main__':
    app.secret_key = 'O#WQiCRf%b*u%XLCDGO8tT31AIyCQ48TN5KkXqHQrkyS*%$jZ#hgiInYtNUC1aWUeu1PdcZNHBgcWv3%9h&lmFZg&kc7Gv'
    app.run(debug=True, port=5001)
