from goalboost.model import auth_models

class UserAccountQueries:

    def __init__(self):
        self.users = auth_models.User()._get_collection()


    # Todo Error handling, why is list none, etc.?
    def get_users_for_account(self, account):
        pass
        #
        # users = []
        # account = self.accounts.find_one({"name": account})
        # # Todo Better error handling -- why is it none?
        # if(account is None):
        #     return users
        # # account is good at this point
        # # print(account["_id"])
        # return list(self.users.find({"account": account["_id"]}))