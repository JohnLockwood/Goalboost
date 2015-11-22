import requests

data = '{"running": false, "userId": "564550dde1539b15490d4111", "notes": "Testing this very entry via Python requests library","entries": [{"dateRecorded": "2015-11-21 00:00:00", "seconds": 10800}]}'
headers = {"content-type":"application/json"}
r = requests.post("http://goalboost.com/api/timer", data=data, headers=headers)
print (r.status_code)