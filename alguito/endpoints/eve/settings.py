import alguito.endpoints.eve.people as people
import alguito.endpoints.eve.teams as teams

# Let's just use the local mongod instance. Edit as needed.

# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'apitestUser'
MONGO_PASSWORD = 'asf$$95yXpiorE'
MONGO_DBNAME = 'apitest'

# Allows us to serve static files from "static" folder in root, etc.  Cf http://stackoverflow.com/questions/27798842/serve-static-files-with-eve
URL_PREFIX = "api"


DOMAIN = {
    'people': people.people,
    'teams' : teams.teams
}
# Global RESOURCE and ITEM METHODS.  These can be overriden on a per-endpoint basis,
# See: http://python-eve.org/config.html#resource-item-endpoints

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

XML = False