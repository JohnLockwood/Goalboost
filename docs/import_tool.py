from json import loads, dumps
import requests
from requests.auth import HTTPBasicAuth
import os
import configparser

def get_user_info():
	config_file = os.path.expanduser('~') + "/.gbconfig"
	config = configparser.ConfigParser()
	settings  = config.read([config_file])
	if len(settings) != 1:	
		sys.exit("Config file not found")
	return dict(config.items("user"))

def format_date(d):
	mm, dd, yyyy = d.split("/")
	return "{0}-{1}-{2} 00:00:00".format(yyyy, mm, dd)

# Todo hard codes filename
def load_records():
	with open('hours.John.json', 'r') as f:
		read_data = f.read()
		data = loads(read_data)
		return data

def upload_records():

	#url_root = "http://localhost:5000"
	url_root = "http://goalboost.com"

	user_info = get_user_info()
	SECONDS_PER_HOUR = 3600
	headers = {"content-type":"application/json"}
	data = load_records()

	for entry in data["hours"]:
		seconds = round(entry["hours"] * SECONDS_PER_HOUR)
		date_recorded = format_date(entry["date"])
		auth = HTTPBasicAuth(user_info["email"],  user_info["token"])
		request_data = dict(tags = ["Goalboost"], running=False, user =  user_info["id"], notes = entry["description"], dateEntered = entry["date"], seconds = seconds, lastRestart = date_recorded) 
		request_data = dumps(request_data)
		
		try:
			r = requests.post(url_root + "/api/v1/timer", data=request_data, headers=headers, auth=auth)
			if r.status_code != 201:
				print("Error, data = " + request_data + " -- status code = " + str(r.status_code))
		except:
			print("Exception in data " + request_data)
		

upload_records()