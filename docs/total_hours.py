from json import loads
with open('hours.json', 'r') as f:
    read_data = f.read()
data = loads(read_data)
hours = [i["hours"] for i in data["hours"]] 
print("Total hours: ", sum(hours))
