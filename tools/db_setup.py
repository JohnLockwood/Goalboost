from pymongo import MongoClient
import datetime
from bson.json_util import dumps 

client = MongoClient()
db = client.goalboost

# Add Roles
collection = db["role"]
roles = [
	{"name" : "Root", "description" : "Site Owner, administator of all accounts"},
	{"name" : "Account Admin", "description" : "Administrator with elevated privileges for a single account only"},
	{"name" : "Account User", "description"  : "User under an account with no elevated rights"} ]
for role in roles:
	collection.insert_one(role)

# Additional work as needed here