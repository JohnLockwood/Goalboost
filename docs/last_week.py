from dateutil.parser import parse
from datetime import datetime, timedelta
now = datetime.now()
now = now.replace(hour=0, minute=0, second=0, microsecond=0)

from json import loads
with open('hours.json', 'r') as f:
    read_data = f.read()
data = loads(read_data)
total_hours_this_week = 0
for i in data["hours"]:
	the_date = parse(i["date"])
	delta_t = now - the_date

	if delta_t.days < 7:
		print(i["date"], " - ", i["hours"], " - ", i["description"])
		total_hours_this_week = total_hours_this_week + i["hours"]

print("Total hours this week: ", round(total_hours_this_week, 1))
