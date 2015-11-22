from json import loads
import requests


def format_date(d):
	mm, dd, yyyy = d.split("/")
	return "{0}-{1}-{2} 00:00:00".format(yyyy, mm, dd)

with open('hours.json', 'r') as f:
    read_data = f.read()

user_id = "564550dde1539b15490d4672"
data = loads(read_data)
SECONDS_PER_HOUR = 3600

headers = {"content-type":"application/json"}

i = 0
for entry in data["hours"]:
	seconds = round(entry["hours"] * SECONDS_PER_HOUR)
	date_recorded = format_date(entry["date"])
	request = '{{"running": false, "userId": "{0}", "notes": "{1}","entries": [{{"dateRecorded": "{2}", "seconds": {3}}}]}}'.format( \
		user_id, entry["description"], date_recorded, seconds)	 
	i += 1
	if i == 1:
		print("First one!")
	print("uploading: " + request)
	# r = requests.post("http://goalboost.com/api/timer", data=request, headers=headers)
	# print (r.status_code)
