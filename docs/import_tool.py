from json import loads

def format_date(d):
	mm, dd, yyyy = d.split("/")
	return "{0}-{1}-{2} 00:00:00".format(yyyy, mm, dd)

with open('hours.json', 'r') as f:
    read_data = f.read()

user_id = "564550dde1539b15490d4672"
data = loads(read_data)
SECONDS_PER_HOUR = 3600
for entry in data["hours"]:
	seconds = round(entry["hours"] * SECONDS_PER_HOUR)
	date_recorded = format_date(entry["date"])
	request = '{{"running": false, "userId": "{0}", notes":" {1}","entries": [{{"dateRecorded": "{2}", seconds": {3}}}]}}'.format( \
		user_id, entry["description"], date_recorded, seconds)	 

	print(request)

#hours = [i["hours"] for i in data["hours"]] 
#print("Total hours: ", round(sum(hours), 1))
