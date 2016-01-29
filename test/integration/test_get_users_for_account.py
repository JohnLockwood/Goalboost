from unittest import TestCase
import goalboost.model.queries.user_account as queries

class test_user_account(TestCase):
  def test_i_can_haz_collection(self):
    q = queries.UserAccountQueries()
    assert(q.users is not None)
    #print(type(q.users))
    user = q.users.find_one({"email": "elitepropertiesbroker@gmail.com"})
    assert(user["_id"] is not None)
