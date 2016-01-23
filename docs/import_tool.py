from json import loads, dumps
import requests


def format_date(d):
	mm, dd, yyyy = d.split("/")
	return "{0}-{1}-{2} 00:00:00".format(yyyy, mm, dd)

with open('hours.John.json', 'r') as f:
    read_data = f.read()

data = loads(read_data)
SECONDS_PER_HOUR = 3600

headers = {"content-type":"application/json"}

i = 0
for entry in data["hours"]:
	seconds = round(entry["hours"] * SECONDS_PER_HOUR)
	date_recorded = format_date(entry["date"])
	request_data = dict(running=False, userId = user_id, notes = entry["description"], dateEntered = entry["date"], seconds = seconds, lastRestart = date_recorded) 
	#request = '{{"running": false, "userId": "{0}", "notes": "{1}", "dateEntered": "{2}", "seconds": "{3}", "lastRestart": "{4}"}}'.format( \
	#	user_id, entry["description"], entry["date"], seconds, date_recorded)	 
	i += 1
	if i == 1:
		#print("First one!")
		#print("uploading: " + request)
		print(dumps(request_data))
	# r = requests.post("http://goalboost.com/api/timer", data=request, headers=headers)
	# print (r.status_code)
