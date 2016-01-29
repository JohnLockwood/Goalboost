import pymongo

class TimerFinder:

	def __init__(self):
		self.client = pymongo.MongoClient('mongodb://localhost:27017/')
		self.db = self.client.goalboost
		self.accounts = self.db["account"]
		self.users = self.db["user"]
		self.timers = self.db["timer"]

	
	# Todo Error handling, why is list none, etc.?
	def get_users_for_account(self, account):
		users = []
		account = self.accounts.find_one({"name": account})
		# Todo Better error handling -- why is it none?
		if(account is None):
			return users
		# account is good at this point	
		# print(account["_id"])
		return list(self.users.find({"account": account["_id"]}))

	# Todo Error handling, why is list none, etc.?
	def get_timers_for_account(self, account):
		timers = [] 		
		users = self.get_users_for_account(account)
		user_ids = [user["_id"] for user in users]
		if len(users) == 0:
			return timers
		return list(self.timers.find({"user": { "$in": user_ids} }))

# utf = TimerFinder()
# users = utf.get_users_for_account("Goalboost")
# if(len(users) == 1):
# 	print("John's email is: " + users[0]["email"])
#
# timers = utf.get_timers_for_account("Goalboost")
# for timer in timers:
# 	print(timer["notes"])